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

import logging
import os
import re
from yolk.pypi import CheeseShop

FILENAMES_TO_SEARCH_FOR = \
    ['setup.py', 'dev-requirements.txt', 'test-requirements.txt']


def check_dependencies_file(path_to_file, ignore_this_regex):
    check_file = PythonSetuptoolsDependencyCheckerForFile(
        path_to_file, ignore_this_regex)
    return check_file.check_file()


def check_dependencies_dir(path_to_dir, ignore_this_regex):
    check_dir = PythonSetuptoolsDependencyCheckerForDir(
        path_to_dir, ignore_this_regex)
    return check_dir.check_all_filename_in_subdirs()


def _string_dependency_to_dict(dependency_string):
    """Receives an item from install_requires field
    in the form of ITEMNAME RELATION VERSION
    like pika==0.9.13
    and returns the following dictionary:
    [name, is_locked_to_specific_version, version_locked_to,
    latest version available from pip]"""
    dependency_params = re.split("<|>|=", dependency_string)
    is_locked = False  # better naming
    if "==" in dependency_string:
        is_locked = True
    dependency_name = dependency_params[0]
    version_relation = dependency_string.replace(dependency_name, "")
    dependency_dict = {"name": dependency_name,
                       "is_locked": is_locked,
                       "version_relation": version_relation,
                       "latest_available":
                           get_latest_version_number(dependency_name)}
    return dependency_dict


def get_latest_version_number(package_name):
    """Receives a package name and
    returns the latest version its available in from pip"""
    pkg, all_versions = CheeseShop().query_versions_pypi(package_name)
    if len(all_versions):
        return all_versions[0]
    return None


def _fix_unequal_conditions(string):
    """Makes <> conditions human readable"""
    return string.replace(",<", "<")


def _remove_whitespace_from_equals(string):
    """Receives string and returns it without inline comments"""
    return string.replace(" =", "=").replace("= ", "=")


def _remove_comments(string):
    """Receives string and returns it without inline comments"""
    return re.sub(re.compile("#.*?\n"), "", string)


def _get_file_contents(path_to_file):
    """Receives a path to file and returns its contents as string"""
    contents = None
    try:
        with open(path_to_file, 'r') as f:
            contents = f.read()
    except IOError as ex:
        logging.error("unable to open file {0}".format(path_to_file))
        logging.error(ex)
        return
    return contents


def _filter_list_for_regex(list_of_strings, filter_regex):
    return [string for string in list_of_strings
            if not re.match(re.compile(filter_regex), string)]


def _remove_quotes_and_whitespace_from_list(list_to_remove_whitespace_from):
    return [_remove_quotes_and_whitespace(x) for x in
            list_to_remove_whitespace_from]


def _remove_quotes_and_whitespace(string):
    return string.replace(" ", "").replace(
        "\'", "").replace("\"", "")


class PythonSetuptoolsDependencyCheckerForFile():

    def __init__(self, path_to_file,
                 regex_to_ignore):
        self._path = path_to_file
        self._ignore_this = regex_to_ignore
        self._list_of_dependencies = []
        self._list_of_unprocessed_dependencies = []

    def _get_list_of_versioned_dependencies(self):
        return [x for x in self._list_of_dependencies if x["is_locked"]]

    def _get_list_of_unversioned_dependencies(self):
        return [x for x in self._list_of_dependencies if not x["is_locked"]]

    def _get_plaintext_list(self,file_contents):
        deps = file_contents.split('\n')
        print deps
        for line in file_contents.split('\n'):
            self._list_of_unprocessed_dependencies += line

    def _get_append_list(self, file_contents):
        """Receives a string: file_contents which should be a setup.py file,
        and a string regex: ignore_this
        returns a list of requirements which
        are added via the append clause
        and ignores the ones that match the regex"""
        phrase_start = "install_requires.append("
        while phrase_start in file_contents:
            starts_at = file_contents.find(phrase_start)
            file_contents = file_contents[starts_at + len(phrase_start):]
            ends_at = file_contents.find(")")
            self._list_of_unprocessed_dependencies.append(
                file_contents[:ends_at])
        return self._list_of_unprocessed_dependencies

    def _get_install_requires_field_contents(self, file_contents):
        """Receives a string: file_contents which should be a setup.py file,
        returns a list of requirements which
        are added via the install_requires variable"""
        phrase_start = "install_requires=["
        file_contents = _fix_unequal_conditions(
            _remove_comments(_remove_whitespace_from_equals(
                _remove_quotes_and_whitespace(file_contents))))
        if phrase_start in file_contents:
            file_contents = ''.join(file_contents.splitlines())
            starts_at = file_contents.find(phrase_start)
            file_contents = file_contents[starts_at + len(phrase_start):]
            ends_at = file_contents.find("]")
            file_contents = file_contents[:ends_at]
            self._list_of_unprocessed_dependencies += file_contents.split(",")
        return self._list_of_unprocessed_dependencies

    def _get_dependency_with_latest_version(self, list_of_dependencies):
        """Receives a list of items from install_requires field
        in the form of ITEMNAME RELATION VERSION
        like pika==0.9.13
        and returns the following dictionary per each item:
        {name, is_locked_to_specific_version, version_locked_to,
        version available from pip}
        in a list"""
        return [self.string_dependency_to_dict(dependency)
                for dependency in list_of_dependencies if dependency]

    def _process_dependency_list(self):
        self._list_of_unprocessed_dependencies = \
            _remove_quotes_and_whitespace_from_list(
                self._list_of_unprocessed_dependencies)
        self._list_of_unprocessed_dependencies = _filter_list_for_regex(
            self._list_of_unprocessed_dependencies, self._ignore_this)
        self._list_of_dependencies = \
            [_string_dependency_to_dict(dependency)
             for dependency in self._list_of_unprocessed_dependencies]

    def check_file(self):
        file_contents = _get_file_contents(self._path)
        if self._path.endswith(".py"):
            self._get_append_list(file_contents)
            self._get_install_requires_field_contents(file_contents)
        if not self._path.endswith(".py"):
            self._get_plaintext_list(file_contents)
        self._process_dependency_list()
        return self._list_of_dependencies


class PythonSetuptoolsDependencyCheckerForDir():

    def __init__(self, path_to_recurse, regex_to_ignore):
        self._path = path_to_recurse
        self._ignore_this = regex_to_ignore
        self._result = []

    def check_all_filename_in_subdirs(self):
        """Receives a path and setup filename to search for,
        a field dependency name and regex to ignore
        returns a dict of filename and the list of dependencies it uses,
        whether they are version locked,
        which version and the latest version of the package available on pip
        """
        for root, _, files in os.walk(self._path):
            for f in files:
                if f in FILENAMES_TO_SEARCH_FOR:
                    fullpath = os.path.join(root, f)
                    logging.info("checking file: {0}".format(fullpath))
                    check_file = PythonSetuptoolsDependencyCheckerForFile(
                        fullpath, self._ignore_this)
                    self._result.append({"filename": fullpath,
                                         "analysis": check_file.check_file()})
        return self._result
