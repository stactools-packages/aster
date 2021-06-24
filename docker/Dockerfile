FROM continuumio/miniconda3

ENV PIP_NO_BINARY rasterio
RUN apt-get update \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN conda update conda && conda install pip

COPY environment.yml /tmp/environment.yml
RUN conda env update -f /tmp/environment.yml -n base && rm /tmp/environment.yml

COPY . /tmp/stactools-aster
RUN cd /tmp/stactools-aster && pip install . && rm -rf /tmp/stactools-aster

ENTRYPOINT [ "python", "-m", "stactools.cli" ]
