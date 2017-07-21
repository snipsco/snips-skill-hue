from setuptools import setup

setup(
    name='snipshue',
    version='0.1.0',
    description='Philips Hue skill for Snips',
    author='Michael Fester',
    author_email='michael.fester@gmail.com',
    url='https://github.com/snipsco/snips-skill-hue',
    download_url='',
    license='MIT',
    install_requires=['requests==2.6.0'],
    test_suite="tests",
    keywords=['snips'],
    packages=[
        'snipshue'
    ]
)
