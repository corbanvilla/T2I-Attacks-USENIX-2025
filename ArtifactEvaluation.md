# Artifact Evaluation (In-Progress)

**Note:** The Artifact Evaluation for Reproducibility is currently in-progress, pending [**Phase-2**](https://secartifacts.github.io/usenixsec2025/instructions#phase-2-artifacts-functional--results-reproducible) guidelines.

## Major Claims

1. **[E1-E5]** We present the first reverse-engineering of the black-box cascading safety guardrails in DALL·E models using a novel time-based side-channel analysis, providing insights into the multi-stage filtering process, and identifying previously unknown blocking or modifying filters.
2. **[E1-E3]** We uncover key differences in safety mechanisms between DALL·E 2 and DALL·E 3, notably the incorporation of an LLM-based implicit filter in DALL·E 3 to soften harmful prompts, in contrast to the conventional blocklist and similarity-based filtering in DALL·E 2.
3. **[E4-E5]** We introduce novel jailbreaking attacks specific to T2I models, namely low-resource-language and negation attacks, which exploit the limitations of safety filters in handling less common languages and negated phrases.
4. **[E1-E4]** We provide an actionable list of countermeasure recommendations for T2I systems to prevent the attacks, and enumerate directions for future defense research.

## Dependencies

1. A commodity computer:
  - 4+ CPU cores
  - 8GB+ memory
  - 10GB+ disk storage
  
2. **(Recommended)** A Linux-based operating system:
  - Validated with `Ubuntu 24.04`.
  - Compatibility with other operating systems may vary.

3. [`docker` and `docker compose`](https://docs.docker.com/engine/install/ubuntu/):
  - Validated with version `27.3.1`.

## Setup

Start by cloning the repository:
```bash
git clone https://github.com/corbanvilla/T2I-Attacks-USENIX-2025.git
cd T2I-Attacks-USENIX-2025
```

To setup the project environment, execute the following script:

```bash
./setup.sh
```

Load the PostgreSQL database dump:
```bash
docker compose up -d postgres
docker compose logs -f postgres # CTRL-C to exit
```

The database is ready when you see the following message:
```
...
postgres  | 2025-01-23 08:56:56.333 UTC [1] LOG:  database system is ready to accept connections
```

Load the Jupyter notebook:
```bash
docker compose up -d notebook
docker compose logs -f notebook # CTRL-C to exit
```

The notebook is ready when you see the following message:
```
...
Jupyter Server 2.15.0 is running at:
http://127.0.0.1:8888/lab?token=...
...
```

Access the Jupyter notebook at the provided address: 
- [http://127.0.0.1:8888/lab?token=T2I-USENIX-rubpGTNAzgd4tgk7npb](http://127.0.0.1:8888/lab?token=T2I-USENIX-rubpGTNAzgd4tgk7npb)

## Evaluation

### Independent Dataset Collection

Prior to our experiments, we collect a small independent sample dataset to compare with our more extensive dataset.

- **DALL·E 2:** 100x requests ($0.020/image * 100 images = $2)
  - **[50 requests]** blocklist probing: 5 words * 5 requests * 2 variants
    - blocklist statistical significance
  - **[50 requests]** low-resource-language: 5 languages * 10 prompts
    - language bypass rates
    - response time distribution
- **DALL·E 3:** 100x requests ($0.040/image * 100 images = $4)
  - **[30 requests]** low-resource-languages: 10 english, 10 zulu, 10 hawaiian
    - language bypass rates
    - prompt softening
    - response time distribution
  - **[20 requests]** negation attacks: 10 negated, 10 non-negated
    - negation attacks

### Experiment 1: DALL·E 2 Blocklist Probing

- Sample Analysis
- Full Analysis
- Applicable Countermeasures

### Experiment 2: Black-box Timing (DALL·E 3/API)

- Sample Analysis
- Full Analysis
- Applicable Countermeasures

### Experiment 3: Gray-box Timing (DALL·E 3/ChatGPT)

- No Sample Analysis
- Full Analysis
- Applicable Countermeasures

### Experiment 4: Low-Resource Language Attacks

- Sample Analysis
- Full Analysis
- Applicable Countermeasures

### Experiment 5: Negation Attacks

- Sample Analysis
- Full Analysis
- Applicable Countermeasures
