import pytest

from stactools.aster.xml_metadata import XmlMetadata
from tests import test_data


@pytest.fixture
def hdf_path() -> str:
    return test_data.get_external_data(
        "AST_L1T_00305032000040446_20150409135350_78838.hdf"
    )


@pytest.fixture
def xml_metadata() -> XmlMetadata:
    path = test_data.get_path(
        "data-files/AST_L1T_00305032000040446_20150409135350_78838.hdf.xml"
    )
    return XmlMetadata.from_file(path)
