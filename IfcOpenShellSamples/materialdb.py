import requests
import xml.etree.ElementTree as ET
from typing import TypeVar

T = TypeVar("T")


class Provider:
    provider_index_url = "http://www.materialsdb.org/download/ProducerIndex.xml"

    def __init__(self, xml_provider):
        self.xml_provider = xml_provider

    def __repr__(self):
        return super().__repr__()

    @property
    def name(self):
        return self.xml_provider.get("name")

    @property
    def id(self):
        return self.xml_provider.get("id")

    @property
    def url(self):
        return self.xml_provider.get("href")

    @classmethod
    def get_by_name(cls, name: str) -> str:
        return cls._get_by_attribute_value("name", name)

    @classmethod
    def get_by_id(cls, id: str) -> str:
        return cls._get_by_attribute_value("id", id)

    @classmethod
    def _get_by_attribute_value(cls, attribute_name: str, searched_value: any):
        response = requests.get(cls.provider_index_url)
        root = ET.fromstring(response.content)
        for child in root:
            if child.attrib[attribute_name] == searched_value:
                return cls(child)


class Material:
    def __init__(self, provider: Provider, xml_material):
        self.provider = provider
        self.xml_material = xml_material
        self.language = "fr"

    @property
    def information(self):
        return self.xml_material.find("{http://www.materialsdb.org}information")

    @property
    def layers(self):
        return self.xml_material.find("{http://www.materialsdb.org}layers")
    
    @property
    def name(self):
        names = self.information.find("{http://www.materialsdb.org}names")
        for name in names:
            if name.get("lang") == self.language:
                return name.text

    @classmethod
    def _create_from_provider_by_attribute_value(
        cls, provider: Provider, attribute_name: str, value: str
    ):
        response = requests.get(provider.url)
        root = ET.fromstring(response.content)
        for child in root:
            if child.get(attribute_name) == value:
                return cls(provider, child)

    @classmethod
    def create_from_provider_by_id(cls, provider: Provider, id: str) -> T:
        return cls._create_from_provider_by_attribute_value(provider, "id", id)


class Layer:
    def __init__(self, provider: Provider, material: Material, xml_layer):
        self.provider = provider
        self.material = material
        self.xml_layer = xml_layer
        self.country = "CH"

    @property
    def _thermal(self):
        return self.xml_layer.find("{http://www.materialsdb.org}thermal")

    @property
    def _physical(self):
        return self.xml_layer.find("{http://www.materialsdb.org}physical")

    @property
    def _security(self):
        for security in self.xml_layer.findall("{http://www.materialsdb.org}security"):
            if security.get("country") == self.country:
                return security
        else:
            return security

    @property
    def provider_name(self):
        return self.provider.name

    @property
    def _other(self):
        return self.xml_layer.find("{http://www.materialsdb.org}other")

    @property
    def thermal_conductivity(self):
        return float(self._thermal.get("lambda_value"))

    @property
    def specific_heat_capacity(self):
        return float(self._thermal.get("therm_capa"))

    @property
    def density(self):
        return float(self._physical.get("density"))

    @property
    def fire_class(self):
        return self._security.get("FireClass")

    @property
    def fire_resistance(self):
        return self._security.get("FireResis")

    @property
    def rademissivity(self):
        return float(self._other.get("Rademissivity"))

    @classmethod
    def create_layer_from_material_by_id(cls, material: Material, id: str):
        for layer in material.layers:
            if layer.get("id") == id:
                return Layer(material.provider, material, layer)


if __name__ == "__main__":
    provider = Provider.get_by_name("Swisspor AG")
    print(provider.name)
    material = Material.create_from_provider_by_id(
        provider, "05839481-BCB1-4892-B73D-3D9037D14773"
    )
    print(material.name)
    layer = Layer.create_layer_from_material_by_id(
        material, "05839481-BCB1-4892-B73D-3D9037D14773"
    )
    print(layer.thermal_conductivity)

    print(layer.fire_class)

