# T2I Attacks and Countermeasures

This repository contains the code, dataset, and analysis for the USENIX 2025 paper: [Exposing the Guardrails: Reverse-Engineering and Jailbreaking Safety Filters in DALL·E Text-to-Image Pipelines](). 



[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14754827.svg)](https://doi.org/10.5281/zenodo.14754827)



## Artifact Evaluation (Phase 2: Reproducible)

Find details on reproducing the results in [ArtifactEvaluation.md](ArtifactEvaluation.md) section.


## Project Overview

Relevant artifacts are organized into the following key directories:

```js
T2I Attacks
├── README.md
├── ArtifactEvaluation.md   // Detailed instructions on reproducing key results.
├── docker-compose.yml      // Database and Jupyter notebook environment.
├── datasets
│   ├── graybox             // Dataset collected from the ChatGPT/Interface.
│   ├── postgres            // All experiment data (prompts, response times, requests, etc).
│   └── prompts             // Image prompts used in the experiments.
└── src
    ├── artifact_evaluation // Scripts to conduct artifact evaluation experiments.
    ├── examples.ipynb      // Notebook with example queries for the database.
    └── paper               // Notebook files to reproduce the paper results.
```


## Setup

Start by cloning the repository:
```bash
git clone https://github.com/corbanvilla/T2I-Attacks-USENIX-2025.git
cd T2I-Attacks-USENIX-2025
```

To setup the project environment, execute the following script:

```bash
./scripts/setup.sh
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
  > 
  > If you encounter issues connecting, please ensure that your browser did not upgrade the connection protocol to HTTPS.
  >


## Dataset Tutorials

To begin exploring the database, please refer to the following Jupyter notebooks:

- **Basic Query Syntax:** [`src/examples.ipynb`](src/examples.ipynb)
- **Reproduce Paper Results:** [`src/paper`](src/paper)


## Cite Us

```bibtex
@inproceedings{villaExposingGuardrailsReverseEngineering2025,
  title = {Exposing the {{Guardrails}}: {{Reverse-Engineering}} and {{Jailbreaking Safety Filters}} in {{DALL·E Text-to-Image Pipelines}}},
  booktitle = {34th {{USENIX Security Symposium}}},
  author = {Villa, Corban and Mirza, Shujaat and P{\"o}pper, Christina},
  year = {2025},
  pages = {},
  isbn = {}
}
```

## Encrypted Prompts

In accordance with ethical standards set by prior work [[1](https://github.com/Yuchen413/text2image_safety),[2](https://github.com/YitingQu/unsafe-diffusion)], we have encrypted the toxic prompts utilized in our experiments (`datasets/prompts/prompts.zip`, `datasets/postgres/unredacted.sql.zip`). The encryption key is available upon request (corban.villa@nyu.edu).

Harmful prompts in the database (`datasets/postgres/redacted.sql`) are nulled out to prevent unintentional exposure, and include a corresponding prompt hash field that allows for pseudonymous identification for database joins.

To decrypt the prompts with the provided decryption key, please execute the following script:
```bash
./scripts/decrypt.sh
```


## Ethical Considerations

We do not cause harm to the T2I systems as we are using them as a regular user within the existing rate limits. The nature of this work, however, introduces the potential exposure to harmful content through both text-based prompts and images generated. In order to minimize this potential harm, the authors of this work are the only ones subject to interacting with these artifacts. In addition, automation is employed when possible to minimize the extent and scale of interaction with harmful content. This methodology is consistent with previous work [[1](https://github.com/Yuchen413/text2image_safety),[2](https://github.com/YitingQu/unsafe-diffusion)].

While we do propose a number of novel attacks for T2I systems, we also introduce a number of countermeasures that mitigate these new vulnerabilities. We intend this work to provide a robust basis for safety guardrails to build upon, providing an increased degree of safety.

## Open Science

All code and timing dataset artifacts related to this work will be published. A permanent and immutable version of these are available at: [https://doi.org/10.5281/zenodo.14754827](https://doi.org/10.5281/zenodo.14754827).

## License

This project is licensed under the [MIT License](LICENSE).

