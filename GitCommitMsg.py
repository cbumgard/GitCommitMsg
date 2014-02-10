import sublime, sublime_plugin
import subprocess
import os
import sys


class GitCommitMsgCommand(sublime_plugin.TextCommand):
  """
  Custom git_commit_msg plugin:
  Shows the git commit history for one or more lines of code.
  Default keybinding is cmd+shift+m (Mac) or alt+shift+m (Linux/Windows).

  Inspired by "Every line of code is always documented"
  (http://mislav.uniqpath.com/2014/02/hidden-documentation/)

  Assumes git is installed and in the path.
  """
  def run(self, edit):
    file_name = self.view.file_name()
    dir_name = os.path.dirname(file_name)
    selected = self.view.sel()[0];
    start_line = self.view.rowcol(selected.begin())[0] + 1
    end_line = self.view.rowcol(selected.end())[0] + 1
    # Call 'git' commands in a subproc:
    cmd = "git show --name-status $(git blame '%s' -L %d,%d | awk '{print $1}')" \
      % (file_name, start_line, end_line) # use --quiet instead for no file stats
    # TODO: run in separate thread. It's quick but best not to block UI thread.
    pr = subprocess.Popen(cmd, cwd = os.path.dirname(file_name), \
      shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (out, error) = pr.communicate()
    print('Executing command: "%s"' % cmd)
    # Show the results in a new tab:
    self.view.window().new_file()
    sublime.active_window().active_view().insert(edit, 0, out.decode("utf-8"))
