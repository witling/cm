from setuptools import find_packages, setup

setup(
    name='cm',
    version='0.0.1',
    description='a discord bot that runs quasicode',
    packages=find_packages(),
    package_data={
        'lang': ['*.json']
    },
    include_package_data=True,
    install_requires=[
        'discord.py',
        'quasicode'
    ],
    entry_points={'console_scripts': ['cm=cm.__main__:main']}
)
