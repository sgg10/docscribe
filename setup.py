from setuptools import find_packages, setup


def read_requirements():
    with open("requirements.txt", "r") as req:
        content = req.read()
        requirements = content.split("\n")

    return requirements


setup(
    name="docscribe",
    version="0.1.0",
    description="A simple tool to generate documentation, reports, and more from your codebase.",
    packages=find_packages(),
    include_dirs=".",
    include_package_data=True,
    install_requires=read_requirements(),
    license="MIT",
    author="sgg10",
    author_email="sgg10.develop@gmail.com",
    entry_points="""
        [console_scripts]
        docscribe=app.main:cli
    """,
    python_requires=">=3.11",
)
