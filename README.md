# JPEG-Compressor(Encoder)压缩器

A JPEG compressor with GUI.

Get started by running   `GUI.py `  !

一款带有图形化界面的 JPEG 压缩软件

程序入口： `GUI.py `

打包exe文件步骤：

1. 运行 `pip install pyinstaller` 安装 pyinstaller打包工具模块

2. 运行

   ```
   pyinstaller GUI.py --onefile --windowed --icon=favicon.ico
   ```

   注意此处的 `favicon.ico` 及`GUI.py`皆为相对路径

3. 生成的exe文件在相对路径的 `\dist\`目录下


参见:[JPEG原理详解(附python实现)](https://blog.csdn.net/qq_41137110/article/details/121724551?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-1.pc_relevant_antiscan&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~Rate-1.pc_relevant_antiscan&utm_relevant_index=2)， [jpeg图片格式详解](https://blog.csdn.net/qq_41137110/article/details/117431046)，[【原创】JPEG图像密写研究（三）
数据流译码 - 连城测 - 博客园 (
cnblogs.com)](https://www.cnblogs.com/gungnir2011/p/3624715.html)， [O1sInfo/jpeg-encoder: JPEG implemention (github.com)](https://github.com/O1sInfo/jpeg-encoder)

