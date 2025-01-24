#!/usr/bin/env python3

"""
This script is used to send inputs from prompt datasets to DALL-E models.
"""

import sys

sys.path.append("..")
sys.path.append(".")

from db import *
from analysis import *
from helpers import (
    evaluate_prompts,
    generate_dalle_2,
    generate_dalle_3,
    get_prompt_prefix_id,
    calculate_file_hash_from_bytes,
)

model_name = "dalle-3"
model = generate_dalle_3

prompt_prefix_id = get_prompt_prefix_id("none")
print(f"{prompt_prefix_id=}")

"""
Select the prompt dataset to use
"""
data = (
    session.query(Prompts.id, Prompts.prompt).filter(
        Prompts.dataset == "coco",
    )
    # .limit(1)
    # .offset(201)
)
df = query_to_df(data)
prompts = list(df.prompt)
prompt_ids = list(df.index)
print(f"Loaded {len(prompts)} prompts")
input("Press Enter to continue...")

# Insert
for results in evaluate_prompts(model, prompts, batch_size=10):
    requests = []
    for idx, row in results.iterrows():
        prompt_id = prompt_ids.pop(0)
        image_id = None

        # Skip if not successful
        if row["success"] == True:
            print(f"Prompt: {prompt_id} failed to generate image!")

            # Store the image itself
            image_bytes = row["image_bytes"]
            image = Images(
                hash=calculate_file_hash_from_bytes(image_bytes),
                from_b64=True,
                bytes=image_bytes,
            )
            session.add(image)
            session.commit()
            image_id = image.id
            assert image_id is not None

        # Store the creation request
        row = row.to_dict()
        del row["prompt"]
        del row["image_bytes"]

        request = ImageCreationRequest(
            model=model_name,
            prompt_id=prompt_id,
            prompt_prefix_id=prompt_prefix_id,
            image_id=image_id,
            **row,
        )
        requests.append(request)

    session.bulk_save_objects(requests)
    session.commit()
    print(f"Inserted batch of {len(requests)} records")
