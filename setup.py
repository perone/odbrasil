from setuptools import setup
import odbrasil
import sys
import string

def install_requirements():
    with open("requirements.txt", "r") as f:
        reqs = f.readlines()
        return map(string.strip, reqs)

setup(
    name='odbrasil',
    version=odbrasil.__version__,
    url='https://github.com/perone/odbrasil/',
    license='Apache License 2.0',
    author=odbrasil.__author__,
    author_email='christian.perone@gmail.com',
    description='A Python package for retrieving and parsing Brazilian government open data.',
    long_description=open('README.rst').read(),
    packages=['odbrasil'],
    package_dir={'odbrasil': 'odbrasil'},
    keywords='open data, parser, odbrasil, brasil',
    platforms='Any',
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['LICENSE', 'README.rst', 'requirements.txt']},
    install_requires=install_requirements(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)


