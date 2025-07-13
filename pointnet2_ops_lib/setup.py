import glob
import os.path as osp

from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

this_dir = osp.dirname(osp.abspath(__file__))
_ext_src_root = osp.join("pointnet2_ops", "_ext-src")
_ext_sources = glob.glob(osp.join(_ext_src_root, "src", "*.cpp")) + glob.glob(
    osp.join(_ext_src_root, "src", "*.cu")
)

requirements = ["torch>=1.4"]

# Load __version__ from _version.py
with open(osp.join("pointnet2_ops", "_version.py")) as f:
    exec(f.read())

# Updated architecture list for modern CUDA versions
os.environ["TORCH_CUDA_ARCH_LIST"] = "5.0;5.2;6.0;6.1;7.0;7.5;8.0;8.6"

setup(
    name="pointnet2_ops",
    version=__version__,
    author="Erik Wijmans",
    packages=["pointnet2_ops"],
    install_requires=requirements,
    ext_modules=[
        CUDAExtension(
            name="pointnet2_ops._ext",
            sources=_ext_sources,
            extra_compile_args={
                "cxx": ["-O3"],
                "nvcc": [
                    "-O3",
                    "-Xfatbin",
                    "-compress-all",
                    "-gencode",
                    "arch=compute_50,code=sm_50",
                    "-gencode",
                    "arch=compute_60,code=sm_60",
                    "-gencode",
                    "arch=compute_70,code=sm_70",
                    "-gencode",
                    "arch=compute_75,code=sm_75",
                    "-gencode",
                    "arch=compute_80,code=sm_80",
                    "-gencode",
                    "arch=compute_86,code=sm_86",
                ],
            },
            include_dirs=[osp.join(this_dir, _ext_src_root, "include")],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)
