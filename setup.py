from setuptools import setup

NAME = "prism's utilities"
VERSION = "3.2"

plist = {
    "CFBundleIconFile": NAME,
    "CFBundleName": NAME,
    "CFBundleShortVersionString": VERSION,
    "CFBundleGetInfoString": " ".join([NAME, VERSION]),
    "CFBundleExecutable": NAME,
}

setup(
   
    app=["prism's utilities.py"],
    setup_requires=["pynput",],
    options={
        "py2app": {
            "arch": "arm64",
            "build-type": "standalone"
        }
    },
)