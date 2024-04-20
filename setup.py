from setuptools import setup

NAME = "prism's autoclicker"
VERSION = "4.0"

plist = {
    "CFBundleIconFile": NAME,
    "CFBundleName": NAME,
    "CFBundleShortVersionString": VERSION,
    "CFBundleGetInfoString": " ".join([NAME, VERSION]),
    "CFBundleExecutable": NAME,
}

setup(
   
    app=["prism's autoclicker.py"],
    setup_requires=["pynput"],
    options={
        "py2app": {
            "arch": "x86_64",
			"includes": ["pickle","threading","time"],
			"packages": ["pynput"]
        }
    }
)