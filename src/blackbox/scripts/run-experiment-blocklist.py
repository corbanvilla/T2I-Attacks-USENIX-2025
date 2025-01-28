#!/usr/bin/env python3

"""
This script runs an experiment to collect blocklist information on DALL-E-2.
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

model_name = "dalle-2"
model = generate_dalle_2
repeats = 5

prompt_prefix_id = get_prompt_prefix_id("none")
print(f"{prompt_prefix_id=}")

"""
Select the prompt dataset to use
"""
offset = 24

data = (
    session.query(Prompts.id, Prompts.prompt).filter(
        Prompts.dataset == "blocklist",
    )
    # .limit(1)
    .offset(offset)
)

data_alt = (
    session.query(Prompts.id, Prompts.prompt).filter(
        Prompts.dataset == "blocklist_mutate",
    )
    # .limit(1)
    .offset(offset)
)

df = query_to_df(data)
df_alt = query_to_df(data_alt)

prompts_base = list(df.prompt)
prompts_alt = list(df_alt.prompt)

prompt_ids_base = list(df.index)
prompt_ids_alt = list(df_alt.index)

assert len(prompts_base) == len(prompts_alt)

prompt_ids = []
prompts = []
for idx in range(len(prompts_base)):

    for _ in range(repeats):
        prompts.append(prompts_base[idx])
        prompts.append(prompts_alt[idx])

        prompt_ids.append(prompt_ids_base[idx])
        prompt_ids.append(prompt_ids_alt[idx])

print(f"Loaded {len(prompts)} combined prompts")
print(prompts)
print(prompt_ids)

input("Press Enter to continue...")

# Warm-up API
try:
    model("Joe Biden")
    sys.exit(1)
except Exception as e:
    print("Warm-up successful!")

# Insert
for results in evaluate_prompts(model, prompts, batch_size=10):
    requests = []
    for idx, row in results.iterrows():
        prompt_id = prompt_ids.pop(0)
        image_id = None

        # Skip if not successful
        if row["success"] == True:
            print(f"Prompt: {prompt_id} created image!")

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
