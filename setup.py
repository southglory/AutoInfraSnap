from setuptools import setup, find_packages

setup(
    name="autoinfrasnap",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "psutil>=5.9.0",
        "docker>=6.1.0",
        "boto3>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "autoinfrasnap=autoinfrasnap.cli:main",
        ],
    },
    python_requires=">=3.13",
    author="DevRamyun",
    description="CLI tool for automated infrastructure state snapshots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
)
