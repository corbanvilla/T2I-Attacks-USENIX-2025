#!/usr/bin/env python3

"""
This module is a helpful script to download the latest images from the database.
"""

import sys

sys.path.append("..")
sys.path.append(".")

import os

from db import *
from analysis import *
from helpers import save_image_from_db

delete_prev = True
download_dir = "./exploration/images/"

# Clear dir
if delete_prev:
    files = [f for f in os.listdir(download_dir) if f.endswith(".png")]
    for f in files:
        os.remove(os.path.join(download_dir, f))

# Fetch prompts
data = (
    session.query(
        ImageCreationRequest.id,
    )
    .order_by(desc(ImageCreationRequest.id))
    .limit(5)
)
df = query_to_df(data)

# Download all
creation_request_ids = list(df.index)
for id in creation_request_ids:
    save_image_from_db(id, f"{download_dir}/{id}.png")
    print(f"Downloaded {id}")
