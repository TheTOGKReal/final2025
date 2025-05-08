import maya.cmds as cmds
from maya import OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

def parent_and_snap():
    selection = cmds.ls(selection=True)

    if len(selection) < 2:
        QtWidgets.QMessageBox.warning(
            get_maya_main_window(),
            "Foolish :)",
            "Make at least two selections, then try again!"
        )
        return

    parent = selection[0]
    children = selection[1:]

    for child in children:
        # Snap translation and rotation
        pos = cmds.xform(parent, q=True, ws=True, t=True)
        rot = cmds.xform(parent, q=True, ws=True, ro=True)
        cmds.xform(child, ws=True, t=pos)
        cmds.xform(child, ws=True, ro=rot)

        # Parent it
        cmds.parent(child, parent)

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class ParentSnapTool(QtWidgets.QDialog):
    def __init__(self, parent=get_maya_main_window()):
        super(ParentSnapTool, self).__init__(parent)
        self.setWindowTitle("Parent & Snap Tool")
        self.setFixedSize(300, 100)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.build_ui()

    def build_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        instructions = QtWidgets.QLabel("Make at least two selections, then slap the button!")
        instructions.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(instructions)

        btn = QtWidgets.QPushButton("Let's parent!")
        btn.clicked.connect(parent_and_snap)
        layout.addWidget(btn)

def show_tool():
    for widget in QtWidgets.QApplication.allWidgets():
        if isinstance(widget, ParentSnapTool):
            widget.close()
    tool = ParentSnapTool()
    tool.show()

# Run this to open the window:
show_tool()