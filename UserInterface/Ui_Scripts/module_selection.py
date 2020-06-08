# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\PROG\AnimeScraper\UserInterface\Source\module_selection.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModuleSelectionWindow(object):
    def setupUi(self, ModuleSelectionWindow):
        ModuleSelectionWindow.setObjectName("ModuleSelectionWindow")
        ModuleSelectionWindow.resize(274, 340)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ModuleSelectionWindow.sizePolicy().hasHeightForWidth())
        ModuleSelectionWindow.setSizePolicy(sizePolicy)
        self.module_selection = QtWidgets.QWidget(ModuleSelectionWindow)
        self.module_selection.setObjectName("module_selection")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.module_selection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.module_selection_tab = QtWidgets.QTabWidget(self.module_selection)
        self.module_selection_tab.setObjectName("module_selection_tab")
        self.tab_pixiv = QtWidgets.QWidget()
        self.tab_pixiv.setObjectName("tab_pixiv")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_pixiv)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.pixiv_config = QtWidgets.QGroupBox(self.tab_pixiv)
        self.pixiv_config.setObjectName("pixiv_config")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.pixiv_config)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.pixiv_config_show = QtWidgets.QPushButton(self.pixiv_config)
        self.pixiv_config_show.setObjectName("pixiv_config_show")
        self.gridLayout_7.addWidget(self.pixiv_config_show, 0, 0, 1, 1)
        self.pixiv_config_save = QtWidgets.QPushButton(self.pixiv_config)
        self.pixiv_config_save.setObjectName("pixiv_config_save")
        self.gridLayout_7.addWidget(self.pixiv_config_save, 1, 0, 1, 1)
        self.pixiv_config_load = QtWidgets.QPushButton(self.pixiv_config)
        self.pixiv_config_load.setObjectName("pixiv_config_load")
        self.gridLayout_7.addWidget(self.pixiv_config_load, 2, 0, 1, 1)
        self.verticalLayout_5.addWidget(self.pixiv_config)
        self.pixiv_status = QtWidgets.QGroupBox(self.tab_pixiv)
        self.pixiv_status.setObjectName("pixiv_status")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.pixiv_status)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.pixiv_status_current = QtWidgets.QLabel(self.pixiv_status)
        self.pixiv_status_current.setObjectName("pixiv_status_current")
        self.gridLayout_6.addWidget(self.pixiv_status_current, 0, 0, 1, 1)
        self.pixiv_status_current_l = QtWidgets.QLabel(self.pixiv_status)
        self.pixiv_status_current_l.setObjectName("pixiv_status_current_l")
        self.gridLayout_6.addWidget(self.pixiv_status_current_l, 0, 1, 1, 1)
        self.pixiv_status_show_detail = QtWidgets.QPushButton(self.pixiv_status)
        self.pixiv_status_show_detail.setObjectName("pixiv_status_show_detail")
        self.gridLayout_6.addWidget(self.pixiv_status_show_detail, 1, 0, 1, 2)
        self.verticalLayout_5.addWidget(self.pixiv_status)
        self.module_selection_tab.addTab(self.tab_pixiv, "")
        self.tab_pixiv_fast = QtWidgets.QWidget()
        self.tab_pixiv_fast.setObjectName("tab_pixiv_fast")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_pixiv_fast)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pixiv_fast_config = QtWidgets.QGroupBox(self.tab_pixiv_fast)
        self.pixiv_fast_config.setObjectName("pixiv_fast_config")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.pixiv_fast_config)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pixiv_fast_config_show = QtWidgets.QPushButton(self.pixiv_fast_config)
        self.pixiv_fast_config_show.setObjectName("pixiv_fast_config_show")
        self.gridLayout_8.addWidget(self.pixiv_fast_config_show, 0, 0, 1, 1)
        self.pixiv_fast_config_save = QtWidgets.QPushButton(self.pixiv_fast_config)
        self.pixiv_fast_config_save.setObjectName("pixiv_fast_config_save")
        self.gridLayout_8.addWidget(self.pixiv_fast_config_save, 1, 0, 1, 1)
        self.pixiv_fast_config_load = QtWidgets.QPushButton(self.pixiv_fast_config)
        self.pixiv_fast_config_load.setObjectName("pixiv_fast_config_load")
        self.gridLayout_8.addWidget(self.pixiv_fast_config_load, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.pixiv_fast_config)
        self.pixiv_fast_status = QtWidgets.QGroupBox(self.tab_pixiv_fast)
        self.pixiv_fast_status.setObjectName("pixiv_fast_status")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.pixiv_fast_status)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.pixiv_fast_status_current_l = QtWidgets.QLabel(self.pixiv_fast_status)
        self.pixiv_fast_status_current_l.setObjectName("pixiv_fast_status_current_l")
        self.gridLayout_9.addWidget(self.pixiv_fast_status_current_l, 0, 0, 1, 1)
        self.pixiv_fast_status_current = QtWidgets.QLabel(self.pixiv_fast_status)
        self.pixiv_fast_status_current.setObjectName("pixiv_fast_status_current")
        self.gridLayout_9.addWidget(self.pixiv_fast_status_current, 0, 1, 1, 1)
        self.pixiv_fast_status_show_detail = QtWidgets.QPushButton(self.pixiv_fast_status)
        self.pixiv_fast_status_show_detail.setObjectName("pixiv_fast_status_show_detail")
        self.gridLayout_9.addWidget(self.pixiv_fast_status_show_detail, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.pixiv_fast_status)
        self.module_selection_tab.addTab(self.tab_pixiv_fast, "")
        self.tab_danbooru = QtWidgets.QWidget()
        self.tab_danbooru.setObjectName("tab_danbooru")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_danbooru)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.danbooru_config = QtWidgets.QGroupBox(self.tab_danbooru)
        self.danbooru_config.setObjectName("danbooru_config")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.danbooru_config)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.danbooru_config_show = QtWidgets.QPushButton(self.danbooru_config)
        self.danbooru_config_show.setObjectName("danbooru_config_show")
        self.gridLayout_12.addWidget(self.danbooru_config_show, 0, 0, 1, 1)
        self.danbooru_config_save = QtWidgets.QPushButton(self.danbooru_config)
        self.danbooru_config_save.setObjectName("danbooru_config_save")
        self.gridLayout_12.addWidget(self.danbooru_config_save, 1, 0, 1, 1)
        self.danbooru_config_load = QtWidgets.QPushButton(self.danbooru_config)
        self.danbooru_config_load.setObjectName("danbooru_config_load")
        self.gridLayout_12.addWidget(self.danbooru_config_load, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.danbooru_config)
        self.danbooru_status = QtWidgets.QGroupBox(self.tab_danbooru)
        self.danbooru_status.setObjectName("danbooru_status")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.danbooru_status)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.danbooru_status_current_l = QtWidgets.QLabel(self.danbooru_status)
        self.danbooru_status_current_l.setObjectName("danbooru_status_current_l")
        self.gridLayout_13.addWidget(self.danbooru_status_current_l, 0, 0, 1, 1)
        self.danbooru_status_current = QtWidgets.QLabel(self.danbooru_status)
        self.danbooru_status_current.setObjectName("danbooru_status_current")
        self.gridLayout_13.addWidget(self.danbooru_status_current, 0, 1, 1, 1)
        self.danbooru_status_show_detail = QtWidgets.QPushButton(self.danbooru_status)
        self.danbooru_status_show_detail.setObjectName("danbooru_status_show_detail")
        self.gridLayout_13.addWidget(self.danbooru_status_show_detail, 1, 0, 1, 2)
        self.verticalLayout_2.addWidget(self.danbooru_status)
        self.module_selection_tab.addTab(self.tab_danbooru, "")
        self.tab_gelbooru = QtWidgets.QWidget()
        self.tab_gelbooru.setObjectName("tab_gelbooru")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_gelbooru)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gelbooru_config = QtWidgets.QGroupBox(self.tab_gelbooru)
        self.gelbooru_config.setObjectName("gelbooru_config")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.gelbooru_config)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gelbooru_config_show = QtWidgets.QPushButton(self.gelbooru_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gelbooru_config_show.sizePolicy().hasHeightForWidth())
        self.gelbooru_config_show.setSizePolicy(sizePolicy)
        self.gelbooru_config_show.setObjectName("gelbooru_config_show")
        self.gridLayout_14.addWidget(self.gelbooru_config_show, 0, 0, 1, 1)
        self.gelbooru_config_save = QtWidgets.QPushButton(self.gelbooru_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gelbooru_config_save.sizePolicy().hasHeightForWidth())
        self.gelbooru_config_save.setSizePolicy(sizePolicy)
        self.gelbooru_config_save.setObjectName("gelbooru_config_save")
        self.gridLayout_14.addWidget(self.gelbooru_config_save, 1, 0, 1, 1)
        self.gelbooru_config_load = QtWidgets.QPushButton(self.gelbooru_config)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gelbooru_config_load.sizePolicy().hasHeightForWidth())
        self.gelbooru_config_load.setSizePolicy(sizePolicy)
        self.gelbooru_config_load.setObjectName("gelbooru_config_load")
        self.gridLayout_14.addWidget(self.gelbooru_config_load, 2, 0, 1, 1)
        self.verticalLayout_7.addWidget(self.gelbooru_config)
        self.gelbooru_status = QtWidgets.QGroupBox(self.tab_gelbooru)
        self.gelbooru_status.setObjectName("gelbooru_status")
        self.gridLayout_15 = QtWidgets.QGridLayout(self.gelbooru_status)
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.gelbooru_status_current_l = QtWidgets.QLabel(self.gelbooru_status)
        self.gelbooru_status_current_l.setObjectName("gelbooru_status_current_l")
        self.gridLayout_15.addWidget(self.gelbooru_status_current_l, 0, 0, 1, 1)
        self.gelbooru_status_current = QtWidgets.QLabel(self.gelbooru_status)
        self.gelbooru_status_current.setObjectName("gelbooru_status_current")
        self.gridLayout_15.addWidget(self.gelbooru_status_current, 0, 1, 1, 1)
        self.gelbooru_status_show_detail = QtWidgets.QPushButton(self.gelbooru_status)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gelbooru_status_show_detail.sizePolicy().hasHeightForWidth())
        self.gelbooru_status_show_detail.setSizePolicy(sizePolicy)
        self.gelbooru_status_show_detail.setObjectName("gelbooru_status_show_detail")
        self.gridLayout_15.addWidget(self.gelbooru_status_show_detail, 1, 0, 1, 2)
        self.verticalLayout_7.addWidget(self.gelbooru_status)
        self.module_selection_tab.addTab(self.tab_gelbooru, "")
        self.verticalLayout.addWidget(self.module_selection_tab)
        self.configuration_group = QtWidgets.QGroupBox(self.module_selection)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configuration_group.sizePolicy().hasHeightForWidth())
        self.configuration_group.setSizePolicy(sizePolicy)
        self.configuration_group.setObjectName("configuration_group")
        self.gridLayout = QtWidgets.QGridLayout(self.configuration_group)
        self.gridLayout.setObjectName("gridLayout")
        self.configuration_dir = QtWidgets.QLineEdit(self.configuration_group)
        self.configuration_dir.setObjectName("configuration_dir")
        self.gridLayout.addWidget(self.configuration_dir, 0, 1, 1, 1)
        self.configuration_dir_browse = QtWidgets.QPushButton(self.configuration_group)
        self.configuration_dir_browse.setObjectName("configuration_dir_browse")
        self.gridLayout.addWidget(self.configuration_dir_browse, 0, 2, 1, 1)
        self.configuration_dir_l = QtWidgets.QLabel(self.configuration_group)
        self.configuration_dir_l.setObjectName("configuration_dir_l")
        self.gridLayout.addWidget(self.configuration_dir_l, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.configuration_group)
        ModuleSelectionWindow.setCentralWidget(self.module_selection)
        self.statusbar = QtWidgets.QStatusBar(ModuleSelectionWindow)
        self.statusbar.setObjectName("statusbar")
        ModuleSelectionWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ModuleSelectionWindow)
        self.module_selection_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ModuleSelectionWindow)

    def retranslateUi(self, ModuleSelectionWindow):
        _translate = QtCore.QCoreApplication.translate
        ModuleSelectionWindow.setWindowTitle(_translate("ModuleSelectionWindow", "Module Selection"))
        self.pixiv_config.setTitle(_translate("ModuleSelectionWindow", "Module Configuration (PIXIV)"))
        self.pixiv_config_show.setText(_translate("ModuleSelectionWindow", "Show Configuration"))
        self.pixiv_config_save.setText(_translate("ModuleSelectionWindow", "Save Configuration"))
        self.pixiv_config_load.setText(_translate("ModuleSelectionWindow", "Load Prexisting Configuration"))
        self.pixiv_status.setTitle(_translate("ModuleSelectionWindow", "Status"))
        self.pixiv_status_current.setText(_translate("ModuleSelectionWindow", "Current Status:"))
        self.pixiv_status_current_l.setText(_translate("ModuleSelectionWindow", "Stopped"))
        self.pixiv_status_show_detail.setText(_translate("ModuleSelectionWindow", "View Details"))
        self.module_selection_tab.setTabText(self.module_selection_tab.indexOf(self.tab_pixiv), _translate("ModuleSelectionWindow", "Pixiv"))
        self.pixiv_fast_config.setTitle(_translate("ModuleSelectionWindow", "Module Configuration (PIXIV FAST)"))
        self.pixiv_fast_config_show.setText(_translate("ModuleSelectionWindow", "Show Configuration"))
        self.pixiv_fast_config_save.setText(_translate("ModuleSelectionWindow", "Save Configuration"))
        self.pixiv_fast_config_load.setText(_translate("ModuleSelectionWindow", "Load Prexisting Configuration"))
        self.pixiv_fast_status.setTitle(_translate("ModuleSelectionWindow", "Status"))
        self.pixiv_fast_status_current_l.setText(_translate("ModuleSelectionWindow", "Current Status:"))
        self.pixiv_fast_status_current.setText(_translate("ModuleSelectionWindow", "Stopped"))
        self.pixiv_fast_status_show_detail.setText(_translate("ModuleSelectionWindow", "View Details"))
        self.module_selection_tab.setTabText(self.module_selection_tab.indexOf(self.tab_pixiv_fast), _translate("ModuleSelectionWindow", "Pixiv Fast"))
        self.danbooru_config.setTitle(_translate("ModuleSelectionWindow", "Module Configuration (DANBOORU)"))
        self.danbooru_config_show.setText(_translate("ModuleSelectionWindow", "Show Configuration"))
        self.danbooru_config_save.setText(_translate("ModuleSelectionWindow", "Save Configuration"))
        self.danbooru_config_load.setText(_translate("ModuleSelectionWindow", "Load Prexisting Configuration"))
        self.danbooru_status.setTitle(_translate("ModuleSelectionWindow", "Status"))
        self.danbooru_status_current_l.setText(_translate("ModuleSelectionWindow", "Current Status:"))
        self.danbooru_status_current.setText(_translate("ModuleSelectionWindow", "Stopped"))
        self.danbooru_status_show_detail.setText(_translate("ModuleSelectionWindow", "View Details"))
        self.module_selection_tab.setTabText(self.module_selection_tab.indexOf(self.tab_danbooru), _translate("ModuleSelectionWindow", "Danbooru"))
        self.gelbooru_config.setTitle(_translate("ModuleSelectionWindow", "Module Configuration (GELBOORU)"))
        self.gelbooru_config_show.setText(_translate("ModuleSelectionWindow", "Show Configuration"))
        self.gelbooru_config_save.setText(_translate("ModuleSelectionWindow", "Save Configuration"))
        self.gelbooru_config_load.setText(_translate("ModuleSelectionWindow", "Load Prexisting Configuration"))
        self.gelbooru_status.setTitle(_translate("ModuleSelectionWindow", "Status"))
        self.gelbooru_status_current_l.setText(_translate("ModuleSelectionWindow", "Current Status:"))
        self.gelbooru_status_current.setText(_translate("ModuleSelectionWindow", "Stopped"))
        self.gelbooru_status_show_detail.setText(_translate("ModuleSelectionWindow", "View Details"))
        self.module_selection_tab.setTabText(self.module_selection_tab.indexOf(self.tab_gelbooru), _translate("ModuleSelectionWindow", "Gelbooru"))
        self.configuration_group.setTitle(_translate("ModuleSelectionWindow", "Configuration"))
        self.configuration_dir_browse.setText(_translate("ModuleSelectionWindow", "Browse"))
        self.configuration_dir_l.setText(_translate("ModuleSelectionWindow", "Config Folder"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ModuleSelectionWindow = QtWidgets.QMainWindow()
    ui = Ui_ModuleSelectionWindow()
    ui.setupUi(ModuleSelectionWindow)
    ModuleSelectionWindow.show()
    sys.exit(app.exec_())
