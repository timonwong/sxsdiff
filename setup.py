from setuptools import setup

long_description = open('README.md').read()


setup(
    name='sxsdiff',
    version='0.1.0',
    url='https://github.com/timonwong/sxsdiff',
    license='BSD',
    author='Timon Wong',
    author_email='timon86.wang@gmail.com',
    description='Side by side diff generator for python',
    long_description=long_description,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=['sxsdiff'],
    install_requires=['diff-match-patch']
)
