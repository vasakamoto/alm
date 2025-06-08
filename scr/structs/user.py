
from dataclasses import dataclass


@dataclass
class User:
    """Structure to store data related to table USERS in memory data from DB"""

    email : str
    nickname : str
    token : str
    db_schema : str

