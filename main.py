import os
import argparse
import mmap
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from threading import Lock

# 默认的文件类型（无限制）
DEFAULT_FILE_EXTENSIONS = ()

# 全局结果缓存 + 锁（避免多线程写文件冲突）
results = []
lock = Lock()

def log_result(text):
    """线程安全的结果记录"""
    with lock:
        results.append(text)
        print(text)

# 定义扫描文件内容的函数（使用 mmap）
def search_in_file_with_mmap(file_path, keyword):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                content = mmapped_file[:].decode("utf-8", errors="ignore")
                lines = content.splitlines()

                # 遍历每一行，查找所有关键词出现位置
                for line_num, line in enumerate(lines, start=1):
                    for match in re.finditer(re.escape(keyword), line, re.IGNORECASE):
                        col_num = match.start() + 1
                        result = f"在文件 {file_path} 的第 {line_num} 行，第 {col_num} 列找到匹配内容"
                        log_result(result)
    except Exception:
        pass  # 不能读的文件直接跳过

# 文件名匹配和内容匹配函数
def search_file(file_path, keyword, max_file_size, read_content, allowed_extensions):
    if allowed_extensions and not file_path.endswith(allowed_extensions):
        return  # 跳过不需要处理的文件类型

    try:
        # 文件大小限制
        if max_file_size != -1 and os.path.getsize(file_path) > max_file_size:
            return

        # 文件名匹配
        if keyword.lower() in file_path.lower():
            result = f"找到文件名匹配: {file_path}"
            log_result(result)

        # 文件内容匹配
        if read_content:
            search_in_file_with_mmap(file_path, keyword)
    except Exception as e:
        log_result(f"处理文件时出错: {file_path}, 错误: {e}")

# 文件遍历与多线程执行
def search_files(directory, keyword, max_threads, max_file_size, read_content, allowed_extensions):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(search_file, file_path, keyword, max_file_size, read_content, allowed_extensions))

        # 等待任务完成
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                log_result(f"线程执行错误: {e}")

def main():
    # 记录开始时间
    start_time = time.time()

    # 命令行参数解析
    parser = argparse.ArgumentParser(description="使用多线程搜索文件名和内容")
    parser.add_argument("directory", help="要搜索的目录路径")
    parser.add_argument("keyword", help="搜索的关键词")
    parser.add_argument("--threads", type=int, default=10, help="设置线程数，默认是 10")
    parser.add_argument("--max-size", type=str, default="10485760", help="设置最大文件大小，单位是字节，默认是 10MB。使用 -1 或 inf 表示无限大")
    parser.add_argument("--read-content", action="store_true", help="是否读取文件内容进行匹配，默认不读取")
    parser.add_argument("--file-types", type=str, default="", help="指定要搜索的文件类型，以逗号分隔（例如：txt,pdf,log）。默认没有文件类型限制")
    parser.add_argument("--output-file", type=str, default="search_results.txt", help="将搜索结果输出到文件，默认是 'search_results.txt'")

    args = parser.parse_args()

    # 处理文件类型参数
    allowed_extensions = tuple(f".{ext.strip()}" for ext in args.file_types.split(',')) if args.file_types else DEFAULT_FILE_EXTENSIONS

    # 处理文件大小无限大的情况
    if args.max_size.lower() in ("inf", "-1"):
        max_file_size = -1
    else:
        max_file_size = int(args.max_size)

    # 调用文件搜索函数
    search_files(args.directory, args.keyword, args.threads, max_file_size, args.read_content, allowed_extensions)

    # 记录结束时间
    end_time = time.time()
    elapsed_time = end_time - start_time

    # 写入结果到文件
    with open(args.output_file, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(line + "\n")
        output_file.write(f"\n总共执行时间: {elapsed_time:.2f} 秒\n")

    print(f"搜索结果已输出到 {args.output_file}")

if __name__ == "__main__":
    main()
