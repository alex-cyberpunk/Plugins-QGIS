import pathlib
import sys
import os.path
import pkg_resources
import subprocess
import time
def spin(seconds):
        """Pause for set amount of seconds, replaces time.sleep so program doesn't stall"""
        time_end = time.time() + seconds
        while time.time() < time_end:
            QApplication.processEvents()
def installer_func():
    plugin_dir = os.path.dirname(os.path.realpath(__file__))

    exception = ['scipy', 'numpy', 'et-xmlfile', 'wxPython', 'urllib3', 'toml', 'six', 'sip', 'simplejson', 'setuptools', 'retrying', 'requests', 'PyYAML', 'pywin32', 'pytz', 'python-dateutil', 'PyQt5', 'PyQt5-sip', 'pyproj', 'pypiwin32', 'pyparsing', 'PyOpenGL', 'pyodbc', 'Pygments', 'psycopg2-binary', 'ply', 'plotly', 'pip', 'Pillow', 'pandas', 'packaging', 'OWSLib', 'nose', 'networkx', 'mock', 'matplotlib', 'MarkupSafe', 'kiwisolver', 'Jinja2', 'idna', 'httplib2', 'geographiclib', 'future', 'ExifRead', 'decorator', 'cycler', 'coverage', 'chardet', 'certifi', 'gdal']

    # List comprehension to get the packages
    pack_names = [d for d in pkg_resources.working_set
        if d.project_name not in exception]
    list=[]
    for dist in pack_names:
        list.append(format(dist).split(" ")[0])
    # print the package names and versions
    with open(os.path.join(plugin_dir,'requirements.txt'), "r") as requirements:
            for dep in requirements.readlines():
                dep = dep.strip().split("==")[0]
                if dep not in  list:
                        try :subprocess.check_call(['python', '-m', 'pip', 'install', dep])
                        except ImportError as e:
                            print("{} not available, installing".format(dep))
                        spin(4)