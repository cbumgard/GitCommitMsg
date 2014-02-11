import sublime, sublime_plugin
import threading
import subprocess
import os
import sys
import re

class GitCommitMsgThread(threading.Thread):
  def __init__(self, file_name, start_line, end_line):
    threading.Thread.__init__(self)
    if sublime.platform() == 'windows':
      cmd = 'echo off && ' \
        'for /f "tokens=1" %%a in ' \
        '( \'"git blame "%s" -L %d,%d --root -s -l"\') do ' \
        'git show --name-status "%%a"'
    else:
      cmd = "git show --name-status $(git blame '%s' -L %d,%d | " \
        "awk '{print $1}')"
    self.command = cmd % (file_name, start_line, end_line)
    self.dir_name = os.path.dirname(file_name)

  def run(self):
    print('GitCommitMsg - Command: %s' % self.command)
    pr = subprocess.Popen(self.command, cwd = self.dir_name, \
      shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    (out, error) = pr.communicate()
    self.result = out

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
    selected = self.view.sel()[0];
    start_line = self.view.rowcol(selected.begin())[0] + 1
    end_line = self.view.rowcol(selected.end())[0] + 1

    thread = GitCommitMsgThread(file_name, start_line, end_line)
    thread.start()
    thread.join(5.0) # Timeout in sec

    if thread.isAlive():
      # Thread timed out
      print("GitCommigMsg - Git thread stalled")
    else:
      # Threaded job finished succesfully
      print("GitCommigMsg - Git result received succesfully")
      if len(thread.result) == 0:
        if start_line == end_line:
          result = "Current line is not committed yet."
        else:
          result = "Selected lines are not committed yet."
      else:
        result = thread.result.decode("utf-8")
      new_file = self.view.window().new_file()
      new_file.insert(edit, 0, result)
      new_file.set_scratch(True)
      new_file.set_read_only(True)

      new_file.set_syntax_file("Packages/GitCommitMsg/GitCommitMsg.tmLanguage")

      tab_title = os.path.basename(file_name) + " @" + str(start_line)
      if start_line != end_line:
        tab_title = tab_title + "," + str(end_line)
      new_file.set_name(tab_title)
