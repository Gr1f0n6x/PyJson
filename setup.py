from setuptools import setup

setup(
    name='pyjson',
    version='0.1',
    description='Library which helps map user defined classes to json',
    author='Ryanov Nikita',
    author_email='ryanov.nikita@gmail.com',
    url='https://github.com/Gr1f0n6x/PyJson',
    packages=[
        'pyjson', 'pyjson.core'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
)
