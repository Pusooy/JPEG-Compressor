import sys
import webbrowser

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog

import encodeImg
from fileInfo import *
# 从生成的.py文件导入定义的窗口类
from ui_mainwindow import Ui_MainWindow


# 定义主窗体
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 初始化窗口
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('favicon.ico'))
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())

        self.quantity = 50  # 压缩质量
        self.imgFilePath = ''  # 压缩图片路径
        self.outFilePath = ''  # 生成图片路径
        self.flushLog = True  # 实时打印日志

        # 绑定事件处理函数
        selectImgButton = self.ui.selectImgButton
        selectImgButton.clicked.connect(self.selectImg)
        quantitylSlider = self.ui.quantitylSlider
        quantitylSlider.valueChanged.connect(self.sliderMove)
        compressButton = self.ui.compressButton
        compressButton.clicked.connect(self.compressImg)
        openFilePathButton = self.ui.openFilePathButton
        openFilePathButton.clicked.connect(self.openFilePath)
        githubButton = self.ui.githubButton
        githubButton.clicked.connect(self.openGithub)

    def openGithub(self):
        webbrowser.open('https://github.com/TrumpHe/JPEG-Compressor', new=0, autoraise=True)

    def openFilePath(self):
        path = '\\'.join(self.outFilePath.split('/')[0:-1])
        os.startfile(path)

    def compressImg(self):
        # 显示原始图片文件信息
        oriFileInfotextBrowser = self.ui.oriFileInfotextBrowser
        oriFileInfotextBrowser.setText(getFileInfo(self.imgFilePath))

        # 生成对应的目标文件路径
        self.outFilePath = ''.join(self.imgFilePath.split('.')[0:-1]) + ' Compressed.jpg'
        self.ui.logtextBrowser.setText('')
        # 启用线程进行压缩处理（因为耗时较大
        process = encodeImg.Processthread()
        process._signal.connect(self.writerLog)
        process.run()
        process.encodeimg(self.imgFilePath, self.outFilePath, self.quantity)

        # 显示生成文件信息
        aftFileInfotextBrowser = self.ui.aftFileInfotextBrowser
        aftFileInfotextBrowser.setText(getFileInfo(self.outFilePath))
        showAftImgLabel = self.ui.showAftImgLabel
        # 显示生成图
        jpg = QtGui.QPixmap(self.outFilePath).scaled(showAftImgLabel.width(), showAftImgLabel.height())
        showAftImgLabel.setPixmap(jpg)

    def writerLog(self, s):  # 实时显示处理进度
        self.ui.logtextBrowser.append(s)

        # qt中的一个坑。。。折腾了好久，不使用这个函数的话就无法实时显示添加的内容
        # ref: https://www.it1352.com/2207991.html
        QtCore.QCoreApplication.processEvents()

    def sliderMove(self):  # 绑定压缩质量选择滑块
        quantitylSlider = self.ui.quantitylSlider
        quantityLabel = self.ui.quantityLabel
        self.quantity = quantitylSlider.value()
        quantityLabel.setText(str(self.quantity) + '%')

    def selectImg(self):  # 调用文件资源管理器选择图片并显示
        showOriImgLabel = self.ui.showOriImgLabel
        imgFilePathEdit = self.ui.imgFilePathEdit
        oriFileInfotextBrowser = self.ui.oriFileInfotextBrowser

        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "",
                                                       "Image Files (*.png *.jpg *.bmp);;All Files(*)")
        self.imgFilePath = imgName
        imgFilePathEdit.setText(imgName)
        oriFileInfotextBrowser.setText(getFileInfo(self.imgFilePath))

        jpg = QtGui.QPixmap(imgName).scaled(showOriImgLabel.width(), showOriImgLabel.height())
        showOriImgLabel.setPixmap(jpg)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = MainWindow()
    my.show()
    sys.exit(app.exec_())

# nuitka --standalone --windows-disable-console --include-qt-plugins=sensible,styles --plugin-enable=qt-plugins --enable-plugin=numpy --enable-plugin=pyqt5 --onefile --output-dir=out --windows-icon-from-ico=favicon.ico GUI.py
