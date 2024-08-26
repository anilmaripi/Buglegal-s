from setuptools import setup, find_packages

version = '0.1'

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='worktridev',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'worktridev = worktridev.manage:main',
        ],
    },
)