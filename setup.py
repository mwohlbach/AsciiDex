from setuptools import setup, find_packages

setup(
    name='pythonTemplateProject',
    version='0.1.0',
    description='Template for starting a Python project.',
    long_description='A long description for display on the PyPi description page',
    url='http://github.com/yourname/yourproject.git',
    author='yourname',
    author_email='youremail@domain.com',
    license='GNU',
    classifiers=[
        'Development Status :: Alpha',
        'Intended Audience :: Developers',
        'License :: GNU General Public License',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='example template project',
    packages=find_packages(exclude=['docs', 'tests*']),
    py_modules=['hello '],
    install_requires=[
        'Click'
    ], #dependicies i.e. 'requests'
    package_data={
        'sample': ['package_data.dat']
    },
    data_files=None, #used for anything outside the package directory
    entry_points={
        'console_scripts': [
            'AsciiDex=AsciiDex:cli'
        ]
    }

)