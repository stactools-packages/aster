from pathlib import Path

from stactools.aster import cog, stac, utils
from stactools.aster.xml_metadata import XmlMetadata


def test_bbox(tmp_path: Path, hdf_path: str, xml_metadata: XmlMetadata) -> None:
    cogs = cog.create_cogs(hdf_path, xml_metadata, str(tmp_path))
    item = stac.create_item(
        xml_metadata.href,
        vnir_cog_href=cogs["VNIR"],
        swir_cog_href=cogs["SWIR"],
        tir_cog_href=cogs["TIR"],
    )
    new_item = utils.update_geometry(item.clone())
    assert new_item.bbox != item.bbox
    new_item.validate()
