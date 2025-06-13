
from dataclasses import dataclass


@dataclass
class User:
    """Structure to store data related to table USERS in memory data from DB"""

    id : str
    email : str
    username : str
    token : str
    db_schema : str

