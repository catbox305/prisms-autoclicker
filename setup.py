from setuptools import setup

NAME = "lion's autoclicker"
VERSION = "3.1"

plist = {
    "CFBundleIconFile": NAME,
    "CFBundleName": NAME,
    "CFBundleShortVersionString": VERSION,
    "CFBundleGetInfoString": " ".join([NAME, VERSION]),
    "CFBundleExecutable": NAME,
}

setup(
   
    app=["lion's autoclicker.py"],
    setup_requires=["pynput",],
    options={
        "py2app": {
            "arch": "arm64",
            "build-type": "standalone"
        }
    },
)