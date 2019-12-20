from maya import cmds, OpenMayaUI
from shiboken2 import wrapInstance
from PySide2 import QtWidgets


control_element = cmds.workspaceControl('custom_workspace')
control_widget = OpenMayaUI.MQtUtil.findControl('custom_workspace')
control_wrap = wrapInstance(long(control_widget), QtWidgets.QWidget)

# widgets example to add
button_object = QtWidgets.QPushButton('Test Me')
control_wrap.layout().addWidget(button_object)