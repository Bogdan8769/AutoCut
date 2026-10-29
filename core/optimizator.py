from dataclasses import dataclass, field
from typing import List, Tuple
from core.modele import Coala, Piesa, PiesaAmplasata


@dataclass
class DreptunghiLiber:
    x: float
    y: float
    lungime: float
    latime: float


@dataclass
class CoalaCalculata:
    index: int
    piese_amplasate: List[PiesaAmplasata] = field(default_factory=list)
    suprafata_utila: float = 0.0
    procent_deseu: float = 0.0


@dataclass
class RezultatOptimizare:
    coli: List[CoalaCalculata]
    piese_neincapute: List[Piesa]
    suprafata_totala_utila: float
    suprafata_totala_coli: float
    procent_mediu_deseu: float


class OptimizatorDebitare:
    def __init__(self, coala: Coala):
        self.coala = coala

    def optimizeaza(self, lista_piese: List[Piesa]) -> RezultatOptimizare:
        piese_de_plasat: List[Piesa] = []
        for p in lista_piese:
            for _ in range(int(p.cantitate)):
                piese_de_plasat.append(p)

        piese_de_plasat.sort(
            key=lambda item: (item.lungime * item.latime, max(item.lungime, item.latime)),
            reverse=True
        )

        coli_generate: List[CoalaCalculata] = []
        piese_ramase = list(piese_de_plasat)
        kerf = self.coala.grosime_panza
        index_coala = 1

        while piese_ramase and index_coala <= 100:
            spatii_libere: List[DreptunghiLiber] = [
                DreptunghiLiber(
                    x=self.coala.margine_tivire,
                    y=self.coala.margine_tivire,
                    lungime=self.coala.lungime_utila,
                    latime=self.coala.latime_utila
                )
            ]

            piese_pe_aceasta_coala: List[PiesaAmplasata] = []
            piese_neplasate_tura_asta: List[Piesa] = []

            for piesa in piese_ramase:
                potrivire_gasita = False
                index_spatiu = -1
                dimensiuni_alese: Tuple[float, float, bool] = (0.0, 0.0, False)

                for idx, spatiu in enumerate(spatii_libere):
                    if piesa.lungime <= spatiu.lungime and piesa.latime <= spatiu.latime:
                        dimensiuni_alese = (piesa.lungime, piesa.latime, False)
                        index_spatiu = idx
                        potrivire_gasita = True
                        break

                    if piesa.permite_rotatie:
                        if piesa.latime <= spatiu.lungime and piesa.lungime <= spatiu.latime:
                            dimensiuni_alese = (piesa.latime, piesa.lungime, True)
                            index_spatiu = idx
                            potrivire_gasita = True
                            break

                if potrivire_gasita:
                    spatiu = spatii_libere.pop(index_spatiu)
                    p_lungime, p_latime, rotita = dimensiuni_alese

                    piese_pe_aceasta_coala.append(
                        PiesaAmplasata(
                            nume_piesa=piesa.nume,
                            x=spatiu.x,
                            y=spatiu.y,
                            lungime=p_lungime,
                            latime=p_latime,
                            rotita=rotita
                        )
                    )

                    spatiu_dreapta = spatiu.lungime - p_lungime - kerf
                    if spatiu_dreapta > 0:
                        spatii_libere.append(
                            DreptunghiLiber(
                                x=spatiu.x + p_lungime + kerf,
                                y=spatiu.y,
                                lungime=spatiu_dreapta,
                                latime=p_latime
                            )
                        )

                    spatiu_jos = spatiu.latime - p_latime - kerf
                    if spatiu_jos > 0:
                        spatii_libere.append(
                            DreptunghiLiber(
                                x=spatiu.x,
                                y=spatiu.y + p_latime + kerf,
                                lungime=spatiu.lungime,
                                latime=spatiu_jos
                            )
                        )

                    spatii_libere.sort(key=lambda s: (s.y, s.x))
                else:
                    piese_neplasate_tura_asta.append(piesa)

            if not piese_pe_aceasta_coala:
                break

            suprafata_utila = sum(p.lungime * p.latime for p in piese_pe_aceasta_coala)
            suprafata_totala = self.coala.lungime * self.coala.latime
            deseu = max(0.0, ((suprafata_totala - suprafata_utila) / suprafata_totala) * 100)

            coli_generate.append(
                CoalaCalculata(
                    index=index_coala,
                    piese_amplasate=piese_pe_aceasta_coala,
                    suprafata_utila=suprafata_utila,
                    procent_deseu=deseu
                )
            )

            piese_ramase = piese_neplasate_tura_asta
            index_coala += 1

        total_util = sum(c.suprafata_utila for c in coli_generate)
        total_coli_aria = len(coli_generate) * (self.coala.lungime * self.coala.latime)
        deseu_mediu = max(0.0, ((total_coli_aria - total_util) / total_coli_aria) * 100) if total_coli_aria > 0 else 0.0

        return RezultatOptimizare(
            coli=coli_generate,
            piese_neincapute=piese_ramase,
            suprafata_totala_utila=total_util,
            suprafata_totala_coli=total_coli_aria,
            procent_mediu_deseu=deseu_mediu
        )