FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y vim git zip unzip wget mc tmux nano build-essential rsync libgl1

RUN wget https://mega.nz/linux/repo/xUbuntu_18.04/amd64/megacmd-xUbuntu_18.04_amd64.deb && apt install -y "$PWD/megacmd-xUbuntu_18.04_amd64.deb" && rm  "$PWD/megacmd-xUbuntu_18.04_amd64.deb"

ARG USERNAME=user
RUN apt-get install -y sudo && \
    addgroup --gid 1000 $USERNAME && \
    adduser --uid 1000 --gid 1000 --disabled-password --gecos '' $USERNAME && \
    adduser $USERNAME sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers && \
    USER=$USERNAME && \
    GROUP=$USERNAME

USER $USERNAME:$USERNAME
WORKDIR "/home/$USERNAME"
ENV PATH="/home/$USERNAME/miniconda3/bin:/home/$USERNAME/.local/bin:${PATH}"

RUN wget -O /tmp/miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh && \
    echo "536817d1b14cb1ada88900f5be51ce0a5e042bae178b5550e62f61e223deae7c /tmp/miniconda.sh" > /tmp/miniconda.sh.sha256 && \
    sha256sum --check --status < /tmp/miniconda.sh.sha256 && \
    bash /tmp/miniconda.sh -bt -p "/home/$USERNAME/miniconda3" && \
    rm /tmp/miniconda.sh && \
    conda build purge && \
    conda init

RUN conda install -n base --override-channels -c conda-forge mamba 'python_abi=*=*cp*'

ENV TORCH_HOME="/home/$USERNAME/.torch"


RUN git clone --recursive https://github.com/Er0manga/Er0mangaSeg.git
RUN git clone --recursive https://github.com/Er0manga/Er0mangaInpaint.git


RUN mega-get "https://mega.nz/file/NNQTgR4Q#MuqoCZACOc9pBZ5BzafszLqa0MEnI65KJx4PXqgjV-k" "/home/$USERNAME/Er0mangaSeg/pretrained/"
RUN mega-get "https://mega.nz/file/gRYn2CBJ#HZ73lqn5noX_t2eyfIaDk7sIDfnGQ9gBwClJ6O3VdTE" "/home/$USERNAME/Er0mangaInpaint/pretrained/"
RUN unzip "/home/$USERNAME/Er0mangaInpaint/pretrained/00-30-09.zip" -d "/home/$USERNAME/Er0mangaInpaint/pretrained/"

RUN mamba env create -f "/home/$USERNAME/Er0mangaSeg/env.yml"

RUN mkdir "/home/$USERNAME/gradio_app"
COPY gradio_app "/home/$USERNAME/gradio_app"
COPY entrypoint.sh "/home/$USERNAME/"

EXPOSE 7860


ENTRYPOINT ["/bin/bash", "/home/user/entrypoint.sh"]



