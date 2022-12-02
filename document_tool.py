import os

from config_execute import ConfigExecute


class DocumentTool:
    def __init__(self):
        self.config_execute = ConfigExecute()
        self.config = self.config_execute.get_config()
        self.file_prefix = None
        self.file_suffix = None
        self.file_path_name = None

    def read_value(self, name):
        return self.config_execute.read_config(name)

    def get_prefix(self):
        if self.file_prefix is None:
            if self.get_output_config()['enable_out_put_file_prefix']:
                self.file_prefix = self.list_concat(self.get_output_config()['out_put_file_prefix'],
                                                    self.get_output_config()['out_put_file_prefix_split'])
            else:
                self.file_prefix = ''
        return self.file_prefix

    @staticmethod
    def list_concat(str_list, split):
        if split is None:
            split = ''
        result = ''
        for temp in str_list:
            if not (result is ''):
                result += split
            result += temp
        return result

    def get_output_config(self):
        return self.config['output']

    def get_suffix(self):
        if self.file_suffix is None:
            if self.get_output_config()['enable_out_put_file_suffix']:
                self.file_suffix = self.list_concat(self.get_output_config()['out_put_file_suffix'],
                                                    self.get_output_config()['out_put_file_suffix_split'])
            else:
                self.file_suffix = ''
        return self.file_suffix

    def get_file_path_name(self):
        if self.file_path_name is None:
            path_list = self.get_output_config()['out_put_path']
            path_split = self.get_output_config()['out_put_path_split']
            self.file_path_name = self.list_concat(path_list, path_split)
        return self.file_path_name

    def get_file_name(self, name: str) -> str:
        prefix = self.get_prefix()
        suffix = self.get_suffix()
        split_list = name.split('.')
        if len(split_list) > 1:
            ext = split_list[-1]
            split_list.remove(ext)
            return prefix + ''.join(split_list) + suffix + "." + ext
        return prefix + name + suffix

    def execute(self):
        file_name = self.get_file_path_name()
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        pass
