#!/usr/bin/env python3

import sys
from collections import Counter

sys.path.append("..")

from db import *
from analysis import *
from blackbox.helpers import (
    evaluate_prompts,
    generate_dalle_2,
    get_prompt_prefix_id,
    calculate_file_hash_from_bytes,
    logger,
    SLEEP_TIME,
)

model_name = "dalle-2"
model = generate_dalle_2
repeats = 5

prompt_prefix_id = get_prompt_prefix_id("none")
logger.info(f"{prompt_prefix_id=}")

"""
Select the prompt dataset to use
"""
offset = 0
limit = 50

# Calculate total experiment duration
total_requests = limit * repeats * 2  # times 2 because we have base and alt prompts
total_seconds = total_requests * SLEEP_TIME
total_minutes = total_seconds // 60
remaining_seconds = total_seconds % 60
logger.info(
    f"Experiment will take approximately {total_minutes} minutes and {remaining_seconds} seconds"
)

data = (
    session.query(Prompts.id, Prompts.prompt)
    .filter(
        Prompts.dataset == "blocklist",
    )
    .limit(limit)
    .offset(offset)
)

data_alt = (
    session.query(Prompts.id, Prompts.prompt)
    .filter(
        Prompts.dataset == "blocklist_mutate",
    )
    .limit(limit)
    .offset(offset)
)

df = query_to_df(data)
df_alt = query_to_df(data_alt)

prompts_base = list(df.prompt)
prompts_alt = list(df_alt.prompt)

prompt_ids_base = list(df.index)
prompt_ids_alt = list(df_alt.index)

assert len(prompts_base) == len(prompts_alt)

prompts = []
prompt_ids = []
for idx in range(len(prompts_base)):
    for _ in range(repeats):
        prompts.append(prompts_base[idx])
        prompts.append(prompts_alt[idx])
        prompt_ids.append(prompt_ids_base[idx])
        prompt_ids.append(prompt_ids_alt[idx])

# Check for existing requests
existing_requests = (
    session.query(ImageCreationRequest.prompt_id)
    .filter(
        ImageCreationRequest.model == model_name,
        ImageCreationRequest.prompt_id.in_(prompt_ids_base + prompt_ids_alt),
        ImageCreationRequest.prompt_prefix_id == prompt_prefix_id,
    )
    .all()
)

# Count occurrences of each prompt_id
completed_counts = Counter(r.prompt_id for r in existing_requests)

# Remove completed prompts from the lists
indices_to_remove = []
for i, (prompt_id, prompt) in enumerate(zip(prompt_ids, prompts)):
    if completed_counts[prompt_id] > 0:
        indices_to_remove.append(i)
        completed_counts[prompt_id] -= 1

# Remove in reverse order to maintain correct indices
for i in reversed(indices_to_remove):
    prompt_ids.pop(i)
    prompts.pop(i)

logger.info(
    f"Loaded {len(prompts)} prompts that still need processing "
    f"({len(indices_to_remove)} already processed!)"
)
if len(prompts) == 0:
    logger.info("All prompts in this range have been processed successfully")
    sys.exit(0)

# Warm-up API
try:
    model("Joe Biden")
    sys.exit(1)
except Exception as e:
    logger.info("Warm-up successful!")

# Insert
for results in evaluate_prompts(model, prompts, batch_size=2):
    requests = []
    for idx, row in results.iterrows():
        prompt_id = prompt_ids.pop(0)
        image_id = None

        # Skip if not successful
        if row["success"] == True:
            logger.info(f"Prompt: {prompt_id} created image!")

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
    logger.info(f"Inserted batch of {len(requests)} records")
