from setuptools import setup, find_packages

setup(
    name='custom_qr',
    version='0.9.4',
    author='Daniele Ye',
    author_email='daniele.ye03@gmail.com',
    description='Generate and customize QR codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/DaYe03/custom_qr.git',
    packages=find_packages(),
    install_requires=['numpy', 'opencv-python'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
