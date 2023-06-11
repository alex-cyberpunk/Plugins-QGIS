from .codes_admin import SaveAttributesPlugin
import sys, os
def classFactory(iface):
    return SaveAttributesPlugin(iface)