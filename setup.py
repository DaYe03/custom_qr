from setuptools import find_packages, setup

setup(
    name='bracodes_generator',
    packages=find_packages(include=['bracodes_generator']),
    version='0.1.0',
    description='Generate any barcode',
    author='Daniele Ye',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==8.2.2'],
    test_suite='tests',
)