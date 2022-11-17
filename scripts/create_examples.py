#!/usr/bin/env python3

from pathlib import Path

from stactools.aster import cog, stac
from stactools.aster.xml_metadata import XmlMetadata

root = Path(__file__).parents[1]
data_files = root / "tests" / "data-files"
external = data_files / "external"
hdf_path = external / "AST_L1T_00305032000040446_20150409135350_78838.hdf"
xml_path = data_files / "AST_L1T_00305032000040446_20150409135350_78838.hdf.xml"
item_path = root / "examples" / "AST_L1T_00305032000040446_20150409135350_78838.json"

xml_metadata = XmlMetadata.from_file(xml_path)
paths = cog.create_cogs(hdf_path, xml_metadata, external)
item = stac.create_item(
    xml_href=str(xml_path),
    vnir_cog_href=paths["VNIR"],
    swir_cog_href=paths["SWIR"],
    tir_cog_href=paths["TIR"],
    hdf_href=str(hdf_path),
)
item.set_self_href(str(item_path))
item.make_asset_hrefs_relative()
item.save_object(include_self_link=False)
