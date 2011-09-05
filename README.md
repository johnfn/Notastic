Notastic
=========

Cross-platform lightweight notetaking app. Written in Python. 

Commands
----------

Notatistic uses a stack-like system to track your notes. When you Jump into a topic, you push it on the stack. When you Jump Out, you pop it off the stack and are now looking at the new top-most note.

**Ctrl-J:** *J* ump into the topic your cursor is on. 

**Ctrl-U:** Jump *U* p from a topic.

**Ctrl-Q:** *Q* uit Notatistic. So sad to see you go.


Setup
-------

Binding a key to Notastic is kind of tricky in Ubuntu. I recommend `xbindkeys`, but it's not a perfect solution (you will need to drop `xbindkeys` in your `.bashrc` to ensure it's always run on startup). The key should just run "notes.py".
