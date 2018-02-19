import os
import sys

import json

# import Qt
from Qt import QtGui, QtCore, QtWidgets

import maya.cmds as cmds
PLUGIN = 'fbxmaya.mll'

SCRIPT_DIR = os.path.dirname(__file__)
JSON_FILE = "{0}/config.json".format(SCRIPT_DIR)

class fbxUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(fbxUI, self).__init__(parent)
        # self.setModal(False)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("FBX Exporter")

        # main widget ---------------------------------------------------------
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(QtWidgets.QVBoxLayout())

        # Export Locations Layout ---------------------------------------------
        export_location_layout = QtWidgets.QHBoxLayout()

        location_lbl = QtWidgets.QLabel("Export Locations:")
        self.project_combobox = QtWidgets.QComboBox()
        add_location_btn = self._button("+")
        remove_location_btn = self._button("x")

        export_location_layout.addWidget(location_lbl)
        export_location_layout.addWidget(self.project_combobox)
        export_location_layout.addWidget(add_location_btn)
        export_location_layout.addWidget(remove_location_btn)

        # Static Mesh Layout --------------------------------------------------
        sm_export_widget = QtWidgets.QWidget()
        sm_export_widget.setLayout(QtWidgets.QFormLayout())

        sm_layout, self.sm_le, self.sm_sel_btn = self._export_selection(
            'Mesh:')

        sm_name_layout, sm_name = self._export_name('FBX Name:')

        sm_export_bttn = self._button("Export")

        sm_export_widget.layout().addRow(sm_layout)
        sm_export_widget.layout().addRow(sm_name_layout)
        sm_export_widget.layout().addRow(sm_export_bttn)

        # Skeletal Mesh Layout ------------------------------------------------
        sk_export_widget = QtWidgets.QWidget()
        sk_export_widget.setLayout(QtWidgets.QFormLayout())

        skin_layout, self.skin_le, self.skin_sel_btn = self._export_selection(
            'Skin:')
        skel_layout, self.skel_le, self.skel_sel_btn = self._export_selection(
            'Bind Skeleton:')

        sk_name_layout, sk_name = self._export_name('FBX Name:')

        sk_export_bttn = self._button("Export")

        sk_export_widget.layout().addRow(skin_layout)
        sk_export_widget.layout().addRow(skel_layout)
        sk_export_widget.layout().addRow(sk_name_layout)
        sk_export_widget.layout().addRow(sk_export_bttn)

        # Animation Layout ----------------------------------------------------
        anim_widget = QtWidgets.QWidget()
        anim_widget.setLayout(QtWidgets.QFormLayout())

        anim_layout, self.anim_le, self.anim_sel_btn = self._export_selection(
            'Bind Skeleton:')

        anim_frames_layout = QtWidgets.QHBoxLayout()
        anim_start_layout, anim_start_name = self._export_name('Start Frame:')
        anim_end_layout, anim_end_name = self._export_name('End Frame:')

        anim_frames_layout.addLayout(anim_start_layout)
        anim_frames_layout.addLayout(anim_end_layout)

        anim_name_layout, anim_name = self._export_name('FBX Name:')

        anim_export_bttn = self._button("Export")

        anim_widget.layout().addRow(anim_layout)
        anim_widget.layout().addRow(anim_frames_layout)
        anim_widget.layout().addRow(anim_name_layout)
        anim_widget.layout().addRow(anim_export_bttn)

        # Tab layout ----------------------------------------------------------
        export_tabs_widget = QtWidgets.QTabWidget()
        export_tabs_widget.addTab(sm_export_widget, "Static Mesh")
        export_tabs_widget.addTab(sk_export_widget, "Skeletal Mesh")
        export_tabs_widget.addTab(anim_widget, "Animation")

        # Add tabs to central widget ------------------------------------------
        central_widget.layout().addLayout(export_location_layout)
        central_widget.layout().addWidget(export_tabs_widget)

        # sets central widget for PyQt window
        self.setCentralWidget(central_widget)
        self.setFixedSize(self.sizeHint())

        # Button Connections --------------------------------------------------
        add_location_btn.clicked.connect(lambda:
            self.get_directory(export_tabs_widget))
        sm_export_bttn.clicked.connect(self.exportDir)
        sk_export_bttn.clicked.connect(self.exportDir)
        anim_export_bttn.clicked.connect(self.exportDir)

    def get_directory(self, tab_widget):
        '''Create popup file browser and stores path.

        Creates QFileDialog to find and store designated folder
        '''

        dlg = QtWidgets.QFileDialog.getExistingDirectory(
            None, 'Select a folder:', 'C:\\Users\\desktop',
            QtWidgets.QFileDialog.ShowDirsOnly)

        print dlg

        json_data = self.loadJSONConfig()
        print json_data['Export Paths']
        # directory_lbl.setText(dlg)

        if dlg:
            tab_widget.setEnabled(True)
            # print directory_lbl.text()
        else:
            tab_widget.setEnabled(False)
            # print directory_lbl.text()

    def loadJSONConfig(self, configFile=JSON_FILE):
        with open(configFile, 'r') as json_file:
            configData = json.loads(json_file)

            return configData

    def exportDir(self, target_path=None):

        print 'aerasdf'

        # self.exportMA(artSource)
        # self.exportSM(target_path)

    def fillAssetList(self, index):
        print index
        smSelection = self.sm_lbl.text() + "\\" + self.typeOfAsset.itemText(index)
        print smSelection

        if self.fillComboBox:
            self.whichAsset.clear()

        self.fillComboBox(self.whichAsset, smSelection)

    def fillComboBox(self, comboBox, filePath):
        assetPaths = self.getPath(filePath)

        print "Paths:", assetPaths

        for x in assetPaths:
            comboBox.addItem(x)

    def osPath(self, filePath):
        print filePath
        print type(filePath)
        if os.path.isdir(filePath):
            return True
        else:
            return False

    def getPath(self, filePath):
        rootDir = filePath
        if self.osPath(rootDir):
            return os.listdir(rootDir)

    def exportMA(self, directory):
        mayaFilesPath = directory + "\\" + "Maya Files" + "\\"
        path = self.getPath(mayaFilesPath)

        sceneName = cmds.file(query = True, sceneName = True, shortName = True)

        print sceneName

        if not sceneName:
            print "Untitled File"
        else:
            mayaFile = mayaFilesPath + sceneName

        """
        cmds.file(save = True)
        meshes = cmds.ls(sl = True)
        cmds.select(meshes)
        """




    def exportSK(self):
        # This code selects the joints and meshes only.
        meshes = cmds.ls(sl=True)

        # Select the mesh and joints to export
        # Select the mesh and joints to export
        cmds.select(meshes)

        skFilePath = directory + self.whichAsset.currentText() + "\\" + "Meshes" + "\\"
        path = self.getPath(skFilePath)

        sceneName = cmds.file(query=True, sceneName=True, shortName=True)

        fileName = sceneName.split(".")

        print skFilePath + str(fileName[0]) + ".fbx"

        try:
            cmds.FBXResetExport()
            cmds.FBXExportShapes("-v", True)
            # cmds.FBXExportShapes("-q")

            cmds.FBXExportSkins("-v", True)
            # cmds.FBXExportSkins ("-q")

            cmds.FBXExportSmoothingGroups("-v", True)
            # cmds.FBXExportSmoothingGroups("-q")
            cmds.FBXExportTangents("-v", True)
            # cmds.FBXExportTangents("-q")
            cmds.FBXExportSmoothMesh("-v", True)
            # cmds.FBXExportSmoothMesh("-q")
            cmds.FBXExportReferencedAssetsContent("-v", True)
            # cmds.FBXExportReferencedAssetsContent("-q")

            # Connections
            cmds.FBXExportInputConnections("-v", False)
            # cmds.FBXExportInputConnections("-q")

            # Axis Conversion
            cmds.FBXExportUpAxis("y")
            # cmds.FBXExportUpAxis("-q")

            cmds.FBXExportFileVersion("-v", "FBX201400")

            # Export!
            cmds.FBXExportInAscii("-v", True)
            cmds.FBXExport("-f", skFilePath + str(fileName[0]) + ".fbx", "-s")

        except RuntimeError, err:
            print str(err)

    def exportSM(self, directory):

        # This code selects the joints and meshes only.
        meshes = cmds.ls(selection=True)

        for x in meshes:
            if cmds.objectType(x, isType="joint"):
                print "Nope not SM"
            else:

                # Select the mesh and joints to export
                cmds.select(meshes)

                smFilePath = directory + self.whichAsset.currentText() + "\\" + "Meshes" + "\\"
                path = self.getPath(smFilePath)

                sceneName = cmds.file(
                    query=True, sceneName=True, shortName=True)

                fileName = sceneName.split(".")

                print smFilePath + str(fileName[0]) + ".fbx"

                try:
                    cmds.FBXResetExport()
                    cmds.FBXExportShapes("-v", True)
                    # cmds.FBXExportShapes("-q")

                    cmds.FBXExportSmoothingGroups("-v", True)
                    # cmds.FBXExportSmoothingGroups("-q")
                    cmds.FBXExportTangents("-v", True)
                    # cmds.FBXExportTangents("-q")
                    cmds.FBXExportSmoothMesh("-v", True)
                    # cmds.FBXExportSmoothMesh("-q")
                    cmds.FBXExportReferencedAssetsContent("-v", True)
                    # cmds.FBXExportReferencedAssetsContent("-q")

                    # Connections
                    cmds.FBXExportInputConnections("-v", False)
                    # cmds.FBXExportInputConnections("-q")

                    # Axis Conversion
                    cmds.FBXExportUpAxis("y")
                    # cmds.FBXExportUpAxis("-q")

                    cmds.FBXExportFileVersion("-v", "FBX201400")

                    # Export!
                    cmds.FBXExportInAscii("-v", True)
                    cmds.FBXExport("-f", smFilePath + str(fileName[0]) + ".fbx", "-s")

                except RuntimeError, err:
                    print str(err)

    def checkSM(self):
        # This code selects the joints and meshes only.
        meshes = cmds.ls(selection=True)

        selection = ""

        for x in meshes:
            if not cmds.objectType(x, isType="mesh"):
                print str(x) + "cannot be exported as a Static Mesh"
                return False
            else:
                selection = selection + str(x)
                self.sm_lbl.setText(selection)

        return True


    def _export_selection(self, label_name):
        # uv_mesh_layout, child of central_widget -----------------------------
        layout = QtWidgets.QHBoxLayout()

        # lbl = label
        lbl = QtWidgets.QLabel(label_name)
        lbl.setAlignment(QtCore.Qt.AlignCenter)

        # le = line edit
        mesh_le = QtWidgets.QLineEdit(None)
        # self.mesh_le.setPlaceholderText(None)
        mesh_le.setReadOnly(True)
        mesh_le.setMaximumWidth(100)

        selection_btn = self._button('<<')

        layout.addWidget(lbl)
        layout.addWidget(mesh_le)
        layout.addWidget(selection_btn)
        layout.setContentsMargins(0, 0, 0, 0)

        return layout, mesh_le, selection_btn

    def _export_name(self, label_name):

        layout = QtWidgets.QHBoxLayout()

        # lbl = label
        lbl = QtWidgets.QLabel(label_name)
        lbl.setAlignment(QtCore.Qt.AlignCenter)
        mesh_le = QtWidgets.QLineEdit()
        mesh_le.setPlaceholderText('Enter Here')
        mesh_le.setMaximumWidth(100)

        layout.addWidget(lbl)
        layout.addWidget(mesh_le)

        return layout, mesh_le

    def _button(self, button_text):
        button = QtWidgets.QPushButton(button_text)

        width = button.fontMetrics().boundingRect(button_text).width() + 10
        button.setMaximumWidth(width)

        return button

def showUI():
    '''Shows Qt UI and attaches the UI to the main Maya window

    Returns:
        Qt Interface -- Qt UI that executes functionality from
                        controllerLibrary
    '''

    main_window = \
        [o for o in QtWidgets.qApp.topLevelWidgets()
            if o.objectName() == 'MayaWindow'][0]

    ui = fbxUI(main_window)
    ui.show()
    return ui
