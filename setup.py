from setuptools import setup, find_packages

setup(
    name='Browsify',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'PyQtWebEngine',
    ],
    entry_points={
        'console_scripts': [
            'browsify = main:main',
        ],
    },
    author='İlker Özgen, Onurcan Ataç',
    author_email='ilker.ozgen@ug.bilkent.edu.tr, onurcan.atac@ug.bilkent.edu.tr',
    description='Browsify: Effortless browsing, every click counts',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
