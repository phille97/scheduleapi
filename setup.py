import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "scheduleapi",
    version = "0.0.1",
    author = "Philip Johansson (https://github.com/phille97)",
    description = (
        "Someday there will be descriptive text here about this project."
    ),
    license = "MIT",
    keywords = "time schedule time-management",
    url = "https://github.com/phille97/scheduleapi",
    packages=['scheduleapi', 'tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Topic :: Office/Business :: Scheduling",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'Flask',
        'Flask-Security',
        'Flask-Bootstrap',
        'PyYAML',
        'pony',
    ]
)
