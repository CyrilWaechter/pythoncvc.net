from Autodesk.Revit.DB import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
getselection = uidoc.Selection.GetElementIds

#Get current selection and store it
selection = getselection()

#Ask user to pick an object which has the desired reference level
def pickobject():
    from Autodesk.Revit.UI.Selection import ObjectType
    __window__.Hide()
    picked = uidoc.Selection.PickObject(ObjectType.Element, "Sélectionnez la référence")
    __window__.Show()
    return picked

#Retrieve needed information from reference object
ref_object = doc.GetElement(pickobject().ElementId)
ref_level = ref_object.ReferenceLevel 
ref_levelid = ref_level.Id

t = Transaction(doc, "Change reference level")

t.Start()

#Change reference level and relative offset for each selected object in order to change reference plane without moving the object
for e in selection:
	object = doc.GetElement(e)
	object_param_level = object.get_Parameter(BuiltInParameter.FAMILY_LEVEL_PARAM)
	object_Level = doc.GetElement(object_param_level.AsElementId())
	object_param_offset = object.get_Parameter(BuiltInParameter.INSTANCE_FREE_HOST_OFFSET_PARAM)
	object_newoffset = object_param_offset.AsDouble() + object_Level.Elevation - ref_level.Elevation
	object_param_level.Set(ref_levelid)
	object_param_offset.Set(object_newoffset)
	
t.Commit()