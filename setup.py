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
        'Flask==0.10.*',
        'Flask-SQLAlchemy==2.0',
        'Flask-Security==1.7.*',
        'Flask-Login==0.3.*',
        'Flask-Bootstrap==3.3.*',
        'Flask-Babel==0.9.*',
        'Flask-WTF==0.12.*',
        'flask_restful==0.3.*',
        'flask-debugtoolbar==0.10.*',
        'WTForms==2.0.*',
        'WTForms-JSON==0.2.*',
        'PyYAML==3.11.*',
        'psycopg2==2.6.*',
        'passlib==1.6.*',
    ]
)
