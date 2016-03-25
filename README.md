# nostrap.py
Create a virtualenv with nothing but Python.

The command line arguments are forwarded directly to `virtualenv`, so usage is the same.

## Why?

I primarily use this for transient build servers or Windows machines where `pip` is not always installed.  Instead of messing around with admin priveleges, use `nostrap.py` to get going now!

More reasons:
* Works on Windows
* Works on any Python version that `virtualenv` supports.
* Automatically get the _latest_ pip and virtualenv.
* No need for admin/sudo.

## Example

Python installed with nothing else:

```shell
$ python -m pip
/usr/bin/python: No module named pip
$ python -m virtualenv
/usr/bin/python: No module named virtualenv
```

Run `nostrap.py`:
```shell
$ python nostrap.py pyenv
Get pip-8.1.1-py2.py3-none-any.whl
Get virtualenv-15.0.1-py2.py3-none-any.whl
...
Installing setuptools, pip, wheel...done.
$ source pyenv/bin/activate
(pyenv) $ pip -V
pip 8.1.1 from /home/user/pyenv/lib/python3.5/site-packages (python 3.5)
```
