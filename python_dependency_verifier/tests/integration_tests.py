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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############

import unittest
from python_dependency_verifier import python_dependency_verifier


class TestDependencies(unittest.TestCase):

    def runTest(self):
        pass

    def test_check_file(self):
        return self.assertEqual(
            python_dependency_verifier.check_dependencies_file(
                "../../setup.py", "cloudify.*"),
            [{'is_locked': True, 'name': 'yolk',
                'latest_available': '0.4.3', 'version_relation': '==0.4.3'}])

    def test_check_dir(self):
        return self.assertEqual(
            python_dependency_verifier.check_dependencies_dir(
                "../../", "cloudify.*"),
            [{'filename': "../../setup.py", 'analysis':
                [{'is_locked': True, 'name': 'yolk',
                  'latest_available': '0.4.3',
                  'version_relation': '==0.4.3'}]}])


newTest = TestDependencies().test_check_file()
newTest = TestDependencies().test_check_dir()
