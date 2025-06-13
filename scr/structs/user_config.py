from dataclasses import dataclass


@dataclass
class User:
    """Structure to store data related to table USER_CONFIG in memory data from DB"""

    id : str
    email : str
    nickname : str
    token : str
    db_schema : str


