try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name': 'zinescape',
    'author': 'Thaddeus Hughes',
    'author_email': 'hughes.thad@gmail.com',
    'version': '1.0-rc',
    'install_requires': ['pypdf', 'argparse'],
    'packages': ['zinescape'],

    'entry_points': {
        'console_scripts': {
            'zinescape = zinescape.zinescape:cli'
        }
    }
}

setup(**config)