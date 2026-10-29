from dataclasses import dataclass 
from typing import List, Tuple
from core.modele import Coala, Piesa, PiesaAmplasata


@dataclass
class DreptunghiLiber:
    x: float
    y: float
    lungime: float
    latime: float


@dataclass
class RezultatOptimizare:
     piese_amplasate: List[PiesaAmplasata]
     piese_neincapute: List[Piesa]
     suprafata_utila: float
     suprafata_totala: float
     procent_deseu: float


class OptimizatorDebitare:

    def __init__(self, coala: Coala):
        self.coala = coala

    def optimizeaza (self, lista_piese: List[Piesa]) -> RezultatOptimizare:

        piese_individuale : List[Piesa] = []
        for p in lista_piese:
            for _ in range (int(p.cantitate)):
                piese_individuale.append(p)


        piese_individuale.sort(
            key= lambda item: (item.lungime * item.latime, max(item.lungime, item.latime )),
            reverse= True
        )

        spatii_libere: List[DreptunghiLiber] = [
            DreptunghiLiber(
                x = self.coala.margine_tivire,
                y= self.coala.margine_tivire,
                lungime= self.coala.lungime_utila,
                latime =self.coala.latime_utila
            )
        ]

        piese_amplasate : List[PiesaAmplasata] = []
        piese_neincapute : List[Piesa] = []
        kerf = self.coala.grosime_panza


        for piesa in piese_individuale:
            potrivire_gasita = False
            index_spatiu_ales = -1
            dimensiune_aleasa: Tuple[float,float,float] = (0.0,0.0,False)

            for idx, spatiu in enumerate(spatii_libere):

                if piesa.lungime <= spatiu.lungime and piesa.latime <= spatiu.latime:
                    dimensiune_aleasa = (piesa.lungime, piesa.latime, False)
                    index_spatiu_ales = idx
                    potrivire_gasita = True
                    break

                if piesa.permite_rotatie:
                    if piesa.latime <= spatiu.lungime and piesa.lungime <= spatiu.latime:
                        dimensiune_aleasa = (piesa.aleasa, piesa.lungime, True)
                        index_spatiu_ales = idx
                        potrivire_gasita = True
                        break

            if potrivire_gasita:
                spatiu = spatii_libere.pop(index_spatiu_ales)
                p_lungime, p_latime, rotita = dimensiune_aleasa


                piese_amplasate.append(
                    PiesaAmplasata(
                        nume_piesa= piesa.nume,
                        x= spatiu.x,
                        y= spatiu.y,
                        lungime=p_lungime,
                        latime = p_latime,
                        rotita = rotita
                    )
                )

                spatiu_dreapta_w = spatiu.lungime - p_lungime -kerf
                if spatiu_dreapta_w > 0:
                    spatii_libere.append(
                        DreptunghiLiber(
                            x= spatiu.x + p_lungime + kerf,
                            y = spatiu.y,
                            lungime= spatiu_dreapta_w,
                            latime= p_latime
                        )
                    )
                spatiu_jos_h = spatiu.latime - p_latime - kerf
                if spatiu_jos_h > 0:
                    spatii_libere.append(
                        DreptunghiLiber(
                            x = spatiu.x,
                            y = spatiu.y + p_latime + kerf,
                            lungime = spatiu.lungime,
                            latime = spatiu_jos_h
                        )
                    )    
                spatii_libere.sort(key=lambda s: (s.y, s.x))
            else:
                piese_neincapute.append(piesa)

        suprafata_utila = sum(p.lungime * p.latime for p in piese_amplasate)
        suprafata_totala = self.coala.lunigme * self.coala.latime
        procent_deseu = max(0.0, ((suprafata_totala - suprafata_utila) / suprafata_totala) * 100)

        return RezultatOptimizare(
            piese_amplasate= piese_amplasate,
            piese_neincapute= piese_neincapute,
            suprafata_utila=suprafata_utila,
            suprafata_totala= suprafata_totala,
            procent_deseu= procent_deseu
        )       
