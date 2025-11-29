from setuptools import setup
import os
import glob

APP = ['app.py']

# Collect all files from docs directory recursively
DATA_FILES = []
for root, dirs, files in os.walk('docs'):
    if files:
        # Remove 'docs/' prefix to place files at the root of Resources
        target_dir = root.replace('docs', '', 1).lstrip('/')
        file_paths = [os.path.join(root, f) for f in files]
        DATA_FILES.append((target_dir, file_paths))
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
    'iconfile': 'icon.icns',
}

setup(
    app=APP,
    name='Does This Feel Right',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
