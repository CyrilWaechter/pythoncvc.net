# IronPython Pad. Write code snippets here and F5 to run.
import ctypes

#Load CoolProp shared library
CP = ctypes.cdll.LoadLibrary(r"E:\Cyril\Dropbox\CVC\BIM_Revit\ScriptsPython\dll\CoolProp.dll")
#making PropsSI function call shorter
PropsSI = CP.PropsSI
#Convert python data type entered in PropsSI function call to expected argtypes for PropsSI function in the .dll
PropsSI.argtypes = (ctypes.c_char_p, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p, ctypes.c_double, ctypes.c_char_p)
#Convert returned value from .dll to desired data type which is a float in python
PropsSI.restype = ctypes.c_double

#You can then call PropsSI function as in previous article
print PropsSI('C','T',275.15,'P',101325,'INCOMP::Water')