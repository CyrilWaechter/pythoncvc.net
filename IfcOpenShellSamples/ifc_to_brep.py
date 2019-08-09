# coding: utf8
import ifcopenshell
from ifcopenshell import geom
import FreeCAD
import FreeCADGui
import Part


def convert_geom(ifc_entity, doc, settings):
    """Convert ifc entity to a basic FreeCAD Part"""

    shape = geom.create_shape(settings, ifc_entity)
    # occ stands for OpenCascade
    occ_shape = shape.geometry.brep_data

    # IfcOpenShell generate an Open Cascade BREP
    with open("IfcOpenShellSamples/brep_data", "w") as file:
        file.write(occ_shape)

    # Create FreeCAD shape from Open Cascade BREP
    fc_shape = Part.Shape()
    fc_shape.importBrepFromString(occ_shape)

    # Ifc lenght internal unit : meter. FreeCAD internal unit : mm.
    fc_shape.scale(1000)

    # Add geometry to FreeCAD scenegraph (Coin)
    fc_part = doc.addObject("Part::Feature", "IfcPart")
    fc_part.Shape = fc_shape

    return fc_part


def display_geom(ifc_path, base_class="IfcProduct"):
    """Display geom in from file in FreeCAD"""
    ifc_file = ifcopenshell.open(ifc_path)

    # Define settings
    settings = geom.settings()
    settings.set(settings.USE_BREP_DATA, True)

    # Allow you to embed FreeCAD in python https://www.freecadweb.org/wiki/Embedding_FreeCAD
    FreeCADGui.showMainWindow()
    doc = FreeCAD.newDocument()

    parts = [
        convert_geom(ifc_entity, doc, settings)
        for ifc_entity in ifc_file.by_type(base_class)
    ]

    # Set Draw Style to display mesh edges. Orient view and fit to wall
    FreeCADGui.runCommand("Std_DrawStyle", 1)
    for part in parts:
        FreeCADGui.Selection.addSelection(part)
    FreeCADGui.activeView().viewIsometric()
    FreeCADGui.SendMsgToActiveView("ViewSelection")

    FreeCADGui.exec_loop()


if __name__ == "__main__":
    # Open the IFC file
    ifc_path = "IfcOpenShellSamples/Wall.ifc"
    display_geom(ifc_path, base_class="IfcWall")
