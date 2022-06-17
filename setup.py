from setuptools import setup

setup(
    name='ade_nf',
    version='0.1.0',
    author='Henri Hemminki',
    author_email='henri.hemminki@solita.fi',
    description='Notify API CLI for Agile Data Engine',
    url='https://github.com/solita/ade-notify-api-cli',
    project_urls = {
        "Bug Tracker": "https://github.com/solita/ade-notify-api-cli/issues"
    },
    license='MIT',
    packages=['utils', 'commands'],
    py_modules=['ade_nf'],
    install_requires=[
        'Click==8.0.3',
        'requests',
        'wheel',
        'adenotifier @ git+https://github.com/solita/adenotifier.git@v0.1.5#egg=adenotifier'
    ],
    entry_points={
        'console_scripts': [
            'adenf = ade_nf:adenf',
        ],
    },
)

