# nostrap.py
Create a virtualenv with nothing but python

## Example

Python installed with nothing else:

```shell
$ python -m pip
/usr/bin/python: No module named pip
$ python -m virtualenv
/usr/bin/python: No module named virtualenv
```

Run ```nostrap.py```:
```shell
$ python nostrap.py
Get pip-8.1.1-py2.py3-none-any.whl -> /tmp/tmpga_2ef/pip-8.1.1-py2.py3-none-any.whl
Get setuptools-20.3.1-py2.py3-none-any.whl -> /tmp/tmpga_2ef/setuptools-20.3.1-py2.py3-none-any.whl
Get wheel-0.29.0-py2.py3-none-any.whl -> /tmp/tmpga_2ef/wheel-0.29.0-py2.py3-none-any.whl
Get virtualenv-15.0.1-py2.py3-none-any.whl -> /tmp/tmpga_2ef/virtualenv-15.0.1-py2.py3-none-any.whl
Created virtual env: pyenv
$ source pyenv/bin/activate
(pyenv) $ pip -V
pip 8.1.1 from /home/user/pyenv/lib/python3.5/site-packages (python 3.5)
```
