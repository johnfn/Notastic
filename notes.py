#!/usr/bin/python

from Tkinter import *
import os.path
import pickle

class Internal:
  """ Internal class to Settings. """
  def __init__(self):
    self.last_edited = "main"
    self.all_files = ["main"]

class Settings:
  SAVE_FILE = "notes.settings"
  internal = None

  def __init__(self):
    self.load()

  def add_file(self, file_name):
    self.internal.all_files.append(file_name)

  def get_text(self):
    return "\n".join([line for line in open(self.internal.last_edited)])

  def save(self):
    pickle.dump(self.internal, open(self.SAVE_FILE, 'wb'))

  def load(self):
    if os.path.exists(self.SAVE_FILE):
      self.internal = pickle.load(open(self.SAVE_FILE, 'rb'))
      print self.internal.last_edited
    else:
      self.internal = Internal()

class Modes:
  normal = 0
  find_note = 1

class Notes:
  mode = Modes.normal

  def __init__(self, root):
    self.settings = Settings()

    frame=Frame(root)
    frame.pack()

    self.txtfr(frame)
    self.text.focus_set()

    self.text.insert(END, self.settings.get_text())
	
  def change_text(self, event):
    key = -1

    if len(event.char) > 0:
      key = ord(event.char)

    if key == 6: # C-F
      print "ok"

    """
    print event
    print dir(event)
    print ord(event.char)
    print self.text.get(1.0, END)
    """

  def close_event(self):
    self.settings.save()
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


def main():
  root = Tk()
  s=Notes(root)

  def call_close():
    s.close_event()
    root.quit()

  root.title('textarea')
  root.protocol("WM_DELETE_WINDOW", call_close)
  root.mainloop()
main()
