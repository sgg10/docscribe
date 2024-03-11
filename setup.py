import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="docscribe",
    version="0.1.1",
    description="A simple tool to generate documentation, reports, and more from your codebase.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(),
    include_dirs=".",
    include_package_data=True,
    install_requires=read_requirements(),
    url="https://github.com/sgg10/docscribe/",
    license="MIT",
    author="sgg10",
    author_email="sgg10.develop@gmail.com",
    entry_points="""
        [console_scripts]
        docscribe=app.main:cli
    """,
    python_requires=">=3.11",
    project_urls={  # Optional
        "Bug Reports": "https://github.com/sgg10/docscribe/issues",
        "Source": "https://github.com/sgg10/docscribe/",
        "Repository": "https://github.com/sgg10/docscribe/",
    },
)
