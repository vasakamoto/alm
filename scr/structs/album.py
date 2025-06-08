
from dataclasses import dataclass
from datetime import (
    date,
    time
)


@dataclass
class Album:
    """Structure to store data related to table ALBUMS in memory data from DB"""

    title : str
    artists : str
    genre : str
    subgenre : str
    rating : float
    n_tracks : int 
    length : time
    dt_release : date
    dt_inserted : date
