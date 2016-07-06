"""
Flask-Redislite
---------------

Using Flask with Redislite
"""
import io
from sys import version
from setuptools import setup

with io.open('README.rst', encoding='utf-8') as f:
    description = f.read()
with io.open('HISTORY.rst', encoding='utf-8') as f:
    description += "\n\n%s" % f.read()


assert int(version[0]) >= 2 and int(version[2]) > 6


setup(
    name='Flask-Redislite',
    version='0.0.4',
    url='https://github.com/scattm/FlaskRedislite',
    download_url='https://github.com/scattm/FlaskRedislite',
    license='MIT',
    author='Trong-Nghia Nguyen',
    author_email='ntngh2712@gmail.com',
    maintainer='Trong-Nghia Nguyen',
    maintainer_email='ntngh2712@gmail.com',
    description='Using Flask with Redislite',
    long_description=description,
    py_modules=['flask_redislite'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'redislite',
        'redis-collections',
        'rq'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
