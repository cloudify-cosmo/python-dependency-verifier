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

import os
import re
from yolk.pypi import CheeseShop


def fix_unequal_conditions(string):
    return string.replace(",<", "<")


def remove_comments(string):
    """
    :param string:
    :return:
    """
    return re.sub(re.compile("#.*?\n"), "", string)


def get_file_contents(path_to_file):
    return open(path_to_file).read()


def get_append_list(file_contents, ignore_this):
    list_of_appended_requirements = []
    while "install_requires.append(" in file_contents:
        starts_at = file_contents.find("install_requires.append(")
        file_contents = file_contents[starts_at + 24:]
        ends_at = file_contents.find(")")
        list_of_appended_requirements.append(
            string_dependency_to_dict(
                file_contents[:ends_at]
                .replace(" ", "").replace("\'", "").replace("\"", "")))
    return list_of_appended_requirements


def get_install_requires_field_contents(file_contents):
    file_contents = fix_unequal_conditions(remove_comments(file_contents).replace(" = ", "="))
    file_contents = ''.join(file_contents.splitlines())
    starts_at = file_contents.find("install_requires=[")
    file_contents = file_contents[starts_at + 18:]
    ends_at = file_contents.find("]") - 2
    file_contents = file_contents[:ends_at]
    list_of_requirements = file_contents.replace(" ", "")\
        .replace("\'", "").replace("\"", "").split(",")
    return list_of_requirements


def filter_list_for_unversioned_dependencies(
        list_of_dependencies, ignore_this):
    unversioned_dependencies = []
    for dependency in list_of_dependencies:
        if dependency != '':
            if "==" not in dependency:
                if not re.match(re.compile(ignore_this), dependency):
                    unversioned_dependencies.append(
                        string_dependency_to_dict(dependency))
    return unversioned_dependencies


def filter_list_for_versioned_dependencies(list_of_dependencies, ignore_this):
    versioned_dependencies = []
    for dependency in list_of_dependencies:
        if dependency != '':
            if "=" in dependency:
                if not re.match(re.compile(ignore_this), dependency):
                    versioned_dependencies.append(
                        string_dependency_to_dict(dependency))
    return versioned_dependencies


def get_dependency_with_latest_version(list_of_dependencies, ignore_this):
    dependencies = []
    for dependency in list_of_dependencies:
        if dependency != '':
            if not re.match(re.compile(ignore_this), dependency):
                dependencies.append(string_dependency_to_dict(dependency))
    return dependencies


def string_dependency_to_dict(string_dependency):
    dependency_dict = re.split("<|>|=", string_dependency)
    is_locked = False
    if "==" in string_dependency:
        is_locked = True
    version_relation = string_dependency.replace(dependency_dict[0], "")
    dependency_dict = [dependency_dict[0], is_locked, version_relation,
                       get_latest_version_number(dependency_dict[0])]
    return dependency_dict


def get_latest_version_number(package_name):
    pkg, all_versions = CheeseShop().query_versions_pypi(package_name)
    if len(all_versions):
        return all_versions[0]
    return None


def check_all_filename_in_subdirs(path, filename_to_search_for,
                                  field_dependency_name, ignore_this):
    for dir in os.listdir(path):
        try:
            filename = path + dir + filename_to_search_for
            file_contents = get_file_contents(filename)
            file_contents = file_contents.replace(" = ", "=")
            if field_dependency_name not in file_contents:
                continue
            dependency_list = get_dependency_with_latest_version(
                get_install_requires_field_contents(file_contents),
                ignore_this)
            dependency_list += get_append_list(file_contents, ignore_this)
            if dependency_list is not []:
                print filename
                print dependency_list

        except IOError:
            continue

# path = '/Users/gilzellner/dev/git/cloudify-cosmo/'
# filename = "/setup.py"
# field_dependency_name = "install_requires=["
# check_all_filename_in_subdirs(path,
#                               filename, field_dependency_name, "cloudify.*")
