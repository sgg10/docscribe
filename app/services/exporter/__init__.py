from app.services.exporter.types import (
    local as LocalExporter,
    s3 as S3Exporter,
)

EXPORTER_TYPES = {
    "local": LocalExporter.Local,
    "s3": S3Exporter.S3,
}
