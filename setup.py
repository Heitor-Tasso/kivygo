import os, sys, re
from pathlib import Path
from setuptools import find_packages, setup


assert sys.version_info >= (3, 7, 0), "Requires Python 3.7+"
_init_file_path, _init_file_name = os.path.split(__file__)


def get_version():
    version_file = os.path.join(_init_file_path, "kivygo", "__init__.py")
    
    with open(version_file, "rt", encoding="utf-8") as file:
        version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
        try:
            version = re.findall(version_regex, file.read(), re.M)[0]
            return version
        except IndexError:
            raise ValueError(f"Unable to find version string in {version_file}.")


def glob_paths(pattern):
    out_files = []
    src_path = os.path.join(_init_file_path, "kivygo")

    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith(pattern):
                filepath = os.path.join(str(Path(*Path(root).parts[1:])), file)
                try:
                    out_files.append(filepath.split(f"kivygo{os.sep}")[1])
                except IndexError:
                    out_files.append(filepath)

    return out_files


if __name__ == "__main__":
    setup(
        name="kivygo",
        version = get_version(),
        packages = find_packages(include=["kivygo", "kivygo.*"]),
        package_dir = {"kivygo": "kivygo"},
        package_data={
            "kivygo": [
                *glob_paths(".png"),
                *glob_paths(".jpg"),
                *glob_paths(".svg"),
                *glob_paths(".ttf"),
                *glob_paths(".kv"),
                *glob_paths(".frag"),
                *glob_paths(".glsl"),
                *glob_paths(".atlas"),
                *glob_paths(".pex"),
                *glob_paths(".bounds"),
            ]
        },
        install_requires=[
            "kivy>=2.0.0", "pillow",
            "opencv-python", "camera4kivy",
            "matplotlib", "pyzbar",
            "requests", "svglib"
        ],
        setup_requires=[],
        python_requires=">=3.7",
)
