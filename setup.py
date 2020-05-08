from setuptools import find_packages, setup

setup(
    name='dnsrecordttl_exporter',
    version='0.1',
    packages=find_packages('src'),
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
