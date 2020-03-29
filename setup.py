from setuptools import setup, find_packages

setup(
    name='twst',
    version='0.1',
    description='Stock data vs Twitter data website',
    author='Alessandro Angioi',
    author_email='alessandro.angioi@hotmail.com',
    packages=find_packages(),
    install_requires=['flask', 'tweepy', 'finnhub'],
)
