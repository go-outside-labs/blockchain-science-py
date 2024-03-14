from setuptools import setup, find_packages

setup(
    name="cointbot",
    version='0.1.4',
    packages=find_packages(include=[
        'src', 
        'src.markets', 
        'src.utils', 
        'src.strategies', 
        'src.bots']),
    author="Mia Stein",
    install_requires=['python-dotenv'],
    entry_points={
        'console_scripts': ['cointbot=src.main:run']
    },
)