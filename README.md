# python-dependency-verifier
A tool to make sure that all dependencies in a python project are version locked and up to date

How to use:

`$ pip install https://github.com/cloudify-cosmo/python-dependency-verifier/archive/master.zip`

and then in python:

```
from python_dependency_verifier import python_dependency_verifier
path = '/Users/gilzellner/dev/git/cloudify-cosmo/'
filename = "/setup.py"
field_dependency_name = "install_requires=["
check_all_filename_in_subdirs(path,filename, field_dependency_name, "cloudify.*")
```
