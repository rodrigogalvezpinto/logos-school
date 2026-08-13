"""Puerto compartido: hace "ahora" inyectable, para que la lógica de tiempo transcurrido
en las entidades sea testeable sin dormir el reloj real."""

from datetime import datetime
from typing import Protocol


class Reloj(Protocol):
    def ahora(self) -> datetime: ...
