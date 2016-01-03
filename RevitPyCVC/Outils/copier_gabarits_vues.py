from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from System.Collections.Generic import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
getselection = uidoc.Selection.GetElementIds
app = __revit__.Application

from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import UIApplication
def alert(msg):
   TaskDialog.Show('RevitPythonShell', msg)

def quit():
   __window__.Close()
exit = quit

t = Transaction(doc, "Copie tous les gabarits de vue")
t.Start()
try:
	ids = List[ElementId]()
	for e in FilteredElementCollector(doc).OfClass(ViewPlan): #Cherche l'Id des éléments sélectionnés
		if e.IsTemplate:
			ids.Add(e.Id)
	ld = {}
	for n, d in enumerate(app.Documents):
		ld[n] = d.Title, d
	for i in ld:
		print i, ld[i][0]
	autreDoc = ld[2][1]
	
	cp_opts = CopyPasteOptions()
	ElementTransformUtils.CopyElements(doc, ids, autreDoc, Transform.Identity, cp_opts)

	t.Commit()
except:
    # print a stack trace and error messages for debugging
    import traceback
    traceback.print_exc()
    t.RollBack()
else:
    # no errors, so just close the window
    __window__.Close()
