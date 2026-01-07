import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='extract-html-diff',
    version='0.1.0',
    author='Konstantin Lopuhin',
    author_email='kostia.lopuhin@gmail.com',
    description='Extract difference between two html pages',
    license='MIT',
    url='https://github.com/TeamHG-Memex/extract-html-diff',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'lxml',
    ],
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
