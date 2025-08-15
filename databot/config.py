from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Caminhos de projeto padronizados.

    Cria diretórios na primeira execução, se não existirem.
    """
    root: Path = Path(__file__).resolve().parent.parent
    data_dir: Path = root / "data"
    raw_dir: Path = data_dir / "raw"
    processed_dir: Path = data_dir / "processed"
    db_path: Path = data_dir / "databot.sqlite"

    def ensure(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)


# Configurações padrão do projeto
OPEN_METEO_BASE_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_LATITUDE = -23.5505  # São Paulo
DEFAULT_LONGITUDE = -46.6333
DEFAULT_TIMEZONE = "auto"

# Datas padrão (últimos 30 dias)
DEFAULT_HISTORY_DAYS = 30

# Leitura de configurações opcionais via env vars
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # usado apenas se o usuário quiser LLM externa


paths = ProjectPaths()
paths.ensure()
