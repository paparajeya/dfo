FROM python:3.12.3-slim-bullseye

# Set the working directory
WORKDIR /app

# Run the update and install the required packages
RUN apt update && \
    apt upgrade -y

# Create virtual env
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy the pyproject.toml file to the working directory
COPY pyproject.toml ./

# Install the poetry package
RUN pip install -U pip && \
    pip install poetry && \
    poetry install

# Copy the source code
COPY ./dfo/ ./start.sh /app/

# Run the start.sh script
CMD ["sh", "start.sh"]