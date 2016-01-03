from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
getselection = uidoc.Selection.GetElementIds

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
def alert(msg):
   TaskDialog.Show('RevitPythonShell', msg)

def quit():
   __window__.Close()
exit = quit

# IronPython Pad. Write code snippets here and F5 to run.
t = Transaction(doc, "supprimer_type")
t.Start()
#Trouve l'Id du type des éléments sélectionnés et supprime ces types
for e in getselection():
	s = doc.GetElement(e).GetTypeId()
	doc.Delete(s)
t.Commit()
exit()
	
