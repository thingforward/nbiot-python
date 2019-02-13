try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='NarrowBand',
    version='0.2.1',
    author='Dominik Fehr',
    author_email='dominik@fe.hr',
    maintainer='Andreas Schmidt',
    maintainer_email='andreas.schmidt@cassini.de',
    packages=['narrowband',],
    url='http://pypi.python.org/pypi/NarrowBand/',
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License',
    description='NarrowBand library',
    long_description=open('README.md').read(),
    install_requires=["pyserial >= 3.4",],
    classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Telecommunications Industry',
    'License :: Other/Proprietary License',
    'Programming Language :: Python', 
    ],
    keywords='nb1 m1 nb-iot iot lte narrowband cat-nb1 cat-m1',
)