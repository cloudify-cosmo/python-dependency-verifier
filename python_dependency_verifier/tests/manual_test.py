from python_dependency_verifier import python_dependency_verifier
import json

path = '/Users/gilzellner/dev/git/cloudify-cosmo/'
regex_to_ignore = "cloudify.*"
test = python_dependency_verifier.PythonSetuptoolsDependencyCheckerForDir(path, regex_to_ignore).check_all_filename_in_subdirs()
print json.dumps(test)