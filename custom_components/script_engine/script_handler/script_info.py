from .class_info import ClassInfo

class ScriptInfo:
    def __init__(self):
        self.path = None
        self.filename = None
        self.module_name = None
        self.class_info_objects: ClassInfo = None
