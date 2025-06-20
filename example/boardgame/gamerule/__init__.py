import importlib
from pathlib import Path
from ..gridrule import APPS


def register_all_apps() -> None:
    """自动注册所有节点模块
    遍历nodes目录及其子目录下的所有Python模块文件，动态导入实现自动注册
    """
    package_dir = Path(__file__).parent
    module_paths = (path.relative_to(package_dir) for path in package_dir.glob("**/*.py"))
    for module_path in module_paths:
        module_name = "." + module_path.with_suffix('').as_posix().replace('/', '.')
        importlib.import_module(module_name, package = __package__)


register_all_apps()