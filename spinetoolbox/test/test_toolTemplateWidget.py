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

"""
Unit tests for ToolTemplateWidget class.

:author: M. Marin (KTH)
:date:   8.1.2019
"""

import unittest
from unittest import mock
import logging
import sys
from PySide2.QtWidgets import QApplication
from widgets.tool_template_widget import ToolTemplateWidget
from ui_main import ToolboxUI


class TestToolTemplateWidget(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Overridden method. Runs once before all tests in this class."""
        try:
            cls.app = QApplication().processEvents()
        except RuntimeError:
            pass
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    def setUp(self):
        """Overridden method. Runs before each test. Makes instance of TreeViewForm class.
        """

        # # Set logging level to Error to silence "Logging level: All messages" print
        logging.disable(level=logging.ERROR)  # Disable logging
        toolbox = ToolboxUI()
        self.tool_template_widget = ToolTemplateWidget(toolbox)
        logging.disable(level=logging.NOTSET)  # Enable logging

    def tearDown(self):
        """Overridden method. Runs after each test.
        Use this to free resources after a test if needed.
        """
        self.tool_template_widget = None

    def test_create_minimal_tool_template(self):
        """Test that a minimal tool template can be created by specifying name, type and main program file."""
        with mock.patch("widgets.tool_template_widget.QFileDialog") as mock_file_dialog, \
            mock.patch("widgets.tool_template_widget.ToolTemplateWidget.call_add_tool_template") as mock_add, \
            mock.patch("widgets.tool_template_widget.ToolTemplateWidget.close") as mock_close:
            self.tool_template_widget.ui.comboBox_tooltype.setCurrentIndex(1)
            self.tool_template_widget.ui.lineEdit_name.setText("test_tool")
            self.tool_template_widget.ui.lineEdit_main_program.setText(__file__)
            mock_file_dialog.getSaveFileName.return_value = ['test_tool.json']
            self.tool_template_widget.ui.pushButton_ok.click()
        mock_add.assert_called_once()
        mock_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
