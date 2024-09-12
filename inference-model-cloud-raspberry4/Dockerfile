FROM python:3.10-slim as base

EXPOSE 9999

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y zlib1g-dev \
    && apt-get install -y libjpeg-dev \
    && apt-get install -y \
    cmake \
    build-essential \
    curl \
    g++ \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    # && . $HOME/.cargo/env \
    && rm -rf /var/lib/apt/lists/*

# ENV PATH="/root/.cargo/bin:${PATH}"

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

VOLUME ["/workspace/app/data"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9999"]
