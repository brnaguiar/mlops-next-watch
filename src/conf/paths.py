from pathlib import Path
from typing import Union

from conf import globals

"""
Paths for the Next Watch project
"""

SRC = Path("src")
DATA = Path("data")
DATA_01EXTERNAL = DATA / "01-external"
DATA_01RAW = DATA / "01-raw"
DATA_02PROCESSED = DATA / "02-processed"
DATA_03TRAIN = DATA / "03-train"
DATA_04MONITORING = DATA / "04-monitoring"
LOGS = "logs"
ENV = ".env"
ASSETS = "assets"
SPARKML_TMP_DIR = "docker/sparktmp"

def get_path(
    *args,
    suffix: str = "",
    as_string: bool = False,
    storage: str = globals.Storage.DOCKER,
    s3_protocol: str = globals.Protocols.S3A,
) -> Union[Path, str]:
    """
    params:
        *args: can be of a Paths obj, a Source obj, a name of a dir as a string, a filename, etc.
        scope: the file's scope. For instance if a file is within project directories then the scope is the PROJECT, otherwise insert the root dir
    """
    path = Path()
    if storage == globals.Storage.DOCKER:
        path = Path("/app")
    elif storage == globals.Storage.S3:
        path = Path()
    else:
        path = Path(__file__).parent.parent.parent.absolute()

    for arg in args:
        path = path / arg
    if suffix != "":
        path = path.with_suffix(suffix)

    return (
        (f"{s3_protocol}://" + str(path) if storage == globals.Storage.S3 else str(path))
        if as_string
        else path
    )
