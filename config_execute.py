import logging
import re

import yaml


class ConfigExecute:
    def __init__(self):
        self.config = None
        self.log = logging.getLogger()

    def get_config(self):
        if self.config is None:
            with open("config.yaml", encoding='utf8') as a_yaml_file:
                # 解析yaml
                config = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
                self.config = config
        return self.config

    def read_config(self, source: str) -> str:
        value = source
        match = self.match_placeholder(value)
        while not (match is None):
            placeHolder = match.group()
            readKey = self.read_key(placeHolder)
            value = value.replace(placeHolder, readKey)
            match = self.match_placeholder(value)
        return value

    @staticmethod
    def match_placeholder(string):
        par = re.compile('\${.*?}')
        match = par.match(string)
        return match

    def read_key(self, key):
        source = key
        if not isinstance(key, str):
            return source
        key = key.lstrip().rstrip()
        if len(source) == 0:
            return source

        if key.startswith("${") and key.endswith("}"):
            key = key.lstrip("${")
            key = key.rstrip("}")
            keys = key.split(".")
            try:
                temp = self.config
                for tempKey in keys:
                    temp = temp[tempKey]
                return temp
            except Exception:
                self.log.error("config template key error, key: %s" % source)
                return source
        return key
