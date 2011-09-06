#!/usr/bin/python

# TODO: Start at top of file.
#   TODO: Even better, remember cursor position, like a true stack!
# TODO: Nicer gui
# NICE: display of current stack

from Tkinter import *
import os.path
import pickle
import sys
import tkFont

DIR = sys.path[0] + "/"
PID_FILE = DIR + ".pid"

def inspect(obj):
  """Inspects an object. Prints out all internal properties. Not recursive."""
  for fn_string in dir(obj):
    sub_obj = getattr(obj, fn_string)
    obj_type = ""

    if hasattr(sub_obj, '__call__'):
      obj_type = "function"
      print "function %s" % sub_obj.__name__
      print "\t %s" % str(sub_obj.__doc__).replace("        ", " " * 14)
    else:
      print "%s = %s" % (fn_string, sub_obj)

class Internal:
  """ Internal class to Settings. """

  def __init__(self):
    self.current_file = "main"
    self.all_files = ["main"]
    self.heirarchy = ""

class Settings:
  """ State is kept between different sessions by pickling/unpickling the 
  Settings object (or, to be more precise, the Internal object). """

  SAVE_FILE = "notes.settings"
  internal = None

  def __init__(self):
    self.load()

  def add_file(self, file_name):
    print "loading %s" % file_name
    self.internal.all_files.append(file_name)

  def get_file_data(self):
    file_name = DIR + self.internal.current_file
    if not os.path.exists(file_name):
      open(file_name, "w").close() # Make an empty file

    contents =  "\n".join([line[:-1] for line in open(file_name, 'rw')])
    return contents

  def get_file(self):
    return self.internal.current_file

  # TODO: Maybe this should also load the file in?
  def set_file(self, file_name):
    self.internal.current_file = file_name

  def save(self):
    """ Save the settings. """
    pickle.dump(self.internal, open(DIR + self.SAVE_FILE, 'wb'))

  def load(self):
    if os.path.exists(self.SAVE_FILE):
      self.internal = pickle.load(open(DIR + self.SAVE_FILE, 'rb'))
      print self.internal.current_file
    else:
      self.internal = Internal()

class Modes:
  normal = 0
  find_note = 1

class Notes:
  mode = Modes.normal
  stack = []

  def __init__(self, root):
    self.settings = Settings()
    self.root = root

    frame=Frame(root)
    frame.pack()

    self.txtfr(frame)
    self.text.focus_set()

    self.load_file(self.settings.get_file())
    self.frame=frame

  def load_file(self, file_name):
    self.settings.set_file(file_name)
    self.text.delete(0.0, END)
    self.text.insert(END, self.settings.get_file_data())
    self.text.mark_set("insert", "1.0+%d chars" % 0)
    self.set_title(file_name)

  # Shows the textbox prompt.
  def prompt_user(self):
    self.input_txt.place(x = 0, y = 20)
    self.text.focus_set()

  # Eventually I should abstract out all text functionality, etc...
  def get_text(self):
    return self.text.get(1.0, END)

  def set_title(self, new_title):
    self.root.wm_title("Notastic |   %s" % " > ".join(self.stack + [self.settings.get_file()]))

  def save_note(self):
    file_path = DIR + self.settings.get_file()
    if not os.path.exists(file_path):
      os.remove(file_path)

    file_data = open(file_path, 'w')
    file_data.write(self.get_text())

  def remove_all(self, text, remove):
    for c in remove:
      text = text.replace(c, "")
    return text

  def jump_in(self):
    row = int((self.text.index("insert")).split(".")[0]) - 1
    content = self.get_text().split("\n")[row]

    content = content[:15]
    content = content.replace(" ", "_")
    file_name = self.remove_all(content, "!@#$%^&*(<>,.?/:\"';'[]{}|\\")

    assert file_name != ""

    self.stack.append(self.settings.get_file())
    self.load_file(file_name)

  def jump_out(self):
    self.load_file(self.stack.pop())
	
  def change_text(self, event):
    key = -1

    if len(event.char) > 0:
      key = ord(event.char)

    print key

    if key == 6: # C-F
      self.prompt_user()
    elif key == 17: # C-Q Quit
      self.close_event()
      self.root.destroy() #TODO: Put elsewhere.
    elif key == 10: # C-J Jump in
      self.jump_in()
    elif key == 21: # C-U Jump Up
      self.jump_out()
    else:
      self.save_note()

  def close_event(self):
    self.settings.save()
    self.save_note()
    print "Bye!"

  def txtfr(self, frame):
    self.customFont = tkFont.Font(family="Helvetica", size=12)

    #define a new frame and put a text area in it
    textfr=Frame(frame)
    self.text=Text(textfr,height=20,width=80,background='white', font=self.customFont)
    self.text.bind("<Key>", self.change_text)
    # put a scroll bar in the frame
    scroll=Scrollbar(textfr)
    self.text.configure(yscrollcommand=scroll.set)
    #pack everything
    self.text.pack(side=LEFT)
    scroll.pack(side=RIGHT,fill=Y)
    textfr.pack(side=TOP)

    self.input_txt = Text(textfr, height=2, width=50, background = 'white')
    self.input_txt.place(x = 0, y = 20)
    self.input_txt.pack()
    self.input_txt.pack_forget()

    self.check_send_to_front()

  def check_send_to_front(self):
    f = open(PID_FILE, 'r')
    contents = f.read()
    f.close()

    if contents != "":
      open(PID_FILE, 'wa').close() 
      print "zomg send to top"

      self.root.iconify()
      self.root.update()
      self.root.deiconify()

      self.root.lift()

    self.root.after(1000, self.check_send_to_front)


def main():
  root = Tk()
  root.tk_strictMotif()

  s=Notes(root)

  def call_close():
    s.close_event()
    root.quit()

  root.protocol("WM_DELETE_WINDOW", call_close)
  root.mainloop()

if os.path.exists(PID_FILE):
  print "Already running"
  f = open(PID_FILE, 'w')
  f.write("bringup")
  f.close()
  exit(0)

open(PID_FILE, 'wa').close() # touch PID_FILE

try:
  main()
finally:
  os.remove(PID_FILE)
