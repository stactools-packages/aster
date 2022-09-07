import os.path
from tempfile import TemporaryDirectory

import stactools.aster.cog
from stactools.aster.xml_metadata import XmlMetadata


def test_create_cogs(hdf_path: str, xml_metadata: XmlMetadata) -> None:
    with TemporaryDirectory() as temporary_directory:
        cogs = stactools.aster.cog.create_cogs(
            hdf_path, xml_metadata, temporary_directory
        )
        assert len(cogs) == 3
        for path in cogs.values():
            assert os.path.exists(path)


def test_create_cogs_subdirectory(hdf_path: str, xml_metadata: XmlMetadata) -> None:
    with TemporaryDirectory() as temporary_directory:
        output_directory = os.path.join(temporary_directory, "subdirectory")
        cogs = stactools.aster.cog.create_cogs(hdf_path, xml_metadata, output_directory)
        assert len(cogs) == 3
        for path in cogs.values():
            assert os.path.exists(path)
