# Er0manga censorship removal interface

This repo contains code to build docker image to run the whole decensoring pipeline and sets up the gradio-based web interface. Currently, only dark-colored bar censorship is supported for colored and B&W images.

## Quick start:

### Step 0: Install Docker:

If you are using Windows (even if you are using WSL/WSL2): install Docker Desktop directly from Microsoft Store

OR

If you are using Linux: install docker normally

### Step 1: Get docker image:

#### (Easy option) Pull docker image directly from docker hub:

Run in the terminal/PowerShell:

`docker pull er0manga/er0mangademo:latest`

OR

#### (Manual option) build the image yourself:

Clone this repo and run in terminal/PowerShell:

`docker build . -t er0manga`

### Step 2: Run the docker image with web demo:

Open the terminal/PowerShell and if you have an NVIDIA GPU, run:

`docker run --gpus all --rm -it -p 7860:7860 er0manga/er0mangademo`

Otherwise, for CPU-based inference (significantly slower) run:

`docker run --rm -it -p 7860:7860 er0manga/er0mangademo`

### Step 2:

Go to 127.0.0.1:7860 in the browser, upload the image and do some testing!

Notice that you can run `docker run --rm -it -p 7860:7860 --entrypoint /bin/bash er0manga/er0mangademo` to explore and run the code yourself.

## The links to the repos that do the processing:

[https://github.com/Er0manga/Er0mangaSeg](https://github.com/Er0manga/Er0mangaSeg)

[https://github.com/Er0manga/Er0mangaInpaint](https://github.com/Er0manga/Er0mangaInpaint)
