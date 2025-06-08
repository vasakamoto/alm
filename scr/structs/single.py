
from dataclasses import dataclass
from datetime import (
    date,
    time
)


@dataclass
class Single:
    """Structure to store data related to table SINGLES in memory data from DB"""

    title : str
    artists : str
    genre : str
    subgenre : str
    rating : float
    length : time
    dt_release : date
    dt_inserted : date

