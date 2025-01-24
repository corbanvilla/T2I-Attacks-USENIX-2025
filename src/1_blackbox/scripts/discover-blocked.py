#!/usr/bin/env python3

"""
This script is used to discover which prompts are blocked by OpenAI's API.

It is meant to be invoked as a standalone Python script.
"""

import time
import pandas as pd
import sys

sys.path.append("..")
sys.path.append(".")

from db import *
from analysis import *
from helpers import (
    generate_dalle_2,
)

with open("../prompts/blocked.txt") as f:
    prompts = [line.strip() for line in f]

# Skip the first 15 prompts
prompts = prompts[15:]

results = []

# Prime
try:
    generate_dalle_2("Joe Biden")
    sys.exit(1)
except Exception as e:
    print("Warm-up successful!")

print(f"Running {len(prompts)} prompts")
input("Press Enter to continue...")

for prompt in prompts:
    start = time.time()
    try:
        generate_dalle_2(prompt)
    except Exception as e:
        # print(e)
        print(f'"{prompt}" blocked!')
        pass
    end = time.time()

    print(f"Time to run: {end - start:.4f} seconds")

    results.append(
        {
            "prompt": prompt,
            "time": end - start,
        }
    )

    # Don't spam the api
    time.sleep(3)

pd.DataFrame(results).to_csv("blocked.csv", index=False)
