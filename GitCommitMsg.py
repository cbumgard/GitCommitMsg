import sublime, sublime_plugin
import threading
import subprocess
import os
import sys

class GitCommitMsgThread(threading.Thread):
  def __init__(self, view):
    threading.Thread.__init__(self)
    self.view = view
    selected = view.sel()[0]
    self.file_name = view.file_name()
    self.start_line = view.rowcol(selected.begin())[0] + 1
    self.end_line = view.rowcol(selected.end())[0] + 1
    if sublime.platform() == 'windows':
      cmd = 'echo off && ' \
        'for /f "tokens=1" %%a in ' \
        '( \'"git blame "%s" -L %d,%d --root -s -l"\') do ' \
        'git show --name-status "%%a"'
    else:
      cmd = "git show --name-status " \
        "$(git blame '%s' -L %d,%d | " \
        "awk '{print $1}')"
    self.command = cmd % (self.file_name, self.start_line, self.end_line)
    self.dir_name = os.path.dirname(self.file_name)

  def run(self):
    sublime.set_timeout(
      lambda: sublime.status_message("Getting commit info from Git repository ..."),
      100)
    pr = subprocess.Popen(self.command,
      cwd = self.dir_name,
      shell = True,
      stdout = subprocess.PIPE,
      stderr = subprocess.PIPE,
      stdin = subprocess.PIPE)
    (result, error) = pr.communicate()
    if len(result) == 0:
      if self.start_line == self.end_line:
        result = "Current line is not committed yet."
      else:
        result = "Selected lines are not committed yet."
    else:
      result = result.decode("utf-8")

    # Separate different commits with an empty line
    if sublime.platform() == 'windows':
      result = result.replace("\ncommit", "\n\ncommit")

    args = {
      "file_name": self.file_name,
      "start_line": self.start_line,
      "end_line": self.end_line,
      "result": result
    }
    sublime.set_timeout(
      lambda: self.view.run_command("git_commit_msg_result", args),
      100)

class GitCommitMsgResultCommand(sublime_plugin.TextCommand):
  """
  Invisible command to show results in a new scratch
  read-only buffer.

  A separate command is needed to be able to use 'edit' after method
  GitCommitMsgCommand.run has executed, which is the case
  as the main action of this plugin takes place in a
  separate thread.

  If you try to use 'edit' after main 'run' execution, you get
  the following error: "Edit objects may not be used after the
  TextCommand's run method has returned"
  """
  def run(self, edit, file_name, start_line, end_line, result):
    new_file = self.view.window().new_file()
    new_file.run_command("append", {"characters": result})
    new_file.set_scratch(True)
    new_file.set_read_only(True)
    syntax = "Packages/GitCommitMsg/GitCommitMsg.tmLanguage"
    new_file.set_syntax_file(syntax)
    basename = os.path.basename(file_name)
    if start_line == end_line:
      tab_title = "%s@%d" % (basename, start_line)
    else:
      tab_title = "%s@%d,%d" % (basename, start_line, end_line)
    new_file.set_name(tab_title)
    sublime.status_message("")

  def is_visible():
    False

class GitCommitMsgCommand(sublime_plugin.TextCommand):
  """
  Custom git_commit_msg plugin:
  Shows the git commit history for one or more lines of code.
  Default keybinding is cmd+shift+m (Mac) or alt+shift+m (Linux/Windows).

  Inspired by "Every line of code is always documented"
  (http://mislav.uniqpath.com/2014/02/hidden-documentation/)

  Assumes git is installed and in the path.

  All work is performed in a separate thread to avoid
  blocking the UI.
  """
  def run(self, edit):
    thread = GitCommitMsgThread(self.view)
    thread.start()

