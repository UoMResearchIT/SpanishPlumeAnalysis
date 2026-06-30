FROM mambaorg/micromamba:1.5.8

COPY environment.yml /tmp/environment.yml

RUN micromamba create -y -n wrf-py-env -f /tmp/environment.yml \
    && micromamba run -n wrf-py-env python -m pip install --no-cache-dir pytest coverage \
    && micromamba clean --all --yes

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Ensure container commands execute inside the project environment.
ENV ENV_NAME=wrf-py-env

WORKDIR /memory
WORKDIR /wrf-analysis
COPY wrf_analysis_toolkit_cli.py /wrf-analysis/wrf_analysis_toolkit_cli.py
COPY wrf_analysis_toolkit /wrf-analysis/wrf_analysis_toolkit
COPY tests /wrf-analysis/tests
COPY pytest.ini /wrf-analysis/pytest.ini

CMD ["python", "-u", "wrf_analysis_toolkit_cli.py"]
