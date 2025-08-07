from setuptools import setup, find_packages

setup(
    name="toolbox_installer_cli",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "inquirer",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'toolbox=toolbox_installer.cli:main',
        ],
    },
)
