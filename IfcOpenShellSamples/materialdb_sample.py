# coding: utf8
import ifcopenshell
from ifcopenshell import template
import materialdb

# Default location and directions
ORIGIN = (0.0, 0.0, 0.0)
DIR_X = (1.0, 0.0, 0.0)
DIR_Y = (0.0, 1.0, 0.0)
DIR_Z = (0.0, 0.0, 1.0)


def create_ifc_axis2placement(ifc_file, point=ORIGIN, dir_z=DIR_Z, dir_x=DIR_X):
    point = ifc_file.createIfcCartesianPoint(point)
    dir_z = ifc_file.createIfcDirection(dir_z)
    dir_x = ifc_file.createIfcDirection(dir_x)
    return ifc_file.createIfcAxis2Placement3D(point, dir_z, dir_x)


def create_ifclocalplacement(ifc_file, ifcaxis2placement, relative_to=None):
    return ifc_file.createIfcLocalPlacement(relative_to, ifcaxis2placement)


def create_ifc_polyline(ifc_file, points):
    ifcpts = []
    ifc_cartesian_points = [ifc_file.createIfcCartesianPoint(point) for point in points]
    return ifc_file.createIfcPolyLine(ifc_cartesian_points)


def create_ifc_extruded_area_solid(
    ifc_file, extrusion_vertices, ifcaxis2placement, extruded_dir: tuple, depth: float
):
    polyline = create_ifc_polyline(ifc_file, extrusion_vertices)
    closed_profile = ifc_file.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    direction = ifc_file.createIfcDirection(extruded_dir)
    return ifc_file.createIfcExtrudedAreaSolid(
        closed_profile, ifcaxis2placement, direction, depth
    )


def create_ifc_layer_from_materialdb(
    materialdb_layer: materialdb.Layer, thickness: float, is_ventilated: bool = None
):
    name = materialdb_layer.material.name
    material = ifc_file.createIfcMaterial(name)
    material_layer = ifc_file.createIfcMaterialLayer(material, thickness)

    # Create and assign property set
    for pset in generate_material_db_psets(materialdb_layer):
        ifc_rel_properties_uuid = ifcopenshell.guid.new()
        ifc_file.createIfcRelDefinesByProperties(
            ifc_rel_properties_uuid, owner_history, None, None, [material], pset
        )
    return material_layer


def get_material_db_layer(provider_name, material_id, layer_id):
    provider = materialdb.Provider.get_by_name("Swisspor AG")
    material = materialdb.Material.create_from_provider_by_id(provider, material_id)
    return materialdb.Layer.create_layer_from_material_by_id(material, layer_id)


def generate_material_db_psets(layer):
    for pset_name, properties in material_attributes.items():
        property_values = list()
        for prop, values in properties.items():
            property_values.append(
                ifc_file.createIfcPropertySinglevalue(
                    prop,
                    values["Description"],
                    ifc_file.create_entity(
                        values["Type"], getattr(layer, values["attr_name"])
                    ),
                )
            )
        pset_uuid = ifcopenshell.guid.new()
        yield ifc_file.createIfcPropertySet(
            pset_uuid, owner_history, pset_name, None, property_values
        )


material_attributes = {
    "Pset_MaterialThermal": {
        "SpecificHeatCapacity": {
            "Type": "IfcSpecificHeatCapacityMeasure",
            "Description": "Specific Heat Capacity",
            "attr_name": "specific_heat_capacity",
        },
        "ThermalConductivity": {
            "Type": "IfcThermalConductivityMeasure",
            "Description": "Thermal Conductivity",
            "attr_name": "thermal_conductivity",
        },
    },
    "Pset_MaterialCommon": {
        "MassDensity": {
            "Type": "IfcMassDensityMeasure",
            "Description": "Mass Density",
            "attr_name": "density",
        }
    },
    "Pset_FireSecurity": {
        "FireRating": {
            "Type": "IfcLabel",
            "Description": "Fire Rating",
            "attr_name": "fire_resistance",
        },
        "SurfaceSpreadOfFlame": {
            "Type": "IfcLabel",
            "Description": "Surface Spread Of Flame",
            "attr_name": "fire_class",
        },
    },
    "Pset_ManufacturerTypeInformation": {
        "Manufacturer": {
            "Type": "IfcLabel",
            "Description": "Manufacturer",
            "attr_name": "provider_name",
        },
        "SurfaceSpreadOfFlame": {
            "Type": "IfcLabel",
            "Description": "Surface Spread Of Flame",
            "attr_name": "fire_class",
        },
    },
}

