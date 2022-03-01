# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(840, 600)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setStyleSheet(u"background-color:rgb(230, 230, 230)")
        self.widget = QWidget(self.centralWidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 350, 600))
        self.widget.setStyleSheet(u"background-color: rgb(50, 67, 71);")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 54, 12))
        self.label.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.imgFilePathEdit = QLineEdit(self.widget)
        self.imgFilePathEdit.setObjectName(u"imgFilePathEdit")
        self.imgFilePathEdit.setGeometry(QRect(10, 30, 271, 31))
        self.imgFilePathEdit.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.compressButton = QPushButton(self.widget)
        self.compressButton.setObjectName(u"compressButton")
        self.compressButton.setGeometry(QRect(10, 140, 331, 31))
        self.compressButton.setStyleSheet(u"background-color: rgb(50, 67, 71);\n"
                                          "color: rgb(255, 255, 255);")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 80, 54, 12))
        self.label_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.quantitylSlider = QSlider(self.widget)
        self.quantitylSlider.setObjectName(u"quantitylSlider")
        self.quantitylSlider.setGeometry(QRect(10, 110, 271, 22))
        self.quantitylSlider.setValue(50)
        self.quantitylSlider.setOrientation(Qt.Horizontal)
        self.quantityLabel = QLabel(self.widget)
        self.quantityLabel.setObjectName(u"quantityLabel")
        self.quantityLabel.setGeometry(QRect(310, 110, 31, 16))
        self.quantityLabel.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 180, 161, 191))
        self.groupBox.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.oriFileInfotextBrowser = QTextBrowser(self.groupBox)
        self.oriFileInfotextBrowser.setObjectName(u"oriFileInfotextBrowser")
        self.oriFileInfotextBrowser.setGeometry(QRect(10, 20, 141, 161))
        self.oriFileInfotextBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                                  "color: rgb(0, 0, 0);")
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(180, 180, 161, 191))
        self.groupBox_2.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.aftFileInfotextBrowser = QTextBrowser(self.groupBox_2)
        self.aftFileInfotextBrowser.setObjectName(u"aftFileInfotextBrowser")
        self.aftFileInfotextBrowser.setGeometry(QRect(10, 20, 141, 161))
        self.aftFileInfotextBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                                  "color: rgb(0, 0, 0);")
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 380, 331, 211))
        self.groupBox_3.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.logtextBrowser = QTextBrowser(self.groupBox_3)
        self.logtextBrowser.setObjectName(u"logtextBrowser")
        self.logtextBrowser.setGeometry(QRect(10, 20, 201, 181))
        self.logtextBrowser.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
                                          "color: rgb(0, 0, 0);")
        self.openFilePathButton = QPushButton(self.groupBox_3)
        self.openFilePathButton.setObjectName(u"openFilePathButton")
        self.openFilePathButton.setGeometry(QRect(214, 20, 111, 23))
        self.plainTextEdit = QPlainTextEdit(self.groupBox_3)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(220, 50, 101, 121))
        self.plainTextEdit.setReadOnly(True)
        self.githubButton = QPushButton(self.groupBox_3)
        self.githubButton.setObjectName(u"githubButton")
        self.githubButton.setGeometry(QRect(220, 180, 101, 23))
        self.selectImgButton = QPushButton(self.widget)
        self.selectImgButton.setObjectName(u"selectImgButton")
        self.selectImgButton.setGeometry(QRect(290, 30, 51, 31))
        self.selectImgButton.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.groupBox_4 = QGroupBox(self.centralWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(360, 10, 471, 281))
        self.showOriImgLabel = QLabel(self.groupBox_4)
        self.showOriImgLabel.setObjectName(u"showOriImgLabel")
        self.showOriImgLabel.setGeometry(QRect(10, 20, 446, 251))
        self.groupBox_5 = QGroupBox(self.centralWidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(360, 310, 471, 281))
        self.showAftImgLabel = QLabel(self.groupBox_5)
        self.showAftImgLabel.setObjectName(u"showAftImgLabel")
        self.showAftImgLabel.setGeometry(QRect(10, 20, 446, 251))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JPEG COMPRESSOR", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u8def\u5f84\uff1a", None))
        self.imgFilePathEdit.setText("")
        self.imgFilePathEdit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", u"\u56fe\u50cf\u6587\u4ef6\u7684\u7edd\u5bf9\u8def\u5f84...",
                                       None))
        self.compressButton.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u538b\u7f29", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u538b\u7f29\u7ea7\u522b\uff1a", None))
        self.quantityLabel.setText(QCoreApplication.translate("MainWindow", u"50%", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u6587\u4ef6\uff1a", None))
        self.oriFileInfotextBrowser.setHtml(QCoreApplication.translate("MainWindow",
                                                                       u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                                       "p, li { white-space: pre-wrap; }\n"
                                                                       "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6587\u4ef6\u8def\u5f84\uff1a</p>\n"
                                                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6587\u4ef6\u5927\u5c0f\uff1a</p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u521b\u5efa\u65f6\u95f4\uff1a</p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; marg"
                                                                       "in-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4fee\u6539\u65f6\u95f4\uff1a</p></body></html>",
                                                                       None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u6587\u4ef6\uff1a", None))
        self.aftFileInfotextBrowser.setHtml(QCoreApplication.translate("MainWindow",
                                                                       u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                                       "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                                       "p, li { white-space: pre-wrap; }\n"
                                                                       "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6587\u4ef6\u8def\u5f84\uff1a</p>\n"
                                                                       "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6587\u4ef6\u5927\u5c0f\uff1a</p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u521b\u5efa\u65f6\u95f4\uff1a</p>\n"
                                                                       "<p style=\" margin-top:0px; margin-bottom:0px; marg"
                                                                       "in-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u4fee\u6539\u65f6\u95f4\uff1a</p></body></html>",
                                                                       None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7\uff1a", None))
        # if QT_CONFIG(tooltip)
        self.logtextBrowser.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.logtextBrowser.setHtml(QCoreApplication.translate("MainWindow",
                                                               u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                               "p, li { white-space: pre-wrap; }\n"
                                                               "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                               "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">...</p></body></html>",
                                                               None))
        self.openFilePathButton.setText(
            QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u751f\u6210\u8def\u5f84", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow",
                                                                   u"\u672c\u7a0b\u5e8f\u9002\u7528\u4e8e\u521d\u6b65\u538b\u7f29\u4ee5\u65e0\u635f\u683c\u5f0f\u50a8\u5b58\u7684\u56fe\u50cf\u6587\u4ef6\uff08\u5982BMP\uff0cPNG\uff09\u5e76\u4ee5JPG\u683c\u5f0f\u50a8\u5b58",
                                                                   None))
        self.githubButton.setText(QCoreApplication.translate("MainWindow", u"Github ", None))
        self.selectImgButton.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u56fe\uff1a", None))
        self.showOriImgLabel.setText(
            QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u56fe\u50cf\u663e\u793a\u533a\u57df", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u56fe\uff1a", None))
        self.showAftImgLabel.setText(
            QCoreApplication.translate("MainWindow", u"\u751f\u6210\u56fe\u50cf\u663e\u793a\u533a\u57df", None))
    # retranslateUi
