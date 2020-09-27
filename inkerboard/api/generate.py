""" Implement the hello command.

"""
import importlib
from inkerboard.core.image import EpaperImage
from inkerboard.core.logger import logger
from inkerboard.core.config import config
from inkerboard.utils.icons import Icons

def dynamic_load_module(module_type: str) -> object:
    try:
        module = importlib.import_module(f'inkerboard.modules.{module_type.lower()}')
        class_ = getattr(module, module_type)
        return class_()
    except ModuleNotFoundError:
        module = importlib.import_module(f'inkerboard.modules.notification')
        class_ = getattr(module, 'Notification')
        return class_('Invalid Module Selected', Icons.EXCLAMATION)

def main() -> int:
    modules = []
    for module in config.generate.modules:
        modules.append(dynamic_load_module(module).render())

    test = EpaperImage(modules)

    test.render().show()
    return 0

