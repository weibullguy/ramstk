# Establishing a Development Environment

This document describes how to setup a development environment for RAMSTK.  These
instructions ensure every developer is using, ideally, the same environment
regardless of platform.

## Required Tools

The following applications will be required to setup the development
environment.  These may be installed system-wide using your package manager or
installed in a local directory and only available for single user.  Either way,
these tools are only required to setup the RAMSTK development environment, they
are not used **in** the environment:

  - virtualenv
  - virtualenvwrapper

## Create the Virtual Environment

Once the tools in the previous section are installed and available for your
use, the next step is to create a virtual environment to develop RAMSTK in.
Execute the following to setup the virtual environment:
```
~/projects/RAMSTK $ export WORKON_HOME="$HOME/.virtualenvs"
~/projects/RAMSTK $ export PROJECT_HOME-"$HOME/projects"
~/projects/RAMSTK $ source $(which virtualenvwrapper.sh)
~/projects/RAMSTK $ mkvirtualenv ramstk-python2.7-pygtk
```

You should now find yourself in a virtual environment named
ramstk-python2.7-pygtk.  The paths and virtual environment name above can be
changed to whatever you would like, those are just the names I use.  Whenever
you need to work in the RAMSTK environment, just execute
`workon ramstk-python2.7-pygtk` to re-enter the virtual environment.

## Install Python Packages

After you are in the virtual environment, you will need to install the Python
packages needed by RAMSTK to run and some recommended packages for development and
testing.
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install -U pip
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install -U setuptools>12.0
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install --only-binary=numpy numpy==1.14.3
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install --only-binary=scipy scipy==1.0.0
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install coverage==4.0.3
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install -r requirements_run.txt
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install -r requirements_dev.txt
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install -r requirements_doc.txt
```

Now that most everything needed in the development environment that can be
installed via PyPi is installed, it is necessary to manually install PyGTK in
the new virtual environment.  It is important to install numpy before PyGTK so
PyGTK will build with numpy support.

First create a build directory and download the PyGTK source tarballs into
that directory:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd $PROJECT_HOME
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ mkdir pygtk_build
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd pygtk_build
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ wget http://www.cairographics.org/releases/py2cairo-1.10.0.tar.bz2
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ wget http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-2.28.6.tar.bz2
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ wget http://ftp.gnome.org/pub/GNOME/sources/pygtk/2.24/pygtk-2.24.0.tar.bz2
```

Now build py2cairo and install into the virtual environment:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ tar -xf py2cairo-1.10.0.tar.bz2
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd py2cairo-1.10.0
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ./waf configure --prefix=$VIRTUAL_ENV
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ./waf build
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ./waf install
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd ..
```

Now build pygobject and install into the virtual environment:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ tar -xf pygobject-2.28.6.tar.bz2
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd pygobject-2.28.6
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ./configure --prefix=$VIRTUAL_ENV --disable-introspection
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ make
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ make install
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd ..
```

Now build pygtk and install into the virtual environment:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ tar -xf pygtk-2.24.0.tar.bz2
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd pygtk-2.24.0
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ./configure --prefix=$VIRTUAL_ENV
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ make
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ make install
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ cd $PROJECT_HOME/RAMSTK
```

Optionally, verify PyGTK installed and is importable.
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ python

>>> import gtk
>>> quit()
```

Finally, after PyGTK is successfully installed in the virtual environment, it
is time to install matplotlib.  Install matplotlib after PyGTK is necessary so
matplotlib builds the GDK backend.
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ pip install matplotlib==1.4.3
```

Optionally, verify the GDK backend shared library (**__backend_gdk.so**) is
installed:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ ls $VIRTUAL_ENV/lib/python2.7/site-packages/matplotlib/backends
```

## Install and Test RAMSTK

Now that all the required runtime, development, and documentation packages are
installed, RAMSTK itself should be installed and tested:
```
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ python setup.py develop
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ which ramstk
/home/arowland/.virtualenvs/ramstk-python2.7-pygtk/bin/ramstk
(ramstk-python2.7-pygtk) ~/projects/RAMSTK $ python setup.py test
```

If all goes well, all the tests will pass and you will be ready to develop and
use RAMSTK.  Good luck and thanks for your help!!

Doyle 'weibullguy' Rowland
May 20, 2018
