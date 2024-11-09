from shutil import copy
from site import getsitepackages
from setuptools import setup, Extension
from subprocess import run
from pathlib import Path

here = Path(__file__).parent
hslib_path = here / "src/hspkg/hslib"

run(
    cwd=hslib_path,
    args=[
        "cabal",
        "build",
    ],
    check=True,
)

(hslib_path / "a.out").unlink(missing_ok=True)  # because cabal is stupid

Path("artifact").mkdir(exist_ok=True)
try:
    library_path = next((hslib_path / "dist-newstyle").rglob("libhs.so")).relative_to(
        here
    )
except StopIteration:
    raise FileNotFoundError("Couldnt figure out `libhs.so` path after `cabal build`")
library_dir = library_path.parent

copy(library_path, "artifact/libhs.so")

setup(
    ext_modules=[
        Extension(
            "hspkg.hslib",
            sources=[
                "src/hspkg/hslib/src/hslib.c",
            ],
            library_dirs=[
                "artifact",
            ],
            libraries=[
                "hs",
            ],
            runtime_library_dirs=[
                getsitepackages()[0]
                + "/hspkg/artifact",  # awful hack, but it is what it is
            ],
        )
    ],
    packages=[
        "hspkg",
        "hspkg.hslib",
        "hspkg.artifact",
    ],
    package_dir={
        "": "src",
        "hspkg.artifact": "artifact",  # not a python package, just a directory..
    },
    package_data={"hspkg.artifact": ["*.so"]},
)
