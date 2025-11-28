from setuptools import setup

APP = ['app.py']
DATA_FILES = [('docs', ['docs'])]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['webview'],
    'plist': {
        'CFBundleName': 'Does This Feel Right',
        'CFBundleDisplayName': 'Does This Feel Right',
        'CFBundleGetInfoString': "Thoughts on business, technology, and the human condition",
        'CFBundleIdentifier': "com.doesthisfeelright.app",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': 'Isaac Hernandez'
    },
    'includes': ['webview', 'bottle'],
    'iconfile': None,  # Add path to .icns file if you have one
}

setup(
    app=APP,
    name='Does This Feel Right',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
