
import QtQuick 2.6
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.0
import QtQuick.Controls.Universal 2.0
import QtCore
import io.github.cybernexus.ntrl.App.Bridge 1.0
import QtQuick.Dialogs

ApplicationWindow {
    id : window
    width : 1000
    height : 600
    visible : true
    title : "App"
    Bridge {
        id : bridge
    }
    Rectangle {
        anchors.fill : parent
        Gradient {
            GradientStop {
                position : 0
                color : "#ffffff"
            }
            GradientStop {
                position : 1
                color : "#c1bbf9"
            }
        }
    }
    Popup {
        id : settingsPopup
        x : 100
        y : 100
        width : 200
        height : 300
        modal : true
        focus : true
        closePolicy : Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
        ColumnLayout {
            Label {
                text : "OpenAI api key:"
            }
            TextField {
                id : apiKeyInput
                text : bridge.getApiKey()
                echoMode : TextInput.Password
                placeholderText : qsTr("Enter OpenAI API Key")
            }
            ColumnLayout {
                RadioButton {
                    id : weekly
                    Component.onCompleted : {
                        weekly.checked = bridge.getPollRate() == "weekly"
                    }
                    text : qsTr("weekly")
                }
                RadioButton {
                    id : daily
                    Component.onCompleted : {
                        daily.checked = bridge.getPollRate() == "daily"
                    }
                    text : qsTr("daily")
                }
                RadioButton {
                    id : monthly
                    Component.onCompleted : {
                        monthly.checked = bridge.getPollRate() == "monthly"
                    }
                    text : qsTr("monthly")
                }
            }
            MenuItem {
                text : qsTr("Open...")
                onTriggered : folderDialog.open()
            }
            FolderDialog {
                id : folderDialog
                currentFolder : StandardPaths.standardLocations(StandardPaths.HomeLocation)[0
                ]
                selectedFolder : bridge.getScanDir() || StandardPaths.standardLocations(StandardPaths.HomeLocation)[0
                ]
            }
            RowLayout {
                Button {
                    text : "Exit"
                    onClicked : {
                        settingsPopup.close()
                    }
                }
                Button {
                    text : "Save"
                    onClicked : {
                        function urlToPath(urlString) {
                            var s
                            if (urlString.startsWith("file:///")) {
                                var k = urlString.charAt(9) === ':'
                                    ? 8
                                    : 7
                                s = urlString.substring(k)
                            } else {
                                s = urlString
                            }
                            return decodeURIComponent(s)
                        }
                        if (urlToPath(folderDialog.selectedFolder.toString()) !== "") {
                            bridge.setScanDir(urlToPath(folderDialog.selectedFolder.toString()))
                        }
                        bridge.setApiKey(apiKeyInput.text)
                        if (weekly.checked) {
                            bridge.setPollRate("weekly")
                        } else if (daily.checked) {
                            bridge.setPollRate("daily")
                        } else if (monthly.checked) {
                            bridge.setPollRate("monthly")
                        }
                    }
                }
            }
        }
    }
    Settings {
        id : settings
        property string style : "Default"
    }
    StackView {
        id : stack
        anchors.fill : parent
        initialItem : homeGrid
        Rectangle {
            anchors.fill : parent
            color : "#8E05C2"
        }
        Pane {
            id : home
            anchors.fill : parent
            property var cellHeight: 240
            property var cellWidth: 240
            property var maxPerLine: homeGrid.model.count
            property var minWidthToSwitch: 0
            onWidthChanged : {
                var margin = 0
                if (home.width < cellWidth) {
                    margin = 0
                }
                else if (home.width / cellWidth < maxPerLine) {
                    margin = home.width % cellWidth
                }
                else {
                    margin = home.width - cellWidth * maxPerLine
                }
                homeGrid.anchors.leftMargin = margin / 2
                homeGrid.anchors.rightMargin = margin / 2
            }
            GridView {
                id : homeGrid
                anchors.fill : parent
                cellHeight: home.cellHeight
                cellWidth: home.cellWidth
                boundsBehavior : Flickable.StopAtBounds
                delegate : Item {
                    height : GridView.view.cellHeight
                    width : GridView.view.cellWidth
                    Button {
                        height : parent.height * 0.8
                        width : parent.width * 0.8
                        anchors.bottom : parent.bottom // Trying to make a column on right
                        anchors.horizontalCenter : parent.horizontalCenter
                        text : model.title
                        background : Rectangle {
                            color : "#8E05C2" // Set button color here
                            radius : 20 // Set button corner radius here
                        }
                        contentItem : Text {
                            text : parent.text
                            color : "white" // Set text color here
                            horizontalAlignment : Text.AlignHCenter
                            verticalAlignment : Text.AlignVCenter
                            font.pixelSize : 18
                        }
                        onClicked : {
                            stack.push(Qt.resolvedUrl(page))
                        }
                    }
                }
                model : ListModel {
                    ListElement {
                        title : "File Scan Status"
                        page : "FileScan-page.qml"
                    }
                    ListElement {
                        title : "Security checks: "
                        page : ""
                    }
                    ListElement {
                        title : "test"
                        page : ""
                    }
                }
            }
        }
    }
    header : ToolBar {
        Material.foreground : "white"
        RowLayout {
            spacing : 20
            anchors.fill : parent
            ToolButton {
                contentItem : Image {
                    fillMode : Image.Pad
                    horizontalAlignment : Image.AlignHCenter
                    verticalAlignment : Image.AlignVCenter
                    source : "./assets/icons8-hamburger-30.webp"
                }
                onClicked : drawer.open()
            }
            Label {
                id : titleLabel
                text : "Dashboard"
                font.pixelSize : 20
                elide : Label.ElideRight
                horizontalAlignment : Qt.AlignHCenter
                verticalAlignment : Qt.AlignVCenter
                Layout.fillWidth : true
            }
            ToolButton {
                contentItem : Image {
                    fillMode : Image.Pad
                    horizontalAlignment : Image.AlignHCenter
                    verticalAlignment : Image.AlignVCenter
                    source : "./assets/icons8-settings-30_copy.webp"
                }
                onClicked : optionsMenu.open()
                Menu {
                    id : optionsMenu
                    x : parent.width - width
                    transformOrigin : Menu.TopRight
                    MenuItem {
                        text : "Settings"
                        onTriggered : settingsPopup.open()
                    }
                    MenuItem {
                        text : "About"
                        onTriggered : aboutDialog.open()
                    }
                }
            }
        }
    }
    Drawer {
        id : drawer
        width : Math.min(window.width, window.height) / 3 * 2
        height : window.height
        ListView {
            id : listView
            currentIndex : -1
            anchors.fill : parent
            delegate : ItemDelegate {
                width : parent.width
                text : model.title
                highlighted : ListView.isCurrentItem
                onClicked : {
                    if (model.title === "Dashboard") { // Return to the original screen
                        stack.clear()
                        stack.push(home)
                    } else if (listView.currentIndex != index) {
                        listView.currentIndex = index
                        titleLabel.text = model.title
                        stack.replace(model.source)
                    }
                    drawer.close()
                }
            }
            model : ListModel {
                ListElement {
                    title : "Dashboard"
                    source : "Dashboard-page.qml"
                }
                ListElement {
                    title : "File Scanner"
                    source : "FileScan-page.qml"
                }
                ListElement {
                    title : "Security Check"
                    source : ""
                }
                ListElement {
                    title : "Firewall Config"
                    source : ""
                }
                ListElement {
                    title : "Net Analysis"
                    source : ""
                }
            }
            ScrollIndicator.vertical : ScrollIndicator {}
        }
    }
}
