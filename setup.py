from setuptools import setup, find_packages

setup(
    name='mathprogvis',
    version='0.0.0',
    description='visualize 2d/3d polytopes, compute some common formulations',
    packages=find_packages(exclude=['tests*']),
    install_requires=['matplotlib', 'numpy', 'pycddlib', 'scipy'],
)
