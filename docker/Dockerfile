FROM stacutils/stactools:0.2.1a0

WORKDIR /opt/aster
COPY src ./src
COPY pyproject.toml setup.cfg ./
RUN pip install --no-deps .
