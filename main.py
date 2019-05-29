#!/usr/bin/env python3
import os
import argparse

class VsCode ():
    # Default extensions
    extensions = {
        "visualstudioexptteam.vscodeintellicode",
        "xyz.local-history",
        "eamodio.gitlens",
        "aaron-bond.better-comments",
        "streetsidesoftware.code-spell-checker",
        "hookyqr.beautify",
        "alefragnani.project-manager",
        "auchenberg.vscode-browser-preview"
    }
    installed_extensions = []
    def __init__(self, extensions=[]):
        if (self.lang_extensions):
            self.extensions.update(self.lang_extensions)
        if (self.platform_extensions):
            self.extensions.update(self.platform_extensions)

        if len(VsCode.installed_extensions) == 0:
            self.fetch_installed_extensions()
    def install(self):
        if (self.extensions == None):
            raise Exception('You are not provided extensions')
        for ext in self.extensions:
            if (not self.check_installed_extensions(ext)):
                os.system("code --install-extension " + str(ext))
            else:
                print(str(ext) + " is already exists")
    def install_extensions(self, extensions=[]):
        for ext in extensions:
            if (not self.check_installed_extensions(ext)):
                os.system("code --install-extension " + str(ext))
            else:
                print(str(ext) + " is already exists")
    def exclude(self, extensions=[]):
        for extension in extensions:
            self.extensions.discard(extension)
    def fetch_installed_extensions(self):
        extensions = os.popen('code --list-extensions').read()
        VsCode.installed_extensions = list(map(lambda item: item.lower(), extensions.split("\n")))
    def check_installed_extensions(self, extension):
        try:
            VsCode.installed_extensions.index(extension)
            return True
        except ValueError:
            return False

class JS (VsCode):
    lang_extensions = {
        "dbaeumer.jshint",
        "ms-vscode.vscode-typescript-tslint-plugin",
        "msjsdiag.debugger-for-chrome",
        "coenraads.bracket-pair-colorizer"
    }
    def __init__(self):
        super().__init__()

class PY (VsCode):
    lang_extensions = {
        "ms-python.python"
    }
    def __init__(self):
        super().__init__()
        self.extensions.update(self.lang_extensions)

class Django (PY):
    platform_extensions = {}
    def __init__(self):
        super().__init__()

class React (JS):
    platform_extensions = {}
    def __init__(self):
        super().__init__()

class Vue (JS):
    platform_extensions = {}
    def __init__(self):
        super().__init__()

class Node (JS):
    platform_extensions = {}
    def __init__(self):
        super().__init__()

class Factory():
    platforms = []
    result = []
    def __init__(self, platoforms):
        self.platforms = platoforms
    def build(self):
        self.find_subclasses(VsCode.__subclasses__())
        return self.result
    def find_subclasses(self, subclasses):
        for _class in subclasses:
            try:
                index = self.platforms.index(_class.__name__.lower())
                self.result.append(_class())
            except ValueError:
                pass
            if len(_class.__subclasses__()) != 0:
                self.find_subclasses(_class.__subclasses__())

parser = argparse.ArgumentParser(description='')
parser.add_argument('-p', '--platforms', help='Please provide platform names', nargs='+', required=True)
parser.add_argument('-i', '--include', help='Include desired extensions', nargs='+')
parser.add_argument('-e', '--exclude', help='Exclude desired extensions', nargs='+')

args = parser.parse_args()
platforms = Factory(args.platforms).build()

for platform in platforms:
    if args.exclude is not None: platform.exclude(args.exclude)
    platform.install()
if args.include is not None: platform.install_extensions(args.include)
