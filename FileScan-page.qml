import QtQuick
import QtQuick.Controls
import io.github.cybernexus.ntrl.App.Bridge 1.0
import QtQuick.Layouts

ColumnLayout {
    Button {
        Bridge {
            id: scanBridge
        }
        text: "start scan"
        onClicked: {
            result.text = "loading..."
            let malware = JSON.parse(scanBridge.scanDirectory())
            console.log(malware)
            let ai_stuff = JSON.parse(scanBridge.promptAi(JSON.stringify(malware)))
            console.log(ai_stuff)
            result.text = JSON.stringify(ai_stuff)
        }
    }
    TextArea {
        id: result
        text: ""
        wrapMode: TextEdit.WordWrap
        width: 10000
    }
}
