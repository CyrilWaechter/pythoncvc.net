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

try:
	t = Transaction(doc, "Renomme la vue")
	t.Start()
	for e in getselection(): #Cherche l'Id des éléments sélectionnés
		view = doc.GetElement(e) #Cherche l'élément correspondant à l'Id
		vft = doc.GetElement(view.GetTypeId()) #Get ViewFamilyType Id
		vft_name = Element.Name.GetValue(vft) #Get ViewFamilyType Name
		vzv = view.get_Parameter(BuiltInParameter.VIEWER_VOLUME_OF_INTEREST_CROP)
		vzv_Id = vzv.AsElementId()
		if str(vzv_Id) == "-1":
			vzv_name = ""
		else:
			vzv_name = "_" + vzv.AsValueString() #Cherche le nom de la zone de définition
		view.Name = "{}{} - {}".format(view.GenLevel.Name, vzv_name, vft_name) #Nomme la vue avec nom du niveau associé + nom du type de la vue
	t.Commit()
except:
    # print a stack trace and error messages for debugging
    import traceback
    traceback.print_exc()
    t.RollBack()
else:
    # no errors, so just close the window
    __window__.Close()
