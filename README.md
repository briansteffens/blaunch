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

# Configuration

*blaunch* has two config files: one to define the menu options available
and one for behavior settings.

## /etc/blaunch/blaunch.conf

This file controls the behavior of *blaunch*. Here's an example:

```
auto_run=True
padding=5
font_size=10
font_name=Monospace
position_x=810
position_y=415
size_w=300
size_h=250
shell_prefix=$
```

The available options are as follows:

- **auto_run** - If True, a menu item will be launched immediately when its
                 shortcut is typed, with no need to press enter first.
- **padding** - The padding used in laying out the launcher window.
- **font_size** - The font size for the menu text.
- **font_name** - The font name for the menu text. This should be a fixed-width
                  font unless you prefer a messed up layout.
- **position_x** - The horizontal position the launcher window will start at.
- **position_y** - The vertical position the launcher window will start at.
- **size_w** - The default width of the launcher window.
- **size_h** - The default height of the launcher window.
- **shell_prefix** - The key (or keys) used to run an ad-hoc shell command
                     instead of selecting a menu item.
