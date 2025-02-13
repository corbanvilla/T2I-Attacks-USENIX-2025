#!/usr/bin/env python3

import sys

sys.path.append("..")

from db import *
from analysis import *
from blackbox.helpers import (
    evaluate_prompts,
    generate_dalle_3,
    get_prompt_prefix_id,
    calculate_file_hash_from_bytes,
    get_binary_hash,
    logger,
    SLEEP_TIME
)

model_name = "dalle-3"
model = generate_dalle_3

# Added offset and limit parameters
offset = 0
limit = 25

# Calculate total experiment duration
total_requests = limit
total_seconds = total_requests * SLEEP_TIME
total_minutes = total_seconds // 60
remaining_seconds = total_seconds % 60
logger.info(
    f"Experiment will take approximately {total_minutes} minutes and {remaining_seconds} seconds"
)

prompt_prefix_id = get_prompt_prefix_id("none")
logger.info(f"{prompt_prefix_id=}")

"""
Select the prompt dataset to use
"""
data = (
    session.query(
        TranslatedPrompts.id.label("translated_prompt_id"),
        TranslatedPrompts.prompt_translation,
    )
    .join(Prompts, TranslatedPrompts.prompt_id == Prompts.id)
    .filter(
        Prompts.dataset == "baseline",
    )
    .limit(limit)
    .offset(offset)
)
df = query_to_df(data)
prompts = list(df.prompt_translation)
translated_prompt_ids = list(df.translated_prompt_id)

# Check for existing successful requests
existing_requests = (
    session.query(ImageCreationRequest.translated_prompt_id)
    .filter(
        ImageCreationRequest.model == model_name,
        ImageCreationRequest.translated_prompt_id.in_(translated_prompt_ids),
        ImageCreationRequest.prompt_prefix_id == prompt_prefix_id,
    )
    .distinct()
)

completed_prompt_ids = [r.translated_prompt_id for r in existing_requests]
remaining_indices = [
    i for i, pid in enumerate(translated_prompt_ids) if pid not in completed_prompt_ids
]

# Filter prompts and prompt_ids to only include remaining work
prompts = [prompts[i] for i in remaining_indices]
translated_prompt_ids = [translated_prompt_ids[i] for i in remaining_indices]

logger.info(
    f"Loaded {len(prompts)} prompts that still need processing ({len(completed_prompt_ids)} already processed!)"
)
if len(prompts) == 0:
    logger.info("All prompts in this range have been processed successfully")
    sys.exit(0)


# Insert
for results in evaluate_prompts(model, prompts, batch_size=2):
    requests = []
    for idx, row in results.iterrows():
        translated_prompt_id = translated_prompt_ids.pop(0)
        image_id = None
        revised_prompt_hash = None
        # Skip if not successful
        if row["success"] == True:
            print(f"Prompt: {translated_prompt_id} successfully created an image!")

            # Store the image itself
            image_bytes = row["image_bytes"]
            revised_prompt_hash = get_binary_hash(row["revised_prompt"])
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
            translated_prompt_id=translated_prompt_id,
            prompt_prefix_id=prompt_prefix_id,
            image_id=image_id,
            **row,
        )
        requests.append(request)

    session.bulk_save_objects(requests)
    session.commit()
    print(f"Inserted batch of {len(requests)} records")
