# cuda-python

This Docker image is built on top of the `nvidia/cuda` image.

It installs the following element(s) on top:

python

## Tag Format

Tags follow this format : `{CUDA_TAG}-python{PYTHON_VERSION}`.

## Dockerhub

These images can be found in Dockerhub through the following link:

[https://hub.docker.com/repository/docker/ismailbouajaja/cuda-python/general](https://hub.docker.com/repository/docker/ismailbouajaja/cuda-python/general)

## Clone repository

To clone the github repository containing the Dockerfile used, follow these steps :

1. Clone the repository [https://github.com/bouajajais/cuda-python.git](https://github.com/bouajajais/cuda-python.git):
    ```bash
    git clone https://github.com/bouajajais/cuda-python.git
    ```

2. Navigate to the project directory:
    ```bash
    cd cuda-python
    ```

2. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build -t cuda-python .
    ```

    The `docker build` command accepts the following arguments:
    - `ARG CUDA_TAG=12.6.1-cudnn-devel-ubuntu22.04`: The CUDA base image tag.
    - `ARG PYTHON_VERSION=3.12`: The Python version to install.

3. Run the Docker container:
    ```bash
    docker run --rm -it cuda-python bash
    ```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.