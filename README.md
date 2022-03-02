# JPEG-Compressor

A JPEG compressor with GUI.

Get started by running   `GUI.py `  !

一款带有图形化界面的 JPEG 压缩软件

程序入口： `GUI.py `

打包exe文件步骤：

1. 运行 `pip install nuitak` 安装 nuitak 打包工具模块

2. 运行

   ```
   nuitka --standalone --windows-disable-console --include-qt-plugins=sensible,styles --plugin-enable=qt-plugins --enable-plugin=numpy --enable-plugin=pyqt5 --onefile --output-dir=out --windows-icon-from-ico=favicon.ico GUI.py
   ```

   注意此处的 `favicon.ico` 及`GUI.py`皆为相对路径

3. 生成的exe文件在相对路径的 `\out\GUI.dist\`目录下

Course Exercise of CUMT.

based on:     [O1sInfo/jpeg-encoder: JPEG implemention (github.com)](https://github.com/O1sInfo/jpeg-encoder)

