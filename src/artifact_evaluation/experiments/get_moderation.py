#!/usr/bin/env python3

import sys

sys.path.append("..")

import time

from db import *
from analysis import *
from blackbox.helpers import get_moderation_full, get_binary_hash, logger


def insert_moderation_records(prompts):
    """
    Loop through a provided list of prompts
    and insert a moderation record for each one.
    """
    moderation_requests = []
    for idx, prompt in enumerate(prompts):
        logger.info(f"Processing prompt {idx} of {len(prompts)}")

        # Sleep 1 for the API
        time.sleep(1)

        # Fetch a moderation response from API
        start = time.time()
        req = get_moderation_full(prompt)
        scores = {
            k: v
            for k, v in dict(req.results[0].category_scores).items()
            if v is not None  # some removed categories have None values
        }
        end = time.time()
        elapsed = end - start

        # Build and append record
        moderation_request = ModerationRequest(
            prompt=prompt,
            request_id=req.id,
            model=req.model,
            request_start=start,
            request_end=end,
            response_time=elapsed,
            flagged=req.results[0].flagged,
            categories=dict(req.results[0].categories),
            category_scores=list(scores.values()),
            prompt_hash=get_binary_hash(prompt),
        )
        moderation_requests.append(moderation_request)

    session.bulk_save_objects(moderation_requests)
    session.commit()
    logger.info(f"Inserted batch of {len(moderation_requests)} records")


# Select all basic prompts that have not been moderated
query = (
    session.query(Prompts)
    .outerjoin(ModerationRequest, Prompts.prompt == ModerationRequest.prompt)
    .filter(ModerationRequest.id == None)
)
df = query_to_df(query)
if df is not None:
    prompts = set(df["prompt"])
    logger.info(f"Requesting moderation for {len(prompts)} prompts")
    insert_moderation_records(prompts)

# Select all prompt translations that have not been moderated
query = (
    session.query(TranslatedPrompts)
    .outerjoin(
        ModerationRequest,
        TranslatedPrompts.prompt_translation == ModerationRequest.prompt,
    )
    .filter(ModerationRequest.id == None)
)
df = query_to_df(query)
if df is not None:
    prompts = set(df["prompt_translation"])
    logger.info(f"Requesting moderation for {len(prompts)} prompt translations")
    insert_moderation_records(prompts)

# Select all revised prompts from image creation requests
query = (
    session.query(ImageCreationRequest)
    .outerjoin(
        ModerationRequest,
        ImageCreationRequest.revised_prompt == ModerationRequest.prompt,
    )
    .filter(ImageCreationRequest.revised_prompt != None, ModerationRequest.id == None)
)
df = query_to_df(query)
if df is not None:
    prompts = set(df["revised_prompt"])
    logger.info(
        f"Requesting moderation for {len(prompts)} revised prompts from image creation requests"
    )
    insert_moderation_records(prompts)
