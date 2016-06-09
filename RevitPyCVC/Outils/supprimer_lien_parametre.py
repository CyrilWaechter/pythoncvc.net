from Autodesk.Revit.DB import *
from System import Guid

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
app = __revit__.Application

#Retrieve all parameters in the document
params = FilteredElementCollector(doc).OfClass(ParameterElement)
filteredparams = []

#Store parameters which has a name starting with "magi" or "MC"
for param in params:
	if param.Name.startswith(("magi", "MC")): #startswith method accept tuple
		filteredparams.append(param)
		print param.Name #To check if a parameter in the list is not supposed to be deleted

#Delete all parameters in the list
t = Transaction(doc, "Delete parameters")
t.Start()
for param in filteredparams:
	doc.Delete(param.Id)
t.Commit()