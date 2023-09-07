from flask import current_app
import os
import shutil
import json


class SettingUtil:
    def __init__(self, config):
        self.config: dict = config

    def check_exit(self):
        file_path = self.config.get("SETTING_FILE")
        return os.path.exists(file_path)

    def load_setting(self):
        if not self.check_exit():
            shutil.copy(os.path.join(os.path.abspath("./setting"), "setting.json"), self.config.get("SETTING_FILE"))
        file_path = self.config.get("SETTING_FILE")
        with open(file_path, "r") as f:
            data = f.read()
            setting = json.loads(data)
            return setting
