from app.services.exporter.types import (
    local as LocalExporter,
    s3 as S3Exporter,
)

"""
A registry mapping exporter type names to their respective class implementations.

This dictionary is utilized to dynamically instantiate exporter objects based on
the specified type. It supports adding new exporter types without modifying existing
codebase, adhering to the open/closed principle. Current supported types are:

- "local": For exporting files to a local filesystem.
- "s3": For exporting files to an AWS S3 bucket.

Examples:
- To instantiate a local exporter: `EXPORTER_TYPES["local"](name, config)`
- To instantiate an S3 exporter: `EXPORTER_TYPES["s3"](name, config)`
"""

EXPORTER_TYPES = {
    "local": LocalExporter.Local,
    "s3": S3Exporter.S3,
}
