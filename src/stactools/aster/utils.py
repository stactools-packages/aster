import re
from collections import defaultdict
from typing import Dict, Optional

import shapely.geometry
import stactools.core.utils.raster_footprint
from pystac import Item
from pystac.extensions.eo import Band
from stactools.core.projection import epsg_from_utm_zone_number
from stactools.core.utils.raster_footprint import DEFAULT_PRECISION

from stactools.aster.constants import (
    ASTER_BANDS,
    ASTER_FILE_NAME_REGEX,
    NO_DATA,
    SWIR_SENSOR,
    TIR_SENSOR,
    VNIR_SENSOR,
)


class AsterSceneId:
    def __init__(self, start_datetime, production_datetime, processing_number):
        self.start_datetime = start_datetime
        self.production_datetime = production_datetime
        self.processing_number = processing_number

    @property
    def item_id(self):
        """The ID used for STAC Items. Comprised of the start_datetime
        and production_datetime, which are sufficient for identifying
        the scene."""
        return "AST_L1T_{}_{}".format(self.start_datetime, self.production_datetime)

    @property
    def file_prefix(self):
        return "AST_L1T_{}_{}_{}".format(
            self.start_datetime, self.production_datetime, self.processing_number
        )

    @staticmethod
    def from_path(path):
        m = re.search(ASTER_FILE_NAME_REGEX, path)
        if m:
            start_datetime = m.group("start")
            production_datetime = m.group("production")
            processing_number = m.group("processing")
        else:
            raise Exception(
                "File name does not match ASTER L1T 003 file name "
                "pattern, which is needed to extract IDs."
            )

        return AsterSceneId(start_datetime, production_datetime, processing_number)


def epsg_from_aster_utm_zone_number(utm_zone_number):
    south = False

    # ASTER LT1 uses negative numbers to indicate southern zones
    if utm_zone_number < 0:
        south = True
        utm_zone_number *= -1

    return epsg_from_utm_zone_number(utm_zone_number, south)


def get_sensors_to_bands() -> Dict[str, Band]:
    sensor_to_bands = defaultdict(list)

    def key(band: Band) -> str:
        match = re.search("([d]+)", band.name)
        if match:
            return match.group(1)
        else:
            return ""

    # Gather the bands for each sensor, sorted by band number
    for band in ASTER_BANDS:
        sensor_to_bands[band.name.split("_")[0]].append(band)
    for sensor in sensor_to_bands:
        sensor_to_bands[sensor] = sorted(sensor_to_bands[sensor], key=key)

    return dict(sensor_to_bands)


def update_geometry(
    item: Item,
    *,
    precision: int = DEFAULT_PRECISION,
    densification_factor: Optional[int] = None,
    simplify_tolerance: Optional[float] = None,
) -> Item:
    """Updates an ASTER item geometry to enclose all bands of all three main assets.

    The Item's geometry is modified in the operation, and the modified item is
    returned from the function.

    Args:
        item (pystac.Item): The ASTER item.

    Returns:
        pystac.Item: The updated item.

    """
    footprints = list()
    for key in (VNIR_SENSOR, SWIR_SENSOR, TIR_SENSOR):
        asset = item.assets.get(key)
        if asset:
            href = asset.get_absolute_href()
            if href:
                footprint = stactools.core.utils.raster_footprint.data_footprint(
                    href=href,
                    precision=precision,
                    densification_factor=densification_factor,
                    simplify_tolerance=simplify_tolerance,
                    no_data=NO_DATA,
                    bands=[],
                )
                footprints.append(shapely.geometry.shape(footprint))
    if not footprints:
        return item
    merged_footprint = footprints[0]
    for footprint in footprints[1:]:
        merged_footprint = merged_footprint.union(footprint)
    item.geometry = shapely.geometry.mapping(merged_footprint)
    return item
