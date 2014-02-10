# Sublime Text 2 plugin: GitCommitMsg

Shows the git commit history for one or more lines of code.
Essentially it performs a ```git blame``` on the selected line(s) of code,
and then performs a ```git show``` on the resulting commit(s).

Inspired by ["Every line of code is always documented"](http://mislav.uniqpath.com/2014/02/hidden-documentation/)

## Usage

 * Mac: Default keybinding is __Command+Shift+m__
 * Linux/Windows: Default keybinding is __Alt+Shift+m__
 * Assumes ```git``` is installed and in the ```$PATH```

## Install from Package Control

The easiest way to install this is with [Package Control](http://wbond.net/sublime\_packages/package\_control).

 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package"
 * Select GitCommitMsg when the list appears.