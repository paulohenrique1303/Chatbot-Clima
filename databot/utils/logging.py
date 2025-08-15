from __future__ import annotations

import logging
from typing import Optional


def setup_logging(level: int = logging.INFO, name: Optional[str] = None) -> logging.Logger:
    """Configura um logger simples e consistente para o projeto.

    - Usa formato compacto com nível, nome e mensagem
    - Evita configuração duplicada em múltiplas importações
    """
    logger_name = name or "databot"
    logger = logging.getLogger(logger_name)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(name)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger
