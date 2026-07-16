# Multi-language, network-disabled-at-runtime sandbox for NEBians Background Agent.
# Build from the backend root:
#   docker build -t nebians-background-agent-sandbox:latest docker/background-agent
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash ca-certificates curl git openssh-client unzip zip jq ripgrep \
       build-essential cmake make pkg-config \
       python3 python3-pip python3-venv python3-pytest python-is-python3 \
       nodejs npm \
       openjdk-21-jdk-headless maven gradle \
       golang-go cargo rustc \
       ruby-full ruby-bundler php-cli composer \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory '*'

RUN npm install -g pnpm yarn \
    && npm cache clean --force

WORKDIR /workspace
ENTRYPOINT []
CMD ["python", "--version"]
