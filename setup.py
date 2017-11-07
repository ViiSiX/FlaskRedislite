"""
Flask-Redislite
---------------

Using Flask with Redislite
"""
import re
import io
from setuptools import setup

with io.open('README.rst', encoding='utf-8') as f:
    description = f.read()
with io.open('HISTORY.rst', encoding='utf-8') as f:
    description += "\n\n%s" % f.read()

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('flask_redislite.py', 'rb') as f:
    version = str(_version_re.search(f.read().decode('utf-8')).group(1)).replace('\'', '')

setup(
    name='Flask-Redislite',
    version=version,
    url='https://github.com/ViiSiX/FlaskRedislite',
    download_url='https://github.com/ViiSiX/FlaskRedislite',
    license='MIT',
    author='Trong-Nghia Nguyen',
    author_email='nghia@viisix.space',
    maintainer='Trong-Nghia Nguyen',
    maintainer_email='nghia@viisix.space',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
