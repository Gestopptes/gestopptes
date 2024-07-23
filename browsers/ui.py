import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def import_submodules(package, recursive=True, ignore=[]):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    import importlib
    import pkgutil
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        if full_name in ignore:
            continue
        try:
            log.info("importing %s", full_name)
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def start_ui():
    import_submodules("src.ui")
    log.info("import finished.")
    import hyperdiv as hd
    from src.ui.main import ui_main
    hd.run(ui_main)

    
if __name__ == "__main__":
    start_ui()