# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='BYCEPS',
    version='0.0',
    description='the Bring-Your-Computer Event Processing System',
    author='Jochen "Y0Gi" Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/',
    license='Modified BSD',
    packages=['byceps'],
    tests_require=['nose2'],
    test_suite='nose2.collector.collector',
)
