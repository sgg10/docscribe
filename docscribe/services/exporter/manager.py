from docscribe.utils.managers import SegmentManager


class ExporterManager(SegmentManager):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, "exporters")

    def export(self, file_name: str, *args, **kwargs) -> None:
        self._validate_exporter()
        self.exporter.export(file_name, mode=kwargs.get("mode", "rb"))

    def make_output_uri(self, file_name: str) -> str:
        self._validate_exporter()
        return self.exporter.make_output_uri(file_name)
