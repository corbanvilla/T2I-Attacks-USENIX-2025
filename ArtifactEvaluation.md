# Artifact Evaluation Guide

## Major Claims

1. **[E1]** We present the first reverse-engineering of the black-box cascading safety guardrails in DALL·E models using a novel time-based side-channel, providing insights into a multi-stage filtering process, identifying previously unknown blocking or modifying filters, and enabling a feedback channel that adaptive attacks may exploit.
2. **[E1,E2]** We synthesize key takeaways for T2I system security by juxtaposing safety mechanisms present in DALL·E 2 and DALL·E 3, notably the incorporation of an LLM-based implicit filter in DALL·E 3 to soften harmful prompts, in contrast to the conventional blocklist and similarity-based filtering in DALL·E 2.
3. **[E3]** We introduce novel jailbreaking attacks specific to T2I models, namely T2I negation and low-resource-language attacks, which exploit the limitations of safety filters in handling negated phrases and less common languages.

## Dependencies

1. A commodity computer:
  - 2+ CPU cores
  - 4GB+ memory
  - 1GB+ disk storage
  
2. **(Recommended)** A Linux-based operating system:
  - Validated with `Ubuntu 22.04`.
  - Compatibility with other operating systems may vary.

3. [`docker` and `docker compose`](https://docs.docker.com/engine/install/ubuntu/):
  - Validated with version `27.3.1`.

## Setup

All code and experimental analysis executes in containers. To setup the repository, simply clone the repository:

```bash
git clone https://github.com/corbanvilla/T2I-Attacks-USENIX-2025.git
cd T2I-Attacks-USENIX-2025
```

## Artifact Evaluation: `Artifacts Available`

Artifact availability has already been verified using the comprehensive dataset collected, following the instructions in [README.md](README.md#setup).

## Artifact Evaluation: `Results Reproduced`

To reproduce the major results of the paper, we include three key experiments that demonstrate the effectiveness of our attacks on DALL·E models. To ensure reasonable time and costs to reproduce, these experiments are conducted with a subset of prompts used in the full evaluation.

### Running Experiment Data Collection

To run all experiments and collect the required dataset for analysis, run the following commands. Experiments are estimated to require **30-45 minutes to complete.** Please allow the experiments to **run continuously and uninterrupted to completion** in order to minimize the potential for variation in the DALL·E system performance.

```bash
# Clean up prior database instances:
./scripts/clean-data.sh  

# Run the evaluation script:
./scripts/artifact-evaluation.sh
```

> **Note:** We recommend you run the evaluation script in a `tmux` or `screen` session to prevent interruptions. 

The experiments are complete once you see the following message:
```
✅ Artifact evaluation completed
```

To evaluate the experimental results, access the Jupyter notebook at:
- [http://127.0.0.1:8888/lab?token=T2I-USENIX-rubpGTNAzgd4tgk7npb](http://127.0.0.1:8888/lab?token=T2I-USENIX-rubpGTNAzgd4tgk7npb)
  > 
  > - If you encounter issues connecting, please ensure that your browser did not upgrade the connection protocol to HTTPS.
  >

### Experiment 1: DALL·E 2 Blocklist Probing

**Description:** This experiment demonstrates the effectiveness of our DALL·E 2 blocklist probing attack, which allows an attacker to detect independent filter systems by their respective response times (§5.1). 

**Dataset:** This experiment uses 5 pairs of blocklisted and mutated words, repeated 5 times each, for a total of 50 requests to DALL·E 2.

**Success Criteria:** The experiment demonstrates the statistical significance between rejection timings.

**Results:** To validate our blocklist probing side-channel attacks:

1. Open `src/artifact_evaluation/1-timing-side-channel.ipynb` in the Jupyter notebook. 
2. Select `Run All Cells` from the `Run` menu.
3. Validate the final cell demonstrates statistical significance.


### Experiment 2: Quantifying Prompt Softening

**Description:** This experiment quantifies the effect of the LLM prompt revision prompt as an implicit filtering mechanism in DALL·E 3 using two key metrics: Toxicity Absolute Change and Toxicity Theme Similarity (§3.3).

**Dataset:** This experiment uses 5 prompts in 4 languages (Hawaiian, Lao, Nepali, Sinhala) for a total of 20 requests to DALL·E 3. Prompts and revised prompts are evaluated for toxicity using the OpenAI Moderation API.

**Success Criteria:** The experiment demonstrates that the prompt revision model "softens" the toxicity of harmful prompts to various degrees of success under multilingual inputs.

**Results:** To validate our prompt softening claims:

1. Open `src/artifact_evaluation/2-prompt-softening.ipynb` in the Jupyter notebook.
2. Select `Run All Cells` from the `Run` menu.
3. Validate the final cell demonstrates various toxicity change and similarity decreases, with the magnitude of change dependent on the respective language.


### Experiment 3: Low-Resource Language Attacks

**Description:** This experiment demonstrates that low-resource languages can be used as an effective mechanism to bypass DALL·E safety filters (§6.1).

**Dataset:** This experiment uses 5 prompts in 5 languages (English, Nepali, Sinhala, Lao, Hawaiian) for a total of 25 requests to DALL·E 3.

**Success Criteria:** Languages with fewer pages in the Common Crawl dataset often demonstrating higher prompt acceptance rates.

**Results:** To validate our low-resource language attacks:

1. Open `src/artifact_evaluation/3-low-resource-lang-attack.ipynb` in the Jupyter notebook.
2. Select `Run All Cells` from the `Run` menu.
3. Validate the final cell depicts various language bypass rates.
