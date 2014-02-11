# Sublime Text plugin: GitCommitMsg

Shows the git commit history for one or more lines of code.
Essentially it performs a ```git blame``` on the selected line(s) of code,
and then performs a ```git show``` on the resulting commit(s).

Inspired by ["Every line of code is always documented"](http://mislav.uniqpath.com/2014/02/hidden-documentation/)

## Usage

 * Supports Sublime Text 2 & Sublime Text 3
 * Mac: Default keybinding is __Command+Shift+m__
 * Linux/Windows: Default keybinding is __Alt+Shift+m__
 * Assumes ```git``` is installed and in the ```$PATH```

## Example

![Screenshot](https://i.cloudup.com/UI1EZ841Zd.png)

## Install from Package Control

The easiest way to install this is with [Package Control](http://wbond.net/sublime\_packages/package\_control).

 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package"
 * Select GitCommitMsg when the list appears.

## Manual Install

Use this if for some reason you cannot use Package Control steps above and/or the plugin does not appear yet in Package Control. Thanks to [https://github.com/kemayo/sublime-text-git/wiki](https://github.com/kemayo/sublime-text-git/wiki) for documenting these steps originally.

First, you need to have `git` installed and in your `$PATH`. Afterwards you may need to restart Sublime Text 2 before the plugin will work.

### OSX

    $ cd ~/Library/Application\ Support/Sublime\ Text\ 2/Packages/
    $ git clone git://github.com/cbumgard/GitCommitMsg.git GitCommitMsg

### Linux (Ubuntu like distros)

    $ cd ~/.config/sublime-text-2/Packages/
    $ git clone git://github.com/cbumgard/GitCommitMsg.git GitCommitMsg

### Windows 7:

    Copy the directory to: "C:\Users\<username>\AppData\Roaming\Sublime Text 2\Packages"

### Windows XP:

    Copy the directory to: "C:\Documents and Settings\<username>\Application Data\Sublime Text 2\Packages"
