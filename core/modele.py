from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Coala:
        lungime: float
        latime: float
        grosime_panza: float = 4.0
        margine_tivire: float = 10.0

        @property
        def lungime_utila(self) -> float:
                return max (0.0, self.lungime - (2* self.margine_tivire))

        @property
        def latime_utila(self) -> float:
                return max(0.0, self.latime - (2* self.margine_tivire))

@dataclass
class Piesa:

    nume: str
    lungime: float
    latime: float
    cantitate: int = 1
    permite_rotatie: bool = True

@dataclass
class PiesaAmplasata:
        nume_piesa: str
        x: float
        y: float
        lungime: float
        latime: float
        rotatia: bool = False