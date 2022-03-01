# JPEG-Compressor
a JPEG compressor with GUI

一款带有图形化界面的 JPEG 压缩软件



打包exe文件步骤：

1. 运行 `pip install nuitak` 安装 nuitak 打包工具模块

2. 运行 

   ```
   nuitka --standalone --windows-disable-console --enable-plugin=pyside2 --enable-plugin=numpy --onefile --output-dir=out --windows-icon-from-ico=favicon.ico GUI.py
   ```

   注意此处的 `favicon.ico` 及`GUI.py`皆为相对路径

3. 生成的exe文件在相对路径的`\out\GUI.dist\`下找到



based on:     [O1sInfo/jpeg-encoder: JPEG implemention (github.com)](https://github.com/O1sInfo/jpeg-encoder)

