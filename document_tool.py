import os

import docx_execute

from constant import base_path
from config_execute import ConfigExecute


class DocumentTool:
    def __init__(self):
        self.config_execute = ConfigExecute()
        self.config = self.config_execute.get_config()
        self.file_prefix = None
        self.file_suffix = None
        self.file_path_name = None
        self.template_path = None
        self.template_file_list = None
        self.docx_list = None
        self.execl_list = None

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
            if result != '':
                result += split
            result += temp
        return result

    def get_output_config(self):
        return self.config['output']

    def get_output(self, name):
        return self.get_output_config() + "/" + name

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
        self.mk_file_path()
        self.execute_docx()
        self.execute_execl()
        pass

    def mk_file_path(self):
        file_name = self.get_file_path_name()
        if not os.path.exists(file_name):
            os.mkdir(file_name)

    def execute_execl(self):

        pass

    def execute_docx(self):
        template_list = self.get_docx_template_list()
        for template in template_list:
            content = self.get_docx_content(template)
            docx_execute.exec_docx(self.get_template_path() + "/" + template, self.get_output(template), content)

    def get_template_path(self):
        if self.template_path is None:
            path = self.config['input']['template_path']
            if path is None or path == '':
                path = './template'
            self.template_path = path
        return self.template_path

    def get_template_file_list(self):
        if self.template_file_list is None:
            path = base_path + '/' + self.get_template_path()
            self.template_file_list = os.listdir(path)
        return self.template_file_list

    def get_docx_template_list(self):
        if self.docx_list is None:
            file_list = self.get_template_file_list()
            docx_list = []
            for file in file_list:
                if (not file.startswith("~")) and file.endswith(".docx"):
                    docx_list.append(file)
            self.docx_list = docx_list
        return self.docx_list

    def get_docx_content(self, file_name: str) -> dict:
        docx_dicts = {}
        global_config = self.config['global']
        global_docx_config = self.config['docx']['global']
        if not (global_config is None):
            for k, v in global_config.items():
                docx_dicts[k] = self.read_value(v)
        if not (global_docx_config is None):
            for k, v in global_docx_config.items():
                docx_dicts[k] = self.read_value(v)
        docx_config = global_docx_config[file_name.replace(".docx", "")]
        if not (docx_config is None):
            for k, v in docx_config.items():
                docx_dicts[k] = self.read_value(v)
        return docx_dicts

    def get_execl_template_list(self):
        if self.execl_list is None:
            file_list = self.get_template_file_list()
            execl_list = []
            for file in file_list:
                if (not file.startswith("~")) and file.endswith(".xlsx"):
                    execl_list.append(file)
            self.execl_list = execl_list
        return self.execl_list
