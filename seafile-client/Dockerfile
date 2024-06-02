ARG TARGET=unstable
FROM debian:${TARGET}-slim

ARG UID
ARG GID
ENV UID 1000
ENV GID 1000
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install \
        --no-install-recommends \
        --yes \
            seafile-cli \
            oathtool \
            ca-certificates \
            gnupg \
            sudo \
            # procps \
            iputils-ping \
            && \
    apt-get clean && apt-get autoclean && \
    rm -rf \
        /var/log/fsck/*.log \
        /var/log/apt/*.log \
        /var/cache/debconf/*.dat-old \
        /var/lib/apt/lists/* && \
    groupmod -g 90 users

COPY --chmod=755 entrypoint-docker.sh /entrypoint.sh
COPY issue /etc/issue

RUN echo '[ ! -z $TERM ] && cat /etc/issue' >> /root/.bashrc && \
    groupadd --gid $GID seafile && \
    useradd --uid $UID --gid $GID --shell /bin/bash --create-home seafile && \
    mkdir /library /seafile && \
    chown seafile:seafile /seafile /library && \
    apt-cache show seafile-cli | grep 'Version: ' | awk '{print $2}' > /SEAFILE_VERSION

COPY --chmod=755 --chown=seafile:seafile entrypoint-seafile.py /home/seafile/entrypoint.py

ARG CREATED
ARG REVISION
ARG VERSION
LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.authors="flow.gunso@gmail.com"
LABEL org.opencontainers.image.url="https://hub.docker.com/r/flowgunso/seafile-client"
LABEL org.opencontainers.image.documentation="https://gitlab.com/florian.anceau/docker-seafile-client"
LABEL org.opencontainers.image.source="https://gitlab.com/florian.anceau/docker-seafile-client"
LABEL org.opencontainers.image.version=${VERSION}
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.title="Seafile Docker client"
LABEL org.opencontainers.image.description="Sync Seafile librairies within Docker containers."

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/home/seafile/entrypoint.py"]
HEALTHCHECK \
    CMD ["/entrypoint.sh", "/home/seafile/entrypoint.py", "--healthcheck"]