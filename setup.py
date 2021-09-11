from setuptools import setup

setup(
    name='dnsrecordttl_exporter',
    version='0.1.1',
    package_dir={'': 'src'},
    install_requires=[
        'dnspython',
        'prometheus-client',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'dnsrecordttl_exporter = core.__main__:main',
        ],
    },
)
