# coding: utf8
import ifcopenshell
from ifcopenshell import geom
import FreeCAD
import FreeCADGui
import Part


def ios_settings(brep):
    """Create ifcopenshell.geom.settings for various cases"""
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, False)  # False by default
    if brep:
        settings.set(settings.USE_BREP_DATA, True)
    return settings


BREP_SETTINGS = ios_settings(brep=True)
MESH_SETTINGS = ios_settings(brep=False)

# IfcOpenShell/IFC default unit is m, FreeCAD internal unit is mm
SCALE = 1000


def convert_brep_geom(ifc_entity, doc):
    """Convert ifc entity to a basic FreeCAD Part"""

    ios_shape = geom.create_shape(BREP_SETTINGS, ifc_entity)
    # occ stands for OpenCascade
    occ_shape = ios_shape.geometry.brep_data

    # Create FreeCAD shape from Open Cascade BREP
    fc_shape = Part.Shape()
    fc_shape.importBrepFromString(occ_shape)
    
    # Ifc lenght internal unit : meter. FreeCAD internal unit : mm.
    fc_shape.scale(SCALE)
    # Shape scale must be applied before shape placement else placement scale would be doubled
    fc_shape.Placement = ios_shape_to_fc_placement(ios_shape)

    # Add geometry to FreeCAD scenegraph (Coin)
    fc_part = doc.addObject("Part::Feature", "IfcPart")
    fc_part.Shape = fc_shape

    return fc_part


def get_matrix(position):
    """Transform position to FreeCAD.Matrix"""
    location = FreeCAD.Vector(position.Location.Coordinates).scale(SCALE, SCALE, SCALE)

    v_1 = FreeCAD.Vector(position.RefDirection.DirectionRatios)
    v_3 = FreeCAD.Vector(position.Axis.DirectionRatios)
    v_2 = v_3.cross(v_1)

    # fmt: off
    matrix = FreeCAD.Matrix(
        v_1.x, v_2.x, v_3.x, location.x,
        v_1.y, v_2.y, v_3.y, location.y,
        v_1.z, v_2.z, v_3.z, location.z,
        0, 0, 0, 1,
    )
    # fmt: on

    return matrix


def ios_shape_to_fc_placement(shape):
    """Return a placement from an IfcOpenShell shape"""
    return FreeCAD.Placement(ios_to_fc_matrix(shape.transformation.matrix.data))


def ios_to_fc_matrix(ios_matrix):
    """Convert a FreeCAD 4x4 matrix from an IfcOpenShell 4x3 matrix.
    IfcOpenShell matrix values is a tuple of 4 consecutive vector's xyz 
    - format : (v1.x, v1.y, v1.z, v2.x, v2.y … , v4.z).
    FreeCAD matrix constructor takes up to 16 float. 4 vectors grouped by x, y, z values
    optionnally followed by 0, 0, 0, 1 (0 = direction, 1 = location).
    - format : (v1.x, v2.x, v3.x, v4.x, v1.y, … , v4.z, 0, 0, 0, 1)
    In consequence values needs to be transposed"""
    m_l = list()
    for i in range(3):
        line = list(ios_matrix[i::3])
        line[-1] *= SCALE
        m_l.extend(line)
    return FreeCAD.Matrix(*m_l)


def display_geom(ifc_path, base_class="IfcProduct"):
    """Display geom in from file in FreeCAD"""

    ifc_file = ifcopenshell.open(ifc_path)

    # Allow you to embed FreeCAD in python https://www.freecadweb.org/wiki/Embedding_FreeCAD
    FreeCADGui.showMainWindow()
    doc = FreeCAD.newDocument()

    parts = [
        convert_brep_geom(ifc_entity, doc)
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
    ifc_path = "IfcOpenShellSamples/hello_wall.ifc"
    display_geom(ifc_path, base_class="IfcWall")
