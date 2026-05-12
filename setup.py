from setuptools import setup, find_packages

setup(
    name="embodied_ai_mujoco",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mujoco>=3.0.0",
        "gymnasium>=0.29.0",
        "numpy>=1.24.0",
        "torch>=2.0.0",
    ],
    python_requires=">=3.8",
)
