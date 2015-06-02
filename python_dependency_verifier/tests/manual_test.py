from python_dependency_verifier import python_dependency_verifier
import json

path = '/Users/gilzellner/dev/git/cloudify-cosmo/'
regex_to_ignore = "cloudify.*"
print json.dumps(python_dependency_verifier.check_dependencies_dir(
    path, regex_to_ignore))
