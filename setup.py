########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from setuptools import setup

setup(
    name='python-dependency-verifier',
    version='0.1',
    author='Gil Zellner',
    author_email='gil@gigaspaces.com',
    packages=['python_dependency_verifier'],
    license='LICENSE',
    description='A tool to make sure that all dependencies in a python project are version locked and up to date',
    zip_safe=False,
    install_requires=['yolk'],
    entry_points={}
)
