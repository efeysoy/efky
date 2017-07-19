from distutils.core import setup, Extension

module1 = Extension('cpu_info',
                    libraries = ['libgtop-2.0'],
                    sources = ['cpu_load.c'])

setup(
    name='efky',
    version='',
    packages=[''],
    url='',
    license='',
    author='efeyucesoy',
    author_email='',
    description='',
    ext_modules = [module1]
)