if __name__ == "__main__":
    # Obtain references to instances defined in template
    file_name = "materialdb_sample.ifc"
    ifc_file = ifcopenshell.template.create(file_name, schema_identifier="IFC2x3")
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]
    project = ifc_file.by_type("IfcProject")[0]
    context = ifc_file.by_type("IfcGeometricRepresentationContext")[0]

    # IFC hierarchy creation
    site_ifcaxis2placement = create_ifc_axis2placement(ifc_file)
    site_placement = create_ifclocalplacement(ifc_file, site_ifcaxis2placement)
    site = ifc_file.createIfcSite(
        ifcopenshell.guid.new(),
        owner_history,
        "Site",
        None,
        None,
        site_placement,
        None,
        None,
        "ELEMENT",
        None,
        None,
        None,
        None,
        None,
    )

    building_ifcaxis2placement = create_ifc_axis2placement(ifc_file)
    building_placement = create_ifclocalplacement(
        ifc_file, building_ifcaxis2placement, relative_to=site_placement
    )
    building = ifc_file.createIfcBuilding(
        ifcopenshell.guid.new(),
        owner_history,
        "Building",
        None,
        None,
        building_placement,
        None,
        None,
        "ELEMENT",
        None,
        None,
        None,
    )

    storey_ifcaxis2placement = create_ifc_axis2placement(ifc_file)
    storey_placement = create_ifclocalplacement(
        ifc_file, storey_ifcaxis2placement, relative_to=building_placement
    )
    elevation = 0.0
    building_storey = ifc_file.createIfcBuildingStorey(
        ifcopenshell.guid.new(),
        owner_history,
        "Storey",
        None,
        None,
        storey_placement,
        None,
        None,
        "ELEMENT",
        elevation,
    )

    container_storey = ifc_file.createIfcRelAggregates(
        ifcopenshell.guid.new(),
        owner_history,
        "Building Container",
        None,
        building,
        [building_storey],
    )
    container_site = ifc_file.createIfcRelAggregates(
        ifcopenshell.guid.new(), owner_history, "Site Container", None, site, [building]
    )
    container_project = ifc_file.createIfcRelAggregates(
        ifcopenshell.guid.new(),
        owner_history,
        "Project Container",
        None,
        project,
        [site],
    )

    # Create wall
    wall_uuid = ifcopenshell.guid.new()
    wall_relative_placement = create_ifc_axis2placement(ifc_file)
    wall_placement = create_ifclocalplacement(
        ifc_file, wall_relative_placement, relative_to=storey_placement
    )

    polyline = create_ifc_polyline(ifc_file, [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0)])
    axis_representation = ifc_file.createIfcShapeRepresentation(
        context, "Axis", "Curve2D", [polyline]
    )

    extrusion_placement = create_ifc_axis2placement(ifc_file)
    extrusion_vertices = [
        (0.0, -0.1, 0.0),
        (1.0, -0.1, 0.0),
        (1.0, 0.1, 0.0),
        (0.0, 0.1, 0.0),
        (0.0, -0.1, 0.0),
    ]

    extrusion = create_ifc_extruded_area_solid(
        ifc_file, extrusion_vertices, extrusion_placement, (0.0, 0.0, 1.0), 3.0
    )

    extrusion_representation = ifc_file.createIfcShapeRepresentation(
        context, "Body", "SweptSolid", [extrusion]
    )

    product_shape = ifc_file.createIfcProductDefinitionShape(
        None, None, [axis_representation, extrusion_representation]
    )

    wall = ifc_file.createIfcWallStandardCase(
        wall_uuid,
        owner_history,
        "Wall",
        "MaterialDB sample wall",
        None,
        wall_placement,
        product_shape,
        None,
    )

    # Define and associate the wall material
    material_layers = list()
    ## Layer 1
    material_db_layer = get_material_db_layer(
        provider_name="Swisspor AG",
        material_id="10013551-6FC1-43DD-9105-7330D2878121",
        layer_id="10013551-6FC1-43DD-9105-7330D2878121",
    )
    material_layer = create_ifc_layer_from_materialdb(material_db_layer, 0.10)
    material_layers.append(material_layer)

    ## Layer 2
    material_db_layer = get_material_db_layer(
        provider_name="Swisspor AG",
        material_id="13AC9948-9946-421E-974F-4C1B1619D6B6",
        layer_id="13AC9948-9946-421E-974F-4C1B1619D6B6",
    )
    material_layer = create_ifc_layer_from_materialdb(material_db_layer, 0.10)
    material_layers.append(material_layer)

    ## Create layer set
    material_layer_set = ifc_file.createIfcMaterialLayerSet(
        material_layers, "MaterialDB sample layer set"
    )

    material_layer_set_usage = ifc_file.createIfcMaterialLayerSetUsage(
        material_layer_set, "AXIS2", "POSITIVE", -0.1
    )

    material_uuid = ifcopenshell.guid.new()

    ifc_file.createIfcRelAssociatesMaterial(
        material_uuid,
        owner_history,
        RelatedObjects=[wall],
        RelatingMaterial=material_layer_set_usage,
    )

    # Relate the window and wall to the building storey
    ifc_file.createIfcRelContainedInSpatialStructure(
        ifcopenshell.guid.new(),
        owner_history,
        "Building Storey Container",
        None,
        [wall],
        building_storey,
    )

    ifc_file.write(file_name)

