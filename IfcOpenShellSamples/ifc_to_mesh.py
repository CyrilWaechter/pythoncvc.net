import ifcopenshell
from ifcopenshell import geom
import FreeCAD
import FreeCADGui
import Mesh


def read_geom(ifc_path):

    ifc_file = ifcopenshell.open(ifc_path)

    settings = geom.settings()

    for ifc_entity in ifc_file.by_type("IfcWall"):
        shape = geom.create_shape(settings, ifc_entity)
        # ios stands for IfcOpenShell
        ios_vertices = shape.geometry.verts
        ios_edges = shape.geometry.edges
        ios_faces = shape.geometry.faces

        # IfcOpenShell store vertices in a single tuple, same for edges and faces
        print(ios_vertices)
        print(ios_edges)
        print(ios_faces)
        """ Above will result in :
(0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 10.0, 0.0, 0.0, 10.0, 0.0, 3.0, 10.0, 0.2, 0.0, 10.0, 0.2, 3.0, 0.0, 0.2, 0.0, 0.0, 0.2, 3.0)
(0, 1, 1, 3, 0, 2, 2, 3, 2, 3, 2, 4, 3, 5, 4, 5, 4, 5, 5, 7, 4, 6, 6, 7, 6, 7, 0, 6, 1, 7, 0, 1, 0, 6, 0, 2, 4, 6, 2, 4, 1, 7, 1, 3, 5, 7, 3, 5)
(1, 0, 3, 3, 0, 2, 3, 2, 4, 5, 3, 4, 5, 4, 7, 7, 4, 6, 7, 6, 0, 1, 7, 0, 0, 6, 2, 2, 6, 4, 3, 7, 1, 5, 7, 3)
"""
        print(set(ios_edges))
        print(set(ios_faces))
        """ Above will result in :
{0, 1, 2, 3, 4, 5, 6, 7}
{0, 1, 2, 3, 4, 5, 6, 7}
"""

        # Let's parse it and prepare it for FreeCAD import
        vertices = [
            FreeCAD.Vector(ios_vertices[i : i + 3])
            for i in range(0, len(ios_vertices), 3)
        ]
        edges = [ios_edges[i : i + 2] for i in range(0, len(ios_edges), 2)]
        faces = [tuple(ios_faces[i : i + 3]) for i in range(0, len(ios_faces), 3)]

        print(
            f"This {ifc_entity.is_a()} has been defined by {len(vertices)} vertices, {len(edges)} edges and {len(faces)} faces"
        )
        print(vertices)
        print(edges)
        print(faces)
        """ Above will result in :
This IfcWall has been defined by 8 vertices, 24 edges and 12 faces
[(0.0, 0.0, 0.0), (0.0, 0.0, 3.0), (10.0, 0.0, 0.0), (10.0, 0.0, 3.0), (10.0, 0.2, 0.0), (10.0, 0.2, 3.0), (0.0, 0.2, 0.0), (0.0, 0.2, 3.0)]
[(0, 1), (1, 3), (0, 2), (2, 3), (2, 3), (2, 4), (3, 5), (4, 5), (4, 5), (5, 7), (4, 6), (6, 7), (6, 7), (0, 6), (1, 7), (0, 1), (0, 6), (0, 2), (4, 6), (2, 4), (1, 7), (1, 3), (5, 7), (3, 5)]
[(1, 0, 3), (3, 0, 2), (3, 2, 4), (5, 3, 4), (5, 4, 7), (7, 4, 6), (7, 6, 0), (1, 7, 0), (0, 6, 2), (2, 6, 4), (3, 7, 1), (5, 7, 3)]
"""
        return {"vertices": vertices, "edges": edges, "faces": faces}


if __name__ == "__main__":
    mesh_values = read_geom(
        "/home/cyril/git/pythoncvc.net/IfcOpenShellSamples/Wall.ifc"
    )

    # Create a FreeCAD geometry. A FreeCAD can take vertices and faces as input
    mesh = Mesh.Mesh((mesh_values["vertices"], mesh_values["faces"]))
    # Ifc lenght internal unit : meter. FreeCAD internal unit : mm.
    scale_factor = 1000
    matrix = FreeCAD.Matrix()
    matrix.scale(scale_factor, scale_factor, scale_factor)
    mesh.transform(matrix)

    # Allow you to embed FreeCAD in python https://www.freecadweb.org/wiki/Embedding_FreeCAD
    FreeCADGui.showMainWindow()
    doc = FreeCAD.newDocument()

    # Add geometry to FreeCAD scenegraph (Coin)
    fc_mesh = doc.addObject("Mesh::Feature", "IfcMesh")
    fc_mesh.Mesh = mesh

    # Set Draw Style to display mesh edges. Orient view and fit to wall
    FreeCADGui.runCommand("Std_DrawStyle",1) 
    FreeCADGui.Selection.addSelection(fc_mesh)
    FreeCADGui.activeView().viewIsometric()
    FreeCADGui.SendMsgToActiveView("ViewSelection")
    
    FreeCADGui.exec_loop()