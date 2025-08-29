import os
import argparse
import mmap
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import time  # 导入 time 模块

# 默认的文件类型（无限制）
DEFAULT_FILE_EXTENSIONS = ()

# 定义扫描文件内容的函数（使用 mmap）
def search_in_file_with_mmap(file_path, keyword, output_file):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            mmapped_file = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            content = mmapped_file.decode('utf-8', errors='ignore')
            lines = content.splitlines()

            # 遍历每一行，查找关键词并输出行号和列号
            for line_num, line in enumerate(lines, start=1):
                col_num = line.lower().find(keyword.lower()) + 1  # 找到第一个匹配的位置
                if col_num > 0:
                    result = f"在文件 {file_path} 的第 {line_num} 行，第 {col_num} 列找到匹配内容"
                    print(result)  # 打印到终端
                    output_file.write(result + "\n")  # 写入文件
            mmapped_file.close()
    except Exception as e:
        pass  # 如果无法读取文件，跳过

# 文件名匹配和内容匹配函数
def search_file(file_path, keyword, max_file_size, read_content, allowed_extensions, output_file):
    if allowed_extensions and not file_path.endswith(allowed_extensions):
        return  # 跳过不需要处理的文件类型

    # 如果文件大小限制为“无限大”，则不进行大小限制
    if max_file_size != -1 and os.path.getsize(file_path) > max_file_size:
        return  # 跳过大于最大文件大小的文件

    # 文件名匹配
    if keyword.lower() in file_path.lower():
        result = f"找到文件名匹配: {file_path}"
        print(result)  # 打印到终端
        output_file.write(result + "\n")  # 写入文件
        if read_content:  # 如果需要读取文件内容
            search_in_file_with_mmap(file_path, keyword, output_file)  # 扫描文件内容

# 文件遍历与多线程执行
def search_files(directory, keyword, max_threads, max_file_size, read_content, allowed_extensions, output_file):
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                futures.append(executor.submit(search_file, file_path, keyword, max_file_size, read_content, allowed_extensions, output_file))

        # 等待任务完成
        for future in as_completed(futures):
            future.result()  # 获取结果，确保执行完毕

def main():
    # 记录开始时间
    start_time = time.time()

    # 命令行参数解析
    parser = argparse.ArgumentParser(description="使用多线程搜索文件名和内容")
    parser.add_argument("directory", help="要搜索的目录路径")
    parser.add_argument("keyword", help="搜索的关键词")
    parser.add_argument("--threads", type=int, default=10, help="设置线程数，默认是 10")
    parser.add_argument("--max-size", type=int, default=10 * 1024 * 1024, help="设置最大文件大小，单位是字节，默认是 10MB。使用 -1 或 'inf' 表示无限大")
    parser.add_argument("--read-content", action="store_true", help="是否读取文件内容进行匹配，默认不读取")
    parser.add_argument("--file-types", type=str, default="", help="指定要搜索的文件类型，以逗号分隔（例如：txt,pdf,log）。默认没有文件类型限制")
    parser.add_argument("--output-file", type=str, default="search_results.txt", help="将搜索结果输出到文件，默认是 'search_results.txt'")

    # 解析并处理 --max-size 参数
    args = parser.parse_args()

    # 处理文件类型参数，如果为空表示无限制
    allowed_extensions = tuple(f".{ext.strip()}" for ext in args.file_types.split(',')) if args.file_types else DEFAULT_FILE_EXTENSIONS

    # 处理文件大小无限大的情况
    if args.max_size == 'inf' or args.max_size == -1:
        max_file_size = -1  # 表示无限大
    else:
        max_file_size = int(args.max_size)

    # 打开输出文件
    with open(args.output_file, "w", encoding="utf-8") as output_file:
        # 调用文件搜索函数
        search_files(args.directory, args.keyword, args.threads, max_file_size, args.read_content, allowed_extensions, output_file)

        # 记录结束时间并计算总时长
        end_time = time.time()
        elapsed_time = end_time - start_time
        output_file.write(f"\n总共执行时间: {elapsed_time:.2f} 秒\n")
    
    print(f"搜索结果已输出到 {args.output_file}")

if __name__ == "__main__":
    main()
