# Lock commit for python-3.12.8 on 2025-01-28
# https://quay.io/repository/jupyter/datascience-notebook?tab=tags
FROM quay.io/jupyter/datascience-notebook@sha256:65c24a2f9a58a5d328c3fa0a3ad12fa2f3523c575e7b800bcfef342f482666e9

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./run-artifact-evaluation.sh /run-artifact-evaluation.sh
