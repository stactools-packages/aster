ARG STACTOOLS_VERSION=latest
FROM stacutils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/aster

# For caching purposes, install dependencies but remove the actual package
COPY pyproject.toml setup.cfg ./
COPY src/stactools/aster/__init__.py src/stactools/aster/
RUN pip install . \
    && rm -r /opt/conda/lib/python3.8/site-packages/stactools/aster

COPY src ./src
RUN pip install .
