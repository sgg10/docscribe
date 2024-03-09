from abc import ABC, abstractmethod

from app.utils.config_operations import (
    write_item_by_segment,
    delete_item_by_segment,
)


class Segment(ABC):
    """
    An abstract base class for defining segments of the application configuration,
    such as repositories or exporters. It provides a standardized way to handle
    configuration and lifecycle management of these segments.

    Attributes:
        name (str): The unique name of the segment instance.
        _type (str): The type of the segment, e.g., 's3', 'local'.
        segment (str): The category of the segment, e.g., 'repositories', 'exporters'.
        config (dict, optional): The configuration dictionary for the segment. If None,
            a default configuration will be created using the `_create_config` method.

    Methods:
        _auth: An abstract method that must be implemented to authenticate or verify access
            for the segment.
        _create_config: An abstract method for creating a default configuration dictionary
            for the segment. Can be overridden to provide custom configuration logic.
        _write_config: Saves the segment configuration to the application's configuration file.
        delete: Removes the segment configuration from the application's configuration file.
    """

    def __init__(self, name: str, _type: str, segment: str, config: dict | None = None):
        """
        Initializes a new instance of the Segment class.

        Args:
            name (str): The name of the segment.
            _type (str): The type of the segment.
            segment (str): The category of the segment.
            config (dict, optional): The configuration for the segment. Defaults to None.
        """
        self.name = name
        self._type = _type
        self.segment = segment
        if config is None:
            self.config = self._create_config()
            self._write_config()
        else:
            self.config = config

    @abstractmethod
    def _auth(self):
        """
        An abstract method that must be implemented by subclasses to handle authentication
        or access verification for the segment.
        """
        ...

    @abstractmethod
    def _create_config(self, *args, **kwargs) -> dict:
        """
        Creates a default configuration dictionary for the segment.

        This method should be overridden by subclasses to provide specific configuration
        logic based on the segment type.

        Returns:
            dict: The default configuration dictionary for the segment.
        """
        return {}

    def _write_config(self) -> None:
        """
        Writes the segment's configuration to the application's configuration file.
        """
        write_item_by_segment(self.segment, self.name, self._type, self.config)

    def delete(self) -> None:
        """
        Removes the segment's configuration from the application's configuration file.
        """
        delete_item_by_segment(self.segment, self.name)
