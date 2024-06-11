import setuptools

with open('README.org') as readme:
    long_description = readme.read()

setuptools.setup(
    name='gdb_fortran_tools',
    version='0.0.1',
    author='Ken Mankoff',
    author_email='mankoff@gmail.com',
    url='https://github.com/mankoff/gdb_fortran_tools',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib'],
    python_requires='>=3',
    description='Plotting and exporting of variables from GDB for FORTRAN programmers',
    long_description=long_description,
    long_description_content_type='text/org',
    keywords=['gdb', 'debug'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Debuggers'
    ]
)
