from .codes_admin import SaveAttributesPlugin

def classFactory(iface):
    return SaveAttributesPlugin(iface)