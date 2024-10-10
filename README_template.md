# {IMAGE_NAME}

This Docker image is built on top of the `{BASE_IMAGE}` image.

It installs the following element(s) on top:

{INSTALLED_FEATURES}

## Tag Format

Tags follow this format : `{TAG_FORMAT}`.

## Dockerhub

These images can be found in Dockerhub through the following link:

[https://hub.docker.com/repository/docker/{DOCKERHUB_USERNAME}/{IMAGE_NAME}/general](https://hub.docker.com/repository/docker/{DOCKERHUB_USERNAME}/{IMAGE_NAME}/general)

## Clone repository

To clone the github repository containing the Dockerfile used, follow these steps :

1. Clone the repository:
    ```bash
    git clone [https://github.com/{GITHUB_USERNAME}/{IMAGE_NAME}.git](https://github.com/{GITHUB_USERNAME}/{IMAGE_NAME}.git)
    ```

2. Navigate to the project directory:
    ```bash
    cd {IMAGE_NAME}
    ```

2. Build the Docker image using the provided Dockerfile:
    ```bash
    docker build -t {IMAGE_NAME} .
    ```

    The `docker build` command accepts the following arguments:
    - `ARG CUDA_TAG={LATEST_CUDA_TAG}`: The CUDA base image tag.
    - `ARG PYTHON_VERSION={LATEST_PYTHON_VERSION}`: The Python version to install.

3. Run the Docker container:
    ```bash
    docker run --rm -it {IMAGE_NAME} bash
    ```

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.