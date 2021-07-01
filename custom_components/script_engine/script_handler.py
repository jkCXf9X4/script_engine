
import os
import fnmatch
import logging
import runpy
import importlib
import inspect
import re

from .misc import ListHelp

# importing to globals for access in scripts
# from .engine import Engine
# from .decorator import *


class Script_info:
    def __init__(self):
        self.path = None
        self.filenmae = None
        self.module_name = None
        self.class_object = None
        self._class = None
        self.script_function_objects = None
        self.script_functions = None
        self.non_script_functions_object = None
        self.non_script_functions = None

class Script_handler:

    def __init__(self, path) -> None:
        self.path = path
        self.scripts = []
        self.logger = logging.getLogger(__name__)

    def find_files(self, pattern) -> None:
        def init_script(path, file):
            script = Script_info()
            script.path = os.path.join(path, file)
            script.filenmae = file
            script.module_name = file.split(".")[0]
            return script

        scripts = [init_script(self.path, name) for name in os.listdir(self.path)]

        self.scripts = [f for f in scripts if fnmatch.fnmatch(f.filenmae, pattern)]

    def extract_script_classes(self):
        def extract_class(script: Script_info):
            module = importlib.import_module(script.module_name)
            members = {i[0]: i[1] for i in inspect.getmembers(module, inspect.isclass)}
            script.class_object = members[script.module_name]

        _ = [extract_class(i) for i in self.scripts]

    def instantiate_script_classes(self, *arg, **kwarg):
        def instantiate_class(script: Script_info):
            script._class = script.class_object(*arg, **kwarg)

        _ = [instantiate_class(i) for i in self.scripts]

    def extract_script_functions(self, pattern):

        def is_script_function(func):
            return re.match(pattern, func.__name__) != None

        def extract_function(script: Script_info):
            attrs = [getattr(script._class, name) for name in dir(script._class) if name[0:1] != "_"]
            functions = [attr for attr in attrs if inspect.ismethod(attr)]
            script.script_function_objects, script.non_script_functions_object = ListHelp.split_list(functions, is_script_function)

            self.logger.info(f"Class: {script.class_object.__name__}")
            self.logger.info(f"Extracted functions: {' '.join([i.__name__ for i in script.script_function_objects])}")
            self.logger.debug(f"Not Extracted: {' '.join([i.__name__ for i in script.non_script_functions_object])}")

        _ = [extract_function(i) for i in self.scripts]

    def instantiate_script_functions(self, *args, **kwargs):
        def instantiate_functions(script: Script_info):
            script.function_results = [func(*args, **kwargs) for func in script.script_function_objects]

            self.logger.debug(f"Instantiate status: {script.function_results}")

        _ = [instantiate_functions(i) for i in self.scripts]