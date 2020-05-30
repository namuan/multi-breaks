from setuptools import setup

APP_NAME = "MultiBreaks"
APP = ['multi-breaks.py']
DATA_FILES = ['data']

OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Improving health by taking breaks",
        'CFBundleIdentifier': "dev.deskriders.multibreaks",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2020, Deskriders Dev, All Rights Reserved",
        'LSUIElement': True,
    },
    'packages': ['rumps'],
    'iconfile': 'app.icns',
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
