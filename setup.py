from setuptools import setup
setup(
    name='skogscrape',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'skogscrape=skogscrape:run'
        ]
    }
)