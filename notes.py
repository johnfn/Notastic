#!/usr/bin/python

# TODO C-X quit
# TODO Display current note in titlebar

from Tkinter import *
import os.path
import pickle

DIR = "/home/grant/notes/"

def inspect(obj):
  """Inspects an object. Prints out all internal properties. Not recursive."""
  for fn_string in dir(obj):
    sub_obj = getattr(obj, fn_string)
    obj_type = ""

    if hasattr(sub_obj, '__call__'):
      obj_type = "function"
      print "function %s" % sub_obj.__name__
      print sub_obj.__doc__
    else:
      print "%s = %s" % (fn_string, sub_obj)

class Internal:
  """ Internal class to Settings. """

  def __init__(self):
    self.current_file = "main"
    self.all_files = ["main"]

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

  def get_text(self):
    return "\n".join([line[:-1] for line in open(DIR + self.internal.current_file)])

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

  def __init__(self, root):
    self.settings = Settings()
    self.root = root

    frame=Frame(root)
    frame.pack()

    self.txtfr(frame)
    self.text.focus_set()

    self.load_file(self.settings.get_file())

  def load_file(self, file_name):
    self.settings.set_file(file_name)
    self.text.delete(0.0, END)
    self.text.insert(END, self.settings.get_text())
    self.set_title(file_name)


  # Shows the textbox prompt.
  def prompt_user(self):
    self.input_txt.place(x = 0, y = 20)
    self.text.focus_set()

  # Eventually I should abstract out all text functionality, etc...
  def get_text(self):
    return self.text.get(1.0, END)

  def set_title(self, new_title):
    self.root.wm_title("Notatistic - %s" % new_title)

  def save_note(self):
    file_path = DIR + self.settings.get_file()
    if not os.path.exists(file_path):
      os.remove(file_path)

    file_data = open(file_path, 'w')
    print self.get_text()
    file_data.write(self.get_text())
	
  def change_text(self, event):
    key = -1
    
    print inspect(event)

    if len(event.char) > 0:
      key = ord(event.char)

    print key
    if key == 6: # C-F
      self.prompt_user()
    elif key == 17: # C-Q
      self.close_event()
      self.root.destroy() #TODO: Put elsewhere.
    else:
      self.save_note()

    """
    print event
    print dir(event)
    print ord(event.char)
    print self.text.get(1.0, END)
    """

  def close_event(self):
    self.settings.save()
    self.save_note()
    print "Closing."

  def txtfr(self, frame):
    #define a new frame and put a text area in it
    textfr=Frame(frame)
    self.text=Text(textfr,height=10,width=50,background='white')
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

def main():
  root = Tk()
  s=Notes(root)

  def call_close():
    s.close_event()
    root.quit()

  root.protocol("WM_DELETE_WINDOW", call_close)
  root.mainloop()
main()
