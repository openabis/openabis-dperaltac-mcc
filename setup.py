from distutils.core import setup

setup(
    name='openabis-dperaltac-mcc',
    version='0.0.1',
    packages=['openabis_dperaltac_mcc'],
    url='https://github.com/newlogic42/openabis-dperaltac-mcc',
    license='Apache 2.0',
    author='newlogic42',
    author_email='',
    description='OpenAbis\' plugin implementation of dperaltac/MCC',
    install_requires=[
        'cffi==1.13.1'
    ],
    package_data={
        '': ['*.so'],
    }
)
