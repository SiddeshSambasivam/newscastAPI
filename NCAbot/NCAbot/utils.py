from typing import Type
import hashlib
from datetime import datetime


def change_datetime_format(timestamp_string: str) -> str:
    """converts datetime format to %d/%m/%Y, %H:%M:%S"""

    try:
        datetime_object = datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return ""

    return datetime_object, datetime_object.strftime("%d/%m/%Y, %H:%M:%S")


def generate_hash(string: str) -> str:
    """Returns the SHA256 hash of string"""
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def get_unix_timestamp(timestamp: Type[datetime]) -> int:
    """Returns the unix timestamp of given time"""
    return int(datetime.timestamp(timestamp))
