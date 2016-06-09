from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Mechanical import Space
from Autodesk.Revit.DB.Architecture import Room
from Autodesk.Revit.UI import UIApplication
from System import Guid

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
getselection = uidoc.Selection.GetElementIds
app = __revit__.Application

#reference desired link
for e in app.Documents:
	if e.Title == "GR8_HOP_MN_R16.rvt":
		lien = e

#Reference the parameter you want to copy by GUID or BuiltInParameter
paramguid = Guid("88938699-b86d-4efa-aeb6-ce66d17d7755")

t = Transaction(doc, "Copy shared parameter from rooms to spaces")

t.Start()
#Get all spaces in the current project
for space in FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_MEPSpaces):	
	if space.Location != None: #Check if the space is placed
		#Get room at space insertion point location. Credit to Revitalizer : https://forums.autodesk.com/t5/revit-api/mep-space-class-room-property-returns-null-with-linked-models/td-p/3650268
		room = lien.GetRoomAtPoint(space.Location.Point)
		#Check if there is actually a room at this location
		if room != None:
			#Call desired parameter in both room and space
			spaceparam = space.get_Parameter(paramguid)
			roomparam = room.get_Parameter(paramguid)
			try:
				#Try to set space parameter value with room parameter value. It can fail if value is null for exemple 
				spaceparam.Set(roomparam.AsString())
			except:
				pass
t.Commit()

__window__.Close()