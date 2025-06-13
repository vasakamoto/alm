
from dataclasses import (
    dataclass,
    fields
)

from datetime import (
    date,
    time
)


@dataclass
class Album:
    """Structure to store data related to table ALBUMS in memory data from DB"""

    id : str
    title : str
    artists : str
    genre : str
    subgenre : str
    rating : float
    n_tracks : int 
    length : float
    dt_release : date
    dt_inserted : date

    def empty(self):
        """Check if all attributes are not empty"""
        for att in fields(self):
            if not getattr(att, att.name):
                return False 

        return True
