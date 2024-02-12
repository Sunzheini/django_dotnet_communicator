import clr
import sys
import os


class DllRunner:
    """
    This class is used to register dlls and import classes from the corresponding namespaces.
    You can then use the classes as attributes of the DllRunner object.
    """
    def __init__(self):
        self.dll_folder_path = None

    def register_dll(self, dll_name, dll_folder_path=None):
        """
        Register the dll name and adds the path to the dll folder to the sys.path
        :param dll_name: name of the dll must be usable by python, not i.e. "09.Some text", but
        "Festo.AST.Testrunner.Interfaces.NFCL" or "System.Windows.Forms"
        :param dll_folder_path: path to the dll folder, where the dll is located
        """
        if dll_folder_path is not None:
            self.dll_folder_path = dll_folder_path
            dll_path = os.path.abspath(self.dll_folder_path)
            sys.path.append(dll_path)

        clr.AddReference(dll_name)

    def handle_imports(self, *args):
        """
        Imports classes from the corresponding namespaces
        :param args: it is a list of dictionaries, where the key is the namespace and the value is a list of classes
        The name of the namespace must be something like "Festo.AST.Testrunner.Interfaces".
        The name of the class must be something like "Device" and it must be public. Can also be a static class.
        """
        # Internal method to import classes
        for arg in args:
            for namespace, classes in arg.items():
                for class_name in classes:
                    exec(f"from {namespace} import {class_name}")
                    setattr(self, class_name, eval(class_name))

    @staticmethod
    def translate_python_list_to_dotnet_generic_list(python_list, type_of_list):
        """
        Translates a Python list to a .NET List<T>
        Example:
        dotnet_device_list = runner.translate_python_list_to_dotnet_generic_list(
                [runner.Device('id1', '1', '1'), runner.Device('id2', '2', '2')],
                runner.Device
            )
        :param type_of_list: the type of the list, i.e. list of objects of type Device
        :param python_list: Python list
        :return: .NET List<T>
        """
        dotnet_list = clr.System.Collections.Generic.List[type_of_list]()
        [dotnet_list.Add(item) for item in python_list]
        return dotnet_list
