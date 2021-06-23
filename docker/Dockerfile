ARG STACTOOLS_VERSION=latest
FROM stacutils/stactools:$STACTOOLS_VERSION

WORKDIR /opt/aster
COPY src ./src
COPY pyproject.toml setup.cfg ./
RUN pip install --no-deps .
