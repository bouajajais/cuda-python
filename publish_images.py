import subprocess
import concurrent.futures
from itertools import product

REPOSITORY = "ismailbouajaja"
IMAGE_NAME = "cuda-python"
CUDA_VERSIONS = ["12.4.1"]
CUDA_CUDNN_OPTIONS = ["", "-cudnn"]
CUDA_TYPES = ["-devel"] # "-base", "-runtime", "-devel"
CUDA_OS_OPTIONS = ["-ubuntu22.04"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

def build_and_push_image(image_name: str, tag: str, repository: str, **args: dict[str, str]):
    try:
        # Build the Docker image
        print(f"Building {IMAGE_NAME}:{tag}...")
        args = " ".join([f"--build-arg {key}={value}" for key, value in args.items()])
        build_command = f"docker build {args} -t {image_name}:{tag} ."
        subprocess.run(build_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Tag the Docker image
        tag_command = f"docker tag {image_name}:{tag} {repository}/{image_name}:{tag}"
        subprocess.run(tag_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Push the Docker image
        print(f"Pushing {IMAGE_NAME}:{tag} to {REPOSITORY}...")
        push_command = f"docker push {repository}/{image_name}:{tag}"
        subprocess.run(push_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print(f"Image {IMAGE_NAME}:{tag} successfully built and pushed to {REPOSITORY}...")
    except Exception as e:
        print(f"Error building and pushing image {IMAGE_NAME}:{tag} to {REPOSITORY}: {e}")

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for cuda_version, cudnn_option, cuda_type, cuda_os, python_version in product(CUDA_VERSIONS, CUDA_CUDNN_OPTIONS, CUDA_TYPES, CUDA_OS_OPTIONS, PYTHON_VERSIONS):
            cuda_tag = f"{cuda_version}{cudnn_option}{cuda_type}{cuda_os}"
            args = {
                "CUDA_TAG": cuda_tag,
                "PYTHON_VERSION": python_version
            }
            tag = f"{cuda_tag}-python{python_version}"
            futures.append(executor.submit(build_and_push_image, IMAGE_NAME, tag, REPOSITORY, **args))
        
        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()