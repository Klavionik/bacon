from dataclasses import dataclass, field


@dataclass
class Config:
    API_BASE_URL: str = "https://www.perekrestok.ru/api/customer/1.4.1.0"
    PROXIES: dict[str] = field(default_factory=dict)


config = Config()
