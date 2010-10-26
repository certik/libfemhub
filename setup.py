from distutils.core import setup

setup(
    name='libfemhub',
    version="0.1",
    license='BSD',
    author='hp-FEM group at UNR',
    packages=[
        'femhub',
        'femhub.examples',
        ],
    package_data = {
        'femhub.examples': ['data/domain*'],
        }
)
