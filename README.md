# DocScribe Project

DocScribe is a document generation and management tool designed to streamline the process of creating, managing, and exporting documents across different repositories and platforms. With its modular design, DocScribe offers flexibility and efficiency, catering to a wide range of documentation needs for individuals and organizations alike.

# Features

- Document Generation: Generate documents dynamically using templates and scripts.
- Repository Management: Organize documents in local or cloud-based repositories.
- Exporting: Seamlessly export documents to various formats and destinations.
- Customization: Use and define custom templates, scripts, and exporters based on project needs.
- Modularity: Extend functionality with custom repository types and exporters.

# Installation
Before installing DocScribe, ensure you have Python 3.11 or higher installed on your system.

```bash
pip install docscribe
```

# Understanding Repositories and Exporters

## Repositories
A repository in DocScribe is a storage space where documents are organized. Repositories can be local (on your file system) or cloud-based (such as an AWS S3 bucket). Each repository can contain multiple documents, each with its own configuration, templates, and scripts for generation.

## Exporters
Exporters are modules in DocScribe that handle the exporting of generated documents to different formats or destinations. For example, a document can be exported to a local directory or to an S3 bucket.

# Quick Start Guide

## Init DocScribe
To start using DocScribe, you need to create a new repository. You can do this using the `docscribe init` command. Pass `-p` or `--package-manager` to specify the package manager you are using. For example `pip`, `pipenv`, etc.

```bash
docscribe init -p pip
```

## Create a local document package
After initializing DocScribe, you can create a new document package using the `docscribe create` command. This will create a new document package in the current directory.

```bash
docscribe create -n "my_document_package_name" -t md
```



# License
DocScribe is released under the MIT License. See the LICENSE file for more details.

# Support
If you encounter any issues or have questions about DocScribe, please file an issue on the GitHub repository.
