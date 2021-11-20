from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.1"
DESCRIPTION = "For cow disease detection"
# LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="cow_disease_detection",
    version=VERSION,
    author="Hussnain Ali",
    author_email="<hassnainali89383@gmail.com>",
    description=DESCRIPTION,
    # long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pandas", "numpy", "gspread", "gspread-dataframe", "pytest"],
    keywords=["python", "video", "stream", "video stream", "camera stream", "sockets"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
