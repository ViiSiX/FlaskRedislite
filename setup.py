"""
Flask-Redislite
---------------

Using Flask with Redislite
"""
from setuptools import setup


setup(
    name='Flask-Redislite',
    version='0.0.1',
    url='https://github.com/scattm/FlaskRedislite',
    download_url='https://github.com/scattm/FlaskRedislite',
    license='MIT',
    author='Trong-Nghia Nguyen',
    author_email='ntngh2712@gmail.com',
    maintainer='Trong-Nghia Nguyen',
    maintainer_email='ntngh2712@gmail.com',
    description='Using Flask with Redislite',
    long_description=__doc__,
    py_modules=['flask_redislite'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'redislite'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
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
