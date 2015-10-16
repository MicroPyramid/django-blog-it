import os
from setuptools import setup
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
PROJECT_NAME = 'micro_blog'

data_files = []
for dirpath, dirnames, filenames in os.walk(PROJECT_NAME):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        continue
    elif filenames:
        for f in filenames:
            data_files.append(os.path.join(
                dirpath[len(PROJECT_NAME) + 1:], f))

setup(
    name='micro-blog',
    version='0.0.3',
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    description='A simple installable app for writing blog posts',
    long_description=README,
    url='https://github.com/MicroPyramid/micro-blog.git',
    author='Micropyramid',
    author_email='hello@micropyramid.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'boto',
        'Django',
        'django-simple-pagination',
        'django-storages',
        'Pillow',
        'requests',
        'wheel'
    ],
)