import configparser
import os
import time
from dataclasses import dataclass

path = 'utils/config/config.ini'


def create_config():

    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "token")
    config.set("Settings", "bot_login", "0")
    config.set("Settings", "admin_group", "0:1")
    config.set("Settings", "admin_id", "0:1")
    config.set("Settings", "group_link", "")
    config.set("Settings", "arbitr_link", "0")
    config.set("Settings", "group_id", "0")
    config.set("Settings", "ref_percent", "0")
    config.set("Settings", "qiwi_number", "0")
    config.set("Settings", "qiwi_token", "0")
    config.set("Settings", "min_sum_deal", "0")
    config.set("Settings", "com_witch", "0")
    config.set("Settings", "min_witch", "0")
    config.set("Settings", "secret_key", "0")
    config.set("Settings", "min_bank", "0")

    with open(path, "w") as config_file:
        config.write(config_file)


@dataclass
class ConfigDatabase:
    protocol: str = "sqlite"
    file_name: str = "data/database.db"
    user: str = None
    password: str = None
    host: str = None
    port: str = None

    def get_db_url(self):
        if self.protocol == "sqlite":
            return f"{self.protocol}://{self.file_name}"
        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}"

    def get_config(self):
        return {
            "connections": {"default": self.get_db_url()},
            "apps": {
                "models": {
                    "models": ["data.functions.user", "data.functions.blacklist",
                               "data.functions.withdrawl", "data.functions.deals",
                               "data.functions.deposit", "data.functions.channel", "aerich.models"],
                    "default_connection": "default",
                },
            },
        }


@dataclass
class Config:
    database: ConfigDatabase


def check_config_file():
    if not os.path.exists(path):
        create_config()
        
        print('Config created')
        time.sleep(3)
        exit(0)


def config(what):
    config = configparser.ConfigParser()
    config.read(path)

    value = config.get("Settings", what)

    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path)

    config.set("Settings", setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)


check_config_file()
