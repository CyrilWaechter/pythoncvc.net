from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.DB.Plumbing import *
from Autodesk.Revit.Exceptions import *
from Autodesk.Revit.UI import TaskDialog
from Autodesk.Revit.UI import TaskDialogCommonButtons
from Autodesk.Revit.UI import TaskDialogResult
import ctypes

#Load CoolProp shared library and configure PropsSI c_types units
CP = ctypes.cdll.LoadLibrary(r"C:\Program Files (x86)\pythoncvc.net\RevitPyCVC\Fluides\dll\CoolProp.dll")
PropsSI = CP.PropsSI
PropsSI.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p)
PropsSI.restype = ctypes.c_double

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

#Set desired fluid, initial temperature(freezing temperature ?), desired pressure for properties call
fluid = 'Water'
t_init = 273.15
pressure = 101325

#Check if fluid_type exist and create it if not
fluid_type = FluidType.GetFluidType(doc, fluid)
if fluid_type == None:
	t = Transaction(doc, "Create fluid type")
	t.Start()
	FluidType.Create(doc, fluid)
	t.Commit()
	fluid_type = FluidType.GetFluidType(doc, fluid)

#Add new temperature with associated heat capacity and viscosity
t = Transaction(doc, "Add temperature")
t.Start()
for i in xrange(1,100):
	#Call CoolProp to get fluid properties and convert it to internal units if necessary 
	temperature = 273.15+i
	viscosity = UnitUtils.ConvertToInternalUnits(PropsSI('V','T',t_init+i,'P',pressure,fluid),DisplayUnitType.DUT_PASCAL_SECONDS)
	density = UnitUtils.ConvertToInternalUnits(PropsSI('D','T',t_init+i,'P',pressure,fluid),DisplayUnitType.DUT_KILOGRAMS_PER_CUBIC_METER)
	#Catching exceptions and trying to overwrite temperature if asked by user in the TaskDialog
	try:
		fluid_type.AddTemperature(FluidTemperature(temperature,viscosity,density))
	except ArgumentException:
		result = TaskDialog.Show("Error", "Temperature already exist, do you want to overwrite it ?",TaskDialogCommonButtons.Yes | TaskDialogCommonButtons.No | TaskDialogCommonButtons.Cancel, TaskDialogResult.Yes)
		if result == TaskDialogResult.Yes:
			try:
				fluid_type.RemoveTemperature(temperature)
				fluid_type.AddTemperature(FluidTemperature(temperature,viscosity,density))
			except ArgumentException:
				TaskDialog.Show("Overwrite error", "Temperature is currently in use and cannot be overwritten")
		elif result == TaskDialogResult.No:
			pass
		else:
			break
t.Commit()

