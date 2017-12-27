from setuptools import setup

setup(
    name='snipshue',
    version='1.0',
    description='Philips Hue skill for Snips',
    author='Snips Labs',
    author_email='labs@snips.ai',
    url='https://github.com/snipsco/snips-skill-hue',
    download_url='',
    license='MIT',
    install_requires=[
        'requests==2.6.0',
        'funcsigs==1.0.2',
        'mock==2.0.0',
        'pbr==3.1.1',
        'six==1.11.0'
    ],
    test_suite="tests",
    keywords=['snips'],
    package_data={'snipshue': ['Snipsspec']},
    packages=['snipshue'],
    include_package_data=True
)
