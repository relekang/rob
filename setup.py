from setuptools import setup, find_packages


setup(
    name="rob",
    version='0.1.0',
    description='Make python objects persistent with Redis.',
    url='http://github.com/relekang/rob',
    author='Rolf Erik Lekang',
    packages=find_packages(),
    install_requires=[
        'redis',
    ]
)
