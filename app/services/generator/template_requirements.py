import os
import importlib.util
from packaging import version

import rich
import click

from app.constants import CONFIG


def check_module(module: str) -> bool:
    """Checks if the module and optionally a specific version are installed."""
    module_parts = module.split("==")
    module_name = module_parts[0].lower()
    version_required = module_parts[1] if len(module_parts) > 1 else None

    try:
        mod = importlib.import_module(module_name)
        if version_required:
            current_version = getattr(mod, "__version__", None)
            if not current_version or version.parse(current_version) < version.parse(
                version_required
            ):
                return False

            if version.parse(current_version) > version.parse(version_required):
                if click.confirm(
                    f"Module {module_name} version {current_version} is installed. Do you want to install version {version_required}?"
                ):
                    return False

    except ImportError:
        return False

    return True


def install_requirements(config: dict):
    """Installs the requirements for the document."""
    requirements = config.get("require_modules", [])
    if not requirements:
        return

    # Validate if the required modules are installed
    uninstalled_modules = [
        module for module in requirements if not check_module(module)
    ]

    uninstalled_modules = " ".join(uninstalled_modules)

    if not uninstalled_modules:
        return

    # Ask the user if they want to install the required modules
    click.confirm(
        f"Do you want to install the required modules? ({uninstalled_modules.replace(' ', ', ')})",
        default=True,
        abort=True,
    )

    result = os.system(
        f"{CONFIG.get('package_manager', 'pip')} install {uninstalled_modules}"
    )

    if result != 0:
        rich.print("[red]Failed to install the required modules![/red]")
        raise click.Abort()


def request_document_kwargs(config: dict) -> dict:
    """Requests the document specific keyword arguments from the user."""
    # Get the document specific keyword arguments

    have_update = False

    document_kwargs = {}
    for key, value in config.get("kwargs", {}).items():
        document_kwargs[key] = click.prompt(
            f"Please enter the value for {key}:", default=value
        )
        if document_kwargs[key] != value:
            have_update = True

    return document_kwargs, have_update
