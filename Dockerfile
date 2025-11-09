FROM debian:trixie-slim

ARG USERNAME=vip
ARG USER_UID=1000
ARG USER_GID=$USER_UID

ENV DEBIAN_FRONTEND=noninteractive
ENV REPO_ROOT=/home/vip/cps-cosimulation-env

RUN apt-get update && apt-get install -y \
    build-essential \
    cargo \
    cmake \
    curl \
    extra-cmake-modules \
    gdb \
    git \
    libboost-dev \
    libczmq-dev \
    libncurses-dev \
    rustc \
    sudo \
    valgrind \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create the non-root user and grant sudo privileges
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(ALL\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to the non-root user
USER $USERNAME
WORKDIR $REPO_ROOT

# Install uv
RUN curl -LfsS https://astral.sh/uv/install.sh | sh

# This will automatically source .venv (after it's created by setup.sh)
RUN echo '. $REPO_ROOT/.venv/bin/activate 2>/dev/null' >> ~/.bashrc

# Change the uv cache to be in the project's directory. Fixes an issue where uv
# can't hardlink a file in the uv cache since it isn't in the shared volume.
ENV UV_CACHE_DIR="$REPO_ROOT/.cache"

# Set the PATH to include the manually built HELICS and Gridlab-D binaries
ENV PATH="$PATH:$REPO_ROOT/install/HELICS/bin:$REPO_ROOT/install/gridlab/bin"

CMD ["/bin/bash"]
