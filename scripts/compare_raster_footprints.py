#!/usr/bin/env python3

"""Generates items with geometries computed from each of the three main assets.

Used to determine which asset should be used to generate tighter item footprints.
"""

import os
import sys

import planetary_computer
import requests
import stactools.core.utils.raster_footprint
from pystac_client import Client
from shapely.geometry import Point

if len(sys.argv) != 2:
    print("Invalid number of arguments.")
    print(f"USAGE: {sys.argv[0]} OUTDIR")
    sys.exit(1)

outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)

client = Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

locations = [
    (40.1672, -105.1019),  # Longmont, CO, USA
    (43.7696, 11.2558),  # Florence, Italy
    (65.6135, -37.6336),  # Tasiilaq, Greenland
    (-12.0464, -77.0428),  # Lima, Peru
    (-41.2924, 174.7787),  # Wellington, New Zealand
]
for location in (Point(location[1], location[0]) for location in locations):
    print(f"Searching at {location}")
    item_search = client.search(
        collections=["aster-l1t"], intersects=location, datetime="2006", max_items=1
    )
    items = list(item_search.get_items())
    assert len(items) == 1
    item = items[0]
    print(f"Found item: {item}")
    for key in ("VNIR", "SWIR", "TIR"):
        item = item.clone()
        print(f"Computing raster footprint for {key}")
        stactools.core.utils.raster_footprint.update_geometry_from_asset_footprint(
            item, asset_names=[key], no_data=0
        )
        dest_href = os.path.join(outdir, f"{item.id}-{key}.json")
        print(f"Saving {dest_href}")
        item.save_object(include_self_link=False, dest_href=dest_href)
        asset = item.assets[key]
        response = requests.get(asset.href)
        asset_path = os.path.join(outdir, f"{item.id}-{key}.tif")
        print(f"Saving {asset_path}")
        with open(asset_path, "wb") as file:
            for chunk in response.iter_content():
                file.write(chunk)
