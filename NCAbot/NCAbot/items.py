from dataclasses import dataclass, field


@dataclass
class NewscastItem:
    # define the fields for your item here like:
    source: str = field(default=None)
    title: str = field(default=None)
    url: str = field(default=None)
    timestamp: str = field(default=None)
    unix_timestamp: int = field(default=None)
    category: str = field(default=None)
    country: str = field(default=None)
    hash: str = field(default=None)
