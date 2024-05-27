# cuda-python

Based on NVIDIA's cuda images, it adds python on top.

## Available tags

Tags reflect the image of cuda used and the version of python added on top in the form `${CUDA_TAG}-python${PYTHON_VERSION}`.

Currently, `latest` corresponds to `CUDA_TAG` = `12.4.1-cudnn-devel-ubuntu22.04` and `PYTHON_VERSION` = `3.12`.

Here are the TAGS currently available :
```Python
CUDA_VERSIONS = ["12.4.1"]
CUDA_CUDNN_OPTIONS = ["", "-cudnn"]
CUDA_TYPES = ["-devel"]
CUDA_OS_OPTIONS = ["-ubuntu22.04"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]
```

Other tags will be added later.

## Usage

You may run it directly from Docker Hub or by cloning the github repository and building the image locally before running it.

### Using Docker Hub image

To use the `cuda-python` image from Docker Hub, run the following command :

```bash
docker run --rm -it --gpus all ismailbouajaja/cuda-python bash
```

### Clone repository

To clone the github repository, build the image yourself and run it, follow these steps :

1. Clone the repository:
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
    - `ARG CUDA_TAG=12.4.1-cudnn-devel-ubuntu22.04`: The CUDA base image tag.
    - `ARG PYTHON_VERSION=3.12`: The Python version to install.

3. Run the Docker container:
    ```bash
    docker run --rm -it --gpus all cuda-python bash
    ```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.