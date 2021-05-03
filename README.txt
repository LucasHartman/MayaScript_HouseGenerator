Execute this code:
1. Open Maya
2. Go to: Top Menu > Windows > Gneral Editors > Script Editor
3. Create a Python Tab
4. copy/paste this code
5. press 'ExecuteAll' button

#--------------------------------------------------------------------------------------------

import sys

#add folder to PythonPath
sys.path.append('c:/root/to/directory')

# print PythonPaths
from pprint import pprint
sys.path
pprint(sys.path)

# import file
import Main

# refresh file
reload(Main)

# call script
Main.Main()