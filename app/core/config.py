import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def default_database_url() -> str:
    configured_dir = os.getenv("CONTROL_FRIGORIFICO_DATA_DIR")
    if configured_dir:
        base_dir = Path(configured_dir)
    elif os.getenv("LOCALAPPDATA"):
        base_dir = Path(os.environ["LOCALAPPDATA"]) / "ControlFrigorifico"
    else:
        base_dir = PROJECT_ROOT / "data"

    base_dir.mkdir(parents=True, exist_ok=True)
    db_path = base_dir / "frigorifico.db"
    return f"sqlite:///{db_path.as_posix()}"


@dataclass(frozen=True)
class Settings:
    app_name: str = "Control Frigorifico API"
    database_url: str = os.getenv("DATABASE_URL", default_database_url())


settings = Settings()
