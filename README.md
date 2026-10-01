# csv-shape

快速查看 CSV 的标题、空值数量和大致值类型，不会打印单元格内容。逐行读取，不需要第三方依赖。

## 使用

需要 Python 3.8+。

```sh
python csv_shape.py data.csv
```

也可通过管道输入：

```sh
cat data.csv | python csv_shape.py
```

第一行会被视为标题；支持 UTF-8 与 UTF-8 BOM，分隔符固定为逗号。空白单元格按空值计；类型判断只区分布尔值、有限数字和文本，是快速提示，不是完整的数据校验。最多处理 1,000 列，输出前 200 列。标题名称会显示，也可能含敏感信息；单元格内容不会显示。

## 许可

MIT，见 [LICENSE](LICENSE)。
## Linux x86_64 下载

- [单文件版](https://github.com/506058115-cmd/csv-shape/releases/download/v1.0.0/csv-shape-linux-x86_64-onefile.tar.gz)
- [目录版](https://github.com/506058115-cmd/csv-shape/releases/download/v1.0.0/csv-shape-linux-x86_64-onedir.tar.gz)
- [v1.0.0 Release 页面](https://github.com/506058115-cmd/csv-shape/releases/tag/v1.0.0)

压缩包附带构建信息和依赖许可证；Release 另附 SHA-256 校验文件。产物在 WSL Ubuntu 24.04（Python 3.12.3、PyInstaller 6.22.2）中构建，目标为 GNU/Linux x86_64。较旧的发行版可能需要兼容的 glibc。
