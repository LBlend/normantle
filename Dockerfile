# syntax=docker/dockerfile:1

FROM python:3.15-slim AS model

ARG MODEL_URL=https://dl.furumo.eu/93_filtered_v2.zip
ARG MODEL_SHA256=81ea150b00b44b88688a34d822dad84966e6a88c42944f523205fedfeb9c0677
ADD --checksum=sha256:${MODEL_SHA256} ${MODEL_URL} /tmp/model.zip
RUN python -m zipfile -e /tmp/model.zip /model

FROM python:3.15-slim AS build

COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-dev --no-install-project

FROM python:3.15-slim

RUN useradd --system --no-create-home --uid 10001 normantle

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 TZ=Europe/Oslo \
    FORWARDED_ALLOW_IPS="127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,fc00::/7"

COPY --from=build /app/.venv /app/.venv
COPY --from=model /model /app/model
COPY src /app/src

USER normantle

EXPOSE 5000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers"]
