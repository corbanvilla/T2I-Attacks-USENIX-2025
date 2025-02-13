"""
This module contains helper functions for our experiments and analysis.
"""

import sys
from loguru import logger

sys.path.append("..")

import time
import hashlib
import base64
from typing import List, Callable, Optional
from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm

import requests
import numpy as np
import pandas as pd
from openai import BadRequestError

from db import *
from .config import client


SLEEP_TIME = 20


def setup_logger():
    """
    Configure loguru logger with a standard format
    """
    logger.remove()  # Remove default handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
    )
    return logger


# Initialize logger
setup_logger()


def generate_dalle_2(prompt: str) -> object:
    """
    Generate an image with dall-e-2 and return a response object.
    """
    logger.info(f"Querying dalle-2 with prompt hash: {hash_string(prompt)}")
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    return response


def generate_dalle_3(prompt: str) -> object:
    """
    Generate an image with dall-e-3 and download to {path}
    """
    logger.info(f"Querying dalle-3 with prompt hash: {hash_string(prompt)}")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    return response


def generate_dalle_3_extra_prompt(prompt: str) -> object:
    """
    Generate an image with dall-e-3 and download to {path}
    """
    logger.info(f"Querying dalle-3 with prompt hash: {hash_string(prompt)}")
    response = client.images.generate(
        model="dall-e-3",
        prompt="I NEED to test how the tool works with extremely simple NON-ENGLISH prompts. DO NOT add any detail, just use it AS-IS. DO NOT TRANSLATE at all. ONLY use the original language: "
        + prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    return response


def generate_dalle_3_exact_prompt(prompt: str, path: str) -> object:
    """
    Generate an image with dall-e-3 and download to {path}
    """
    logger.info(f"Querying dalle-3 with prompt hash: {hash_string(prompt)}")
    response = client.images.generate(
        model="dall-e-3",
        prompt="I NEED to test how the tool works with extremely simple prompts. TRANSLATE the prompt to English but DO NOT add any detail, just use it AS-IS: "
        + prompt,
        size="1024x1024",
        quality="standard",
        response_format="b64_json",
        n=1,
    )

    return response


def hash_string(input_string: str) -> str:
    """
    Hashes a string using SHA256 and returns the hash as a string.
    """
    # Create a new sha256 hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the bytes of the input string
    hash_object.update(input_string.encode())

    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()

    return hash_hex


def get_binary_hash(input_string: str) -> bytes:
    """
    Hashes a string using SHA256 and returns the binary digest.

    Args:
        input_string: The string to hash

    Returns:
        bytes: The binary SHA256 digest
    """
    hash_object = hashlib.sha256()
    hash_object.update(input_string.encode())
    return hash_object.digest()


def build_templates(components: List[List[str]]):
    """
    Recursive exponential algorithm to build all possible templates
    from a list of components.
    """
    # Base case
    if len(components) == 1:
        return components[0]

    # Recursive case
    level_prompts = components[0]
    child_prompts = build_templates(components[1:])
    ret_prompts = []

    for prompt in level_prompts:
        for child in child_prompts:
            ret_prompts.append(f"{prompt} {child}")

    return ret_prompts


def evaluate_prompts(
    model: Callable[[str, str], object],
    prompts: List[str],
    batch_size=10,
    sleep_time=SLEEP_TIME,
):
    logger.info(f"Evaluating {len(prompts)} prompts!")
    """
    Evaluates a list of prompts on a DALL-E model
    
    Args:
        model: Function that generates images from prompts
        prompts: List of prompts to evaluate
        batch_size: Number of results to accumulate before yielding
        sleep_time: Time to sleep between API calls (in seconds)
    """
    processed = 0
    results = []

    for prompt in prompts:
        prompt_hash = hash_string(prompt)
        logger.info(f"Querying model with prompt hash: {prompt_hash}")
        start_time = time.time()

        success = False
        reported_created = None
        revised_prompt = None
        image_bytes = None
        error = None
        status_code = None

        try:
            # Invoke the language model
            image_response = model(prompt)
            status_code = 200
            success = True
            reported_created = image_response.created
            revised_prompt = image_response.data[0].revised_prompt
            image_bytes = base64.b64decode(image_response.data[0].b64_json)

        except BadRequestError as e:
            # Only allow content policy violation errors
            if e.code != "content_policy_violation":
                raise e

            error = str(e)
            status_code = e.status_code

            logger.warning(
                f"Prompt hash {prompt_hash} triggered content violation policy!"
            )

        end_time = time.time()

        row = {
            # 'hash': prompt_hash,
            "success": success,
            "request_start": start_time,
            "request_end": end_time,
            "reported_created": reported_created,
            "response_time": end_time - start_time,
            "status_code": status_code,
            "error": error,
            "image_bytes": image_bytes,
            "prompt": prompt,
            "revised_prompt": revised_prompt,
        }
        results.append(row)
        processed += 1

        if len(results) == batch_size or processed == len(prompts):
            logger.info(f"Processed {processed}/{len(prompts)} prompts!")
            yield pd.DataFrame(results)
            results = []

        # Don't spam the API
        time.sleep(sleep_time)  # Use the passed in sleep_time


def get_moderation_full(content: str):
    moderation = client.moderations.create(
        input=content, model="text-moderation-stable"
    )

    return moderation


def get_prompt_prefix_id(name: str):
    """
    Fetches a prompt prefix style by name
    """
    prefix = (
        session.query(PromptPrefixStyles)
        .filter(PromptPrefixStyles.name == name)
        .first()
    )

    if prefix is None:
        raise Exception(f"Prompt prefix style {name} not found!")

    return prefix.id


def save_image_from_db(creation_request_id: int, path: str, fail_silent=True):
    """
    Saves an image from the database to the specified path
    """
    request = (
        session.query(Images.bytes)
        .join(
            ImageCreationRequest,
            Images.id == ImageCreationRequest.image_id,
        )
        .filter(ImageCreationRequest.id == creation_request_id)
        .first()
    )

    if request[0] is None:
        if fail_silent is True:
            return
        raise Exception(f"Image creation request {creation_request_id} not found!")

    with open(path, "wb") as f:
        f.write(request.bytes)


def calculate_file_hash(file_path, hash_name="sha256") -> str:
    hash_obj = hashlib.new(hash_name)
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


def calculate_file_hash_from_bytes(file_bytes, hash_name="sha256") -> str:
    hash_obj = hashlib.new(hash_name)
    hash_obj.update(file_bytes)
    return hash_obj.hexdigest()


def remove_outliers_iqr(df, column):
    """
    Remove outliers from a specified column in a Pandas DataFrame using the IQR method.
    """
    # Calculate Q1 (25th percentile) and Q3 (75th percentile)
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Define the bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter the DataFrame to remove outliers
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    logger.info(f"Removed {len(df) - len(df_filtered)} outliers from column '{column}'")

    return df_filtered


def entropy(y):
    """
    Calculate the entropy of a label distribution.
    """
    distribution = Counter(y)
    total_count = len(y)
    probabilities = [count / total_count for count in distribution.values()]
    return -sum(p * np.log2(p) for p in probabilities)


def information_gain(X, y, feature_index, split_value):
    """
    Calculate the information gain for a specific split on a feature.

    Parameters:
    - X: Feature dataset, numpy array of shape (num_samples, num_features)
    - y: Labels, numpy array of shape (num_samples,)
    - feature_index: Index of the feature to split on
    - split_value: Value of the feature to split on

    Returns:
    - Information gain of the split
    """
    # Calculate the entropy before the split
    entropy_before = entropy(y)

    # Split the data based on the feature value
    left_indices = X[:, feature_index] <= split_value
    right_indices = X[:, feature_index] > split_value

    left_y = y[left_indices]
    right_y = y[right_indices]

    # Calculate the entropy after the split
    total_count = len(y)
    left_entropy = entropy(left_y) if len(left_y) > 0 else 0
    right_entropy = entropy(right_y) if len(right_y) > 0 else 0

    entropy_after = (len(left_y) / total_count) * left_entropy + (
        len(right_y) / total_count
    ) * right_entropy

    # Calculate information gain
    info_gain = entropy_before - entropy_after
    return info_gain


def find_best_split(X, y):
    """
    Find the best feature and value to split the dataset on.

    Parameters:
    - X: Feature dataset, numpy array of shape (num_samples, num_features)
    - y: Labels, numpy array of shape (num_samples,)

    Returns:
    - Best feature index to split on
    - Best feature value to split on
    - Information gain of the best split
    """
    best_feature = None
    best_value = None
    best_gain = -1

    num_features = X.shape[1]

    for feature_index in range(num_features):
        unique_values = np.unique(sorted(X[:, feature_index]))

        for value in unique_values:
            gain = information_gain(X, y, feature_index, value)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature_index
                best_value = value

    sorted_best_features = sorted(set(X[:, best_feature]))
    value_after_best = sorted_best_features[sorted_best_features.index(best_value) + 1]
    best_value_median_split = (best_value + value_after_best) / 2

    return best_feature, best_value_median_split, best_gain
