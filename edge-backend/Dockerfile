FROM gleissonbezerra/arm32v7-opencv451-python:3.9 as base

EXPOSE 8123

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED=1

FROM base AS runtime

RUN apt-get update \
    && apt-get install -y zlib1g-dev \
    && apt-get install -y libjpeg-dev \
    && apt-get install -y \
    cmake \
    build-essential \
    curl \
    g++ \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . $HOME/.cargo/env \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip

RUN useradd --create-home sodavision
WORKDIR /home/sodavision

COPY . .
RUN pip install --upgrade pip

RUN pip install -r requirements.txt

VOLUME ["/home/sodavision/app/core/data/temp_files"]

RUN chmod +x /home/sodavision/get_ip.sh

ENTRYPOINT [ "/home/sodavision/get_ip.sh" ]
