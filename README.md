# python-dependency-verifier
A tool to make sure that all dependencies in a python project are version locked and up to date

How to use:
```bash
$ pip install https://github.com/cloudify-cosmo/python-dependency-verifier/archive/master.zip
```

and then in python:

```python
from python_dependency_verifier import python_dependency_verifier


path = '/Users/gilzellner/dev/git/cloudify-cosmo/'
<<<<<<< HEAD
regex_to_ignore = "cloudify.*"
test = PythonSetuptoolsDependencyCheckerForDir(path, regex_to_ignore).check_all_filename_in_subdirs()
print json.dumps(test)
=======
filename = "/setup.py"
field_dependency_name = "install_requires=["
check_all_filename_in_subdirs(path,filename, field_dependency_name, "cloudify.*")
>>>>>>> 2fb55bd9a5fcf6d3dd67ce980078ac18c5e8687e
```
