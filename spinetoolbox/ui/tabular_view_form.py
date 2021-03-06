######################################################################################################################
# Copyright (C) 2017 - 2018 Spine project consortium
# This file is part of Spine Toolbox.
# Spine Toolbox is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
# any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# Public License for more details. You should have received a copy of the GNU Lesser General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
######################################################################################################################

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../spinetoolbox/ui/tabular_view_form.ui',
# licensing of '../spinetoolbox/ui/tabular_view_form.ui' applies.
#
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.splitter_3 = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter_3.sizePolicy().hasHeightForWidth())
        self.splitter_3.setSizePolicy(sizePolicy)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter_3)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.comboBox_value_type = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_value_type.setObjectName("comboBox_value_type")
        self.verticalLayout.addWidget(self.comboBox_value_type)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.list_select_class = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.list_select_class.setObjectName("list_select_class")
        self.verticalLayout.addWidget(self.list_select_class)
        self.pushButton_add_object_class = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_add_object_class.setObjectName("pushButton_add_object_class")
        self.verticalLayout.addWidget(self.pushButton_add_object_class)
        self.pushButton_add_relationship_class = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_add_relationship_class.setObjectName("pushButton_add_relationship_class")
        self.verticalLayout.addWidget(self.pushButton_add_relationship_class)
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setOpaqueResize(True)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.list_index = TestListView(self.horizontalLayoutWidget)
        self.list_index.setObjectName("list_index")
        self.verticalLayout_2.addWidget(self.list_index)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.list_column = TestListView(self.horizontalLayoutWidget)
        self.list_column.setObjectName("list_column")
        self.verticalLayout_3.addWidget(self.list_column)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.list_frozen = TestListView(self.horizontalLayoutWidget)
        self.list_frozen.setObjectName("list_frozen")
        self.verticalLayout_4.addWidget(self.list_frozen)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.table_frozen = FrozenTableView(self.verticalLayoutWidget_5)
        self.table_frozen.setObjectName("table_frozen")
        self.verticalLayout_5.addWidget(self.table_frozen)
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.splitter_2)
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.h_layout_filter = QtWidgets.QHBoxLayout()
        self.h_layout_filter.setObjectName("h_layout_filter")
        self.verticalLayout_6.addLayout(self.h_layout_filter)
        self.pivot_table = SimpleCopyPasteTableView(self.verticalLayoutWidget_6)
        self.pivot_table.setObjectName("pivot_table")
        self.verticalLayout_6.addWidget(self.pivot_table)
        self.verticalLayout_7.addWidget(self.splitter_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuSession = QtWidgets.QMenu(self.menubar)
        self.menuSession.setObjectName("menuSession")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionRefresh.setEnabled(True)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionCommit = QtWidgets.QAction(MainWindow)
        self.actionCommit.setEnabled(True)
        self.actionCommit.setObjectName("actionCommit")
        self.actionRollback = QtWidgets.QAction(MainWindow)
        self.actionRollback.setEnabled(True)
        self.actionRollback.setObjectName("actionRollback")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.menuSession.addAction(self.actionRefresh)
        self.menuSession.addAction(self.actionCommit)
        self.menuSession.addAction(self.actionRollback)
        self.menuSession.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSession.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("MainWindow", "Select input type:", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("MainWindow", "Select object/relationship class:", None, -1))
        self.pushButton_add_object_class.setText(QtWidgets.QApplication.translate("MainWindow", "Add object class", None, -1))
        self.pushButton_add_relationship_class.setText(QtWidgets.QApplication.translate("MainWindow", "Add relationship class", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Rows:", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Columns:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Frozen:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Frozen values:", None, -1))
        self.menuSession.setTitle(QtWidgets.QApplication.translate("MainWindow", "Session", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "File", None, -1))
        self.actionRefresh.setText(QtWidgets.QApplication.translate("MainWindow", "Refresh", None, -1))
        self.actionRefresh.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Shift+Return", None, -1))
        self.actionCommit.setText(QtWidgets.QApplication.translate("MainWindow", "Commit", None, -1))
        self.actionCommit.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Return", None, -1))
        self.actionRollback.setText(QtWidgets.QApplication.translate("MainWindow", "Rollback", None, -1))
        self.actionRollback.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Backspace", None, -1))
        self.actionClose.setText(QtWidgets.QApplication.translate("MainWindow", "Close", None, -1))
        self.actionClose.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+W", None, -1))

from widgets.custom_qtableview import FrozenTableView, SimpleCopyPasteTableView
from widgets.custom_qlistview import TestListView
