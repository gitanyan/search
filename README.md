# 🔍 Search

一个基于 **Python** 编写的高效多线程文件搜索工具。  
支持搜索文件名和文件内容，能够灵活设置线程数、文件大小限制、文件类型过滤，并可将结果保存到文件中。

---

## ✨ 功能特性
- ✅ **多线程搜索**：支持自定义线程数，加速搜索效率  
- ✅ **关键词搜索**：可匹配文件名和文件内容  
- ✅ **可选内容读取**：支持指定是否扫描文件内容  
- ✅ **文件大小控制**：支持限制最大文件大小，或设置为无限制  
- ✅ **文件类型过滤**：可按文件扩展名过滤目标文件  
- ✅ **结果保存**：搜索结果会输出到终端，同时保存到文件  
- ✅ **位置信息**：当开启内容搜索时，会显示关键词在文件中的行列位置  
- ✅ **耗时统计**：搜索完成后显示总耗时  

---

## 📦 安装与运行
### 1. 克隆仓库
```bash
git clone https://github.com/your-username/file-search-tool.git
cd file-search-tool
```

| 参数               | 类型      | 默认值                | 说明                                 |
| ---------------- | ------- | ------------------ | ---------------------------------- |
| `directory`      | str     | **必填**             | 要搜索的目录路径                           |
| `keyword`        | str     | **必填**             | 搜索关键词                              |
| `--threads`      | int     | 10                 | 设置线程数                              |
| `--max-size`     | int/str | 10MB               | 设置最大文件大小（字节）。支持 `-1` 或 `inf` 表示无限制 |
| `--read-content` | flag    | False              | 是否读取文件内容进行匹配                       |
| `--file-types`   | str     | 无限制                | 指定要搜索的文件类型，以逗号分隔（如：`txt,log,md`）   |
| `--output-file`  | str     | search_results.txt | 保存搜索结果的文件名                         |

## 🔍 使用示例

### 1. 搜索目录下所有文件名

`python search_files.py ./documents report`

### 2. 使用多线程（20个线程）加快搜索

`python search_files.py ./documents report --threads 20`

### 3. 搜索文件内容，并限制文件大小为 5MB

`python search_files.py ./documents report --read-content --max-size 5242880`

### 4. 搜索特定类型的文件（只搜索 `.txt` 和 `.log`）

`python search_files.py ./documents report --file-types txt,log`

### 5. 保存结果到指定文件

`python search_files.py ./documents report --output-file results.txt`

## 📊 输出示例

**终端显示：**
```bash
找到文件名匹配: ./documents/report1.txt
在文件 ./documents/report1.txt 的第 2 行，第 15 列找到匹配内容
在文件 ./documents/report2.log 的第 5 行，第 8 列找到匹配内容
总共执行时间: 2.34 秒
```

结果文件（results.txt）：
```bash
找到文件名匹配: ./documents/report1.txt
在文件 ./documents/report1.txt 的第 2 行，第 15 列找到匹配内容
在文件 ./documents/report2.log 的第 5 行，第 8 列找到匹配内容

总共执行时间: 2.34 秒
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

步骤：

1. Fork 本仓库
    
2. 创建功能分支 (`git checkout -b feature/xxx`)
    
3. 提交更改 (`git commit -m 'Add xxx feature'`)
    
4. 推送分支 (`git push origin feature/xxx`)
    
5. 提交 Pull Request
