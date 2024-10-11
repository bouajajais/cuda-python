from pathlib import Path
import subprocess
from itertools import product
from parallelize import parallelize

# README.md template variables and default build and repos values
BASE_IMAGE = "nvidia/cuda"
INSTALLED_FEATURES = ", ".join(["python"])

CWD = "."

IMAGE_NAME = "cuda-python"
DOCKERHUB_USERNAME = "ismailbouajaja"
GITHUB_USERNAME = "bouajajais"

TAG_FORMAT = "{CUDA_TAG}-python{PYTHON_VERSION}"

CUDA_VERSIONS = ["12.3.2", "12.4.1", "12.6.1"]
CUDA_CUDNN_OPTIONS = ["", "-cudnn9", "-cudnn"] # -cudnn9 for 12.3.2
CUDA_TYPES = ["-devel"] # -base, -runtime, -devel
CUDA_OS_OPTIONS = ["-ubuntu22.04"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12"]

def get_cuda_tag(
    cuda_version: str = CUDA_VERSIONS[-1],
    cuda_cudnn_option: str = CUDA_CUDNN_OPTIONS[-1],
    cuda_type: str = CUDA_TYPES[-1],
    cuda_os_option: str = CUDA_OS_OPTIONS[-1],
    ) -> str:
    return f"{cuda_version}{cuda_cudnn_option}{cuda_type}{cuda_os_option}"

def get_tag(
    tag_format: str = TAG_FORMAT,
    cuda_tag: str = get_cuda_tag(),
    python_version: str = PYTHON_VERSIONS[-1]
    ) -> str:
    return tag_format.format(
        CUDA_TAG=cuda_tag,
        PYTHON_VERSION=python_version
    )

def build_image(
    image_name: str = IMAGE_NAME,
    tag: str = get_tag(),
    cwd: str = CWD,
    verbose: int = 1,
    **args: dict[str, str]
    ) -> bool:
    try:
        # Build the Docker image
        if verbose >= 1:
            print(f"Building {image_name}:{tag}...")
        args = " ".join([f"--build-arg {key}={value}" for key, value in args.items()])
        build_command = f"docker build {args} -t {image_name}:{tag} ."
        if verbose < 2:
            subprocess.run(build_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
        else:
            subprocess.run(build_command, shell=True, check=True, cwd=cwd)
    except Exception as e:
        # Error
        if verbose >= 1:
            print(f"Error building image {image_name}:{tag}: {e}")
        return False
    else:
        # Success
        if verbose >= 1:
            print(f"Image {image_name}:{tag} successfully built...")
        return True

def push_image(
    image_name: str = IMAGE_NAME,
    tag: str = get_tag(),
    dockerhub_username: str = DOCKERHUB_USERNAME,
    cwd: str = CWD,
    verbose: int = 1
    ) -> bool:
    try:
        # Tag the Docker image
        tag_command = f"docker tag {image_name}:{tag} {dockerhub_username}/{image_name}:{tag}"
        if verbose < 2:
            subprocess.run(tag_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
        else:
            subprocess.run(tag_command, shell=True, check=True, cwd=cwd)

        # Push the Docker image
        if verbose >= 1:
            print(f"Pushing {dockerhub_username}/{image_name}:{tag} to Dockerhub...")
        push_command = f"docker push {dockerhub_username}/{image_name}:{tag}"
        if verbose < 2:
            subprocess.run(push_command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
        else:
            subprocess.run(push_command, shell=True, check=True, cwd=cwd)
    
    except Exception as e:
        # Error
        if verbose >= 1:
            print(f"Error pushing image {dockerhub_username}/{image_name}:{tag} to Dockerhub: {e}")
        return False
    
    else:
        # Success
        if verbose >= 1:
            print(f"Image {dockerhub_username}/{image_name}:{tag} successfully pushed to Dockerhub...")
        return True

def update_github(
    base_image: str = BASE_IMAGE,
    installed_features: str = INSTALLED_FEATURES,
    dockerhub_username: str = DOCKERHUB_USERNAME,
    github_username: str = GITHUB_USERNAME,
    image_name: str = IMAGE_NAME,
    tag_format: str = TAG_FORMAT,
    latest_cuda_tag: str = get_cuda_tag(),
    latest_python_version: str = PYTHON_VERSIONS[-1],
    cwd: str = CWD,
    verbose: int = 1
    ) -> None:
    try:
        with open(Path(__file__).parent / "README.md", "r") as file:
            current_readme = file.read()
    except FileNotFoundError:
        current_readme = ""
    
    with open(Path(__file__).parent / "README_template.md", "r") as file:
        readme = file.read()

    readme = readme.format(
        BASE_IMAGE=base_image,
        INSTALLED_FEATURES=installed_features,
        DOCKERHUB_USERNAME=dockerhub_username,
        GITHUB_USERNAME=github_username,
        IMAGE_NAME=image_name,
        TAG_FORMAT=tag_format,
        LATEST_CUDA_TAG=latest_cuda_tag,
        LATEST_PYTHON_VERSION=latest_python_version
    )
    
    if current_readme == readme:
        if verbose >= 1:
            print("No changes to README.md...")
        return
    
    with open(Path(__file__).parent / "README.md", "w") as file:
        file.write(readme)
    
    if verbose < 2:
        subprocess.run(f"git add .", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
        subprocess.run(f"git commit -m 'Update README.md'", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
        subprocess.run(f"git push", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)
    else:
        subprocess.run(f"git add .", shell=True, check=True, cwd=cwd)
        subprocess.run(f"git commit -m 'Update README.md'", shell=True, check=True, cwd=cwd)
        subprocess.run(f"git push", shell=True, check=True, cwd=cwd)

def publish_images(
    image_name: str = IMAGE_NAME,
    base_image: str = BASE_IMAGE,
    installed_features: str = INSTALLED_FEATURES,
    dockerhub_username: str = DOCKERHUB_USERNAME,
    github_username: str = GITHUB_USERNAME,
    tag_format: str = TAG_FORMAT,
    cuda_versions: list[str] = CUDA_VERSIONS,
    cuda_cudnn_options: list[str] = CUDA_CUDNN_OPTIONS,
    cuda_types: list[str] = CUDA_TYPES,
    cuda_os_options: list[str] = CUDA_OS_OPTIONS,
    python_versions: list[str] = PYTHON_VERSIONS,
    cwd: str = CWD,
    verbose: int = 1,
    n_jobs: int = 8
    ):
    def build_func(piece, index, data):
        cuda_version, cuda_cudnn_option, cuda_type, cuda_os_option, python_version = piece
        cuda_tag = get_cuda_tag(
            cuda_version,
            cuda_cudnn_option,
            cuda_type,
            cuda_os_option
        )
        args = {
            "CUDA_TAG": cuda_tag,
            "PYTHON_VERSION": python_version
        }
        return build_image(
            image_name,
            get_tag(
                tag_format,
                cuda_tag,
                python_version
            ),
            cwd,
            0,
            **args
        )
    
    parallelize(
        build_func,
        list(product(cuda_versions, cuda_cudnn_options, cuda_types, cuda_os_options, python_versions)),
        verbose=verbose,
        n_jobs=n_jobs
    )
    
    def push_func(piece, index, data):
        cuda_version, cuda_cudnn_option, cuda_type, cuda_os_option, python_version = piece
        cuda_tag = get_cuda_tag(
            cuda_version,
            cuda_cudnn_option,
            cuda_type,
            cuda_os_option
        )
        args = {
            "CUDA_TAG": cuda_tag,
            "PYTHON_VERSION": python_version
        }
        return push_image(
            image_name,
            get_tag(
                tag_format,
                cuda_tag,
                python_version
            ),
            dockerhub_username,
            cwd,
            0
        )
    
    parallelize(
        push_func,
        list(product(cuda_versions, cuda_cudnn_options, cuda_types, cuda_os_options, python_versions)),
        verbose=verbose,
        n_jobs=1
    )
    
    update_github(
        base_image,
        installed_features,
        dockerhub_username,
        github_username,
        image_name,
        tag_format,
        get_cuda_tag(
            cuda_versions[-1],
            cuda_cudnn_options[-1],
            cuda_types[-1],
            cuda_os_options[-1]
        ),
        python_versions[-1],
        cwd,
        verbose
    )
    

if __name__ == "__main__":
    publish_images()