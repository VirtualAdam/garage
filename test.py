'''file still not working.  AttributeError: 'module' object has no attribute 'find_gateway'
working through compiling the file boot?
'''

#!/usr/bin/python
import os, sys, inspect
# use this if you want to include modules from a subfolder
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"common")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

import startup as start


#Varriables=============================



# ================================

foo = start.foo
print foo
bar = start.bar
print bar




