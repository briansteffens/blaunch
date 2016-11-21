blaunch
========

blaunch is a very simple, mostly text-based program launcher, which basically
just associates character strings with shell commands. These shortcuts can be
set up in nested categories, and a minimal GUI shows the available options as
you type.

![Screenshot](https://s3.amazonaws.com/briansteffens/blaunch.png)

# Installation

```
cd ~
git clone https://github.com/briansteffens/blaunch
cd blaunch
sudo python2 setup.py install --record files.txt
```

All installed files will be listed in files.txt. Uninstallation is sort of
possible with:

```
cat files.txt | sudo xargs rm
```

This doesn't seem to remove directories (/etc/blaunch for example).
