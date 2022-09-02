import os
from tempfile import TemporaryDirectory
from typing import cast

import pystac
import rasterio as rio
from pystac.extensions.projection import ProjectionExtension
from shapely.geometry import box, shape
from stactools.core.projection import reproject_geom
from stactools.testing import CliTestCase

from stactools.aster.commands import create_aster_command
from stactools.aster.constants import (
    HDF_ASSET_KEY,
    QA_BROWSE_ASSET_KEY,
    QA_TXT_ASSET_KEY,
    SWIR_SENSOR,
    TIR_BROWSE_ASSET_KEY,
    TIR_SENSOR,
    VNIR_BROWSE_ASSET_KEY,
    VNIR_SENSOR,
    XML_ASSET_KEY,
)
from tests import test_data

HDF_PATH_EXTERNAL = "AST_L1T_00305032000040446_20150409135350_78838.hdf"
XML_PATH = "data-files/AST_L1T_00305032000040446_20150409135350_78838.hdf.xml"
VNIR_BROWSE_PATH = (
    "data-files/AST_L1T_00305032000040446_20150409135350_78838_BR.2.VNIR.jpg"
)
TIR_BROWSE_PATH = (
    "data-files/AST_L1T_00305032000040446_20150409135350_78838_BR.2.TIR.jpg"
)
QA_BROWSE_PATH = "data-files/AST_L1T_00305032000040446_20150409135350_78838_BR.2.QA.jpg"
QA_TXT_PATH = "data-files/AST_L1T_00305032000040446_20150409135350_78838_QA.txt"


class CreateItemTest(CliTestCase):
    def create_subcommand_functions(self):
        return [create_aster_command]

    def test_create_item_from_xml(self):
        xml_paths = [
            test_data.get_path(
                "data-files/AST_L1T_00303042000203404_20150409092553_2788.hdf.xml"
            ),
            test_data.get_path(
                "data-files/AST_L1T_00309032000003144_20150411122552_103734.hdf.xml"
            ),
        ]

        for xml_path in xml_paths:
            with self.subTest(xml_path):
                with TemporaryDirectory() as tmp_dir:
                    stac_cmd = [
                        "aster",
                        "create-item",
                        "--xml",
                        xml_path,
                        "--vnir",
                        test_data.get_path("data-files/dummy.tif"),
                        "--swir",
                        test_data.get_path("data-files/dummy.tif"),
                        "--tir",
                        test_data.get_path("data-files/dummy.tif"),
                        "--vnir-browse",
                        VNIR_BROWSE_PATH,
                        "--tir-browse",
                        TIR_BROWSE_PATH,
                        "--qa-browse",
                        QA_BROWSE_PATH,
                        "--qa-txt",
                        QA_TXT_PATH,
                        "--output",
                        tmp_dir,
                    ]

                    self.run_command(stac_cmd)

                    jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
                    self.assertEqual(len(jsons), 1)
                    item_path = os.path.join(tmp_dir, jsons[0])

                    item: pystac.Item = cast(pystac.Item, pystac.read_file(item_path))

                    item.validate()

    def test_create_cogs_then_items(self):
        """Test cogs and items so we don't have to save additional
        test data"""
        hdf_path = test_data.get_external_data(HDF_PATH_EXTERNAL)
        xml_path = test_data.get_path(XML_PATH)

        with TemporaryDirectory() as tmp_dir:
            cog_cmd = [
                "aster",
                "create-cogs",
                "--hdf",
                hdf_path,
                "--xml",
                xml_path,
                "--output",
                tmp_dir,
            ]

            self.run_command(cog_cmd)

            cogs = [p for p in os.listdir(tmp_dir) if p.endswith(".tif")]

            self.assertEqual(
                set(cogs),
                set(
                    [
                        "AST_L1T_00305032000040446_20150409135350_78838-VNIR.tif",
                        "AST_L1T_00305032000040446_20150409135350_78838-SWIR.tif",
                        "AST_L1T_00305032000040446_20150409135350_78838-TIR.tif",
                    ]
                ),
            )

            # Check band names, and that there is variable data
            for cog in cogs:
                sensor = os.path.splitext(cog)[0].split("-")[-1]
                with rio.open(os.path.join(tmp_dir, cog)) as ds:
                    for band_name in ds.descriptions:
                        self.assertTrue(sensor in band_name)

                    self.assertTrue(ds.read().any())

            vnir_cog_fname = next(c for c in cogs if "VNIR" in c)
            swir_cog_fname = next(c for c in cogs if "SWIR" in c)
            tir_cog_fname = next(c for c in cogs if "TIR" in c)

            stac_cmd = [
                "aster",
                "create-item",
                "--xml",
                xml_path,
                "--vnir",
                os.path.join(tmp_dir, vnir_cog_fname),
                "--swir",
                os.path.join(tmp_dir, swir_cog_fname),
                "--tir",
                os.path.join(tmp_dir, tir_cog_fname),
                "--hdf",
                hdf_path,
                "--vnir-browse",
                VNIR_BROWSE_PATH,
                "--tir-browse",
                TIR_BROWSE_PATH,
                "--qa-browse",
                QA_BROWSE_PATH,
                "--qa-txt",
                QA_TXT_PATH,
                "--output",
                tmp_dir,
            ]

            self.run_command(stac_cmd)

            jsons = [p for p in os.listdir(tmp_dir) if p.endswith(".json")]
            self.assertEqual(len(jsons), 1)
            item_path = os.path.join(tmp_dir, jsons[0])

            item: pystac.Item = cast(pystac.Item, pystac.read_file(item_path))

            item.validate()
            self.assertEqual(
                set(item.assets.keys()),
                set(
                    [
                        VNIR_SENSOR,
                        SWIR_SENSOR,
                        TIR_SENSOR,
                        HDF_ASSET_KEY,
                        XML_ASSET_KEY,
                        VNIR_BROWSE_ASSET_KEY,
                        TIR_BROWSE_ASSET_KEY,
                        QA_BROWSE_ASSET_KEY,
                        QA_TXT_ASSET_KEY,
                    ]
                ),
            )

            # Check that the proj bbox and item geom align
            projection_ext = ProjectionExtension.ext(item)
            crs = f"epsg:{projection_ext.epsg}"
            for asset_key in [VNIR_SENSOR, SWIR_SENSOR, TIR_SENSOR]:
                asset_projection_ext = ProjectionExtension.ext(item.assets[asset_key])
                proj_bbox_shp = box(*asset_projection_ext.bbox)
                projected_shp = shape(reproject_geom("epsg:4326", crs, item.geometry))
                self.assertTrue(proj_bbox_shp.covers(projected_shp))
