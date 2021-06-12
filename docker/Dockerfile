FROM stacutils/stactools:0.2.1a1

WORKDIR /opt/aster
COPY src ./src
COPY pyproject.toml setup.cfg ./
RUN pip install --no-deps .
