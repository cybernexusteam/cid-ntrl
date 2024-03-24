import sys
from pathlib import Path
import av_lib
import configparser
import os
from pathlib import Path
import json
import ai

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QListView

QML_IMPORT_NAME = "io.github.cybernexus.ntrl.App.Bridge"
QML_IMPORT_MAJOR_VERSION = 1
@QmlElement
class Bridge(QObject):
    @Slot(str)
    def setApiKey(self, s):
        write_config({
            "apiKey": s
        })
    
    @Slot(result=str)
    def getApiKey(self):
        return get_config("apiKey")
    
    @Slot(str)
    def setPollRate(self, s):
        write_config({
            "pollRate": s
        })
    
    @Slot(result=str)
    def getPollRate(self):
        return get_config("pollRate")
    
    @Slot(str)
    def setScanDir(self, s):
        write_config({
            "scanDir": s
        })
    @Slot(result=str)
    def getScanDir(self):
        return get_config("scanDir")
    @Slot(result=list)
    def getLastScanResult(self):
        return json.loads(get_from_file("config", "scan"))
    @Slot(result=str)
    def scanDirectory(self):
        av_lib.ensure_running()
        out = av_lib.scan_dir(self.getScanDir())
        print(out)
        return json.dumps(out)
    @Slot(str,result=str)
    def promptAi(self, scan_result):
        scan_result = json.loads(scan_result)
        out = list(map(lambda x: (ai.get_resp(x[1], self.getApiKey()), x[0]), scan_result))
        print(out)
        return json.dumps(out)

def get_from_file(section, prop):
    file_path = ""
    if os.name == "posix":
        file_path = os.environ["HOME"] + "/.config/ntrl/ntrl.conf"
    elif os.name == "nt":
        file_path = os.environ["APPDATA"] + "\\ntrl\\ntrl.conf"
    
    config = configparser.ConfigParser()
    config.read(file_path)
    return config.get(section, prop)

def get_config(prop):
    return get_from_file("config", prop)

# writes a dictionary of configs to the config file
def write_config(configs):
    file_path = ""
    if os.name == "posix":
        file_path = os.environ["HOME"] + "/.config/ntrl/ntrl.conf"
    elif os.name == "nt":
        file_path = os.environ["APPDATA"] + "\\ntrl\\ntrl.conf"

    config = configparser.ConfigParser()
    if not os.path.isfile(file_path):
        Path(os.environ["APPDATA"] + "\\ntrl").mkdir(parents=True, exist_ok=True)
        Path(file_path).touch()
        with open("copy.txt", "w") as file:
            config.add_section('config')
            if os.name == "posix":
                config.set("config", "scanDir", os.environ["HOME"] + "/Downloads")
            elif os.name == "nt":
                config.set("config", "scanDir", os.environ["USERPROFILE"] + "\\Downloads")
            config.set("config", "pollRate", "weekly")
            config.set("config", "apiKey", "")
            config.write(file)

    config.read(file_path)
    for key, value in configs.items():
        config.set("config", key, value)
    with open(file_path, "w") as f:
        config.write(f)

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    qml_file = Path(__file__).resolve().parent / "main.qml"
    engine.load(qml_file)
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


