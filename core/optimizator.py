from core.modele import PiesaAmplasata


class CoalaCalculata:
    def __init__(self, index, piese_amplasate, suprafata_utila, procent_deseu):
        self.index = index
        self.piese_amplasate = piese_amplasate
        self.suprafata_utila = suprafata_utila
        self.procent_deseu = procent_deseu


class RezultatOptimizare:
    def __init__(self, coli, piese_neincapute, suprafata_utila, suprafata_totala, deseu_mediu):
        self.coli = coli
        self.piese_neincapute = piese_neincapute
        self.suprafata_totala_utila = suprafata_utila
        self.suprafata_totala_coli = suprafata_totala
        self.procent_mediu_deseu = deseu_mediu


class OptimizatorDebitare:
    def __init__(self, coala):
        self.coala = coala

    def optimizeaza(self, lista_piese):
        piese_individuale = []
        for p in lista_piese:
            for _ in range(p.cantitate):
                piese_individuale.append(p)

        # Sortare descrescatoare dupa arie (First Fit Decreasing)
        piese_individuale.sort(key=lambda x: x.lungime * x.latime, reverse=True)

        coli_generate = []
        piese_ramase = list(piese_individuale)
        kerf = self.coala.grosime_panza
        idx_coala = 1

        while piese_ramase and idx_coala <= 50:
            spatii = [{
                "x": self.coala.margine_tivire,
                "y": self.coala.margine_tivire,
                "w": self.coala.lungime_utila,
                "h": self.coala.latime_utila
            }]

            piese_coala = []
            neplasate = []

            for p in piese_ramase:
                gasit = False
                for i, sp in enumerate(spatii):
                    # Incercare orientare normala
                    if p.lungime <= sp["w"] and p.latime <= sp["h"]:
                        ales = (p.lungime, p.latime, False)
                        gasit = True
                    # Incercare rotire la 90 de grade
                    elif p.permite_rotatie and p.latime <= sp["w"] and p.lungime <= sp["h"]:
                        ales = (p.latime, p.lungime, True)
                        gasit = True

                    if gasit:
                        spatiu = spatii.pop(i)
                        pL, pl, rot = ales

                        piese_coala.append(PiesaAmplasata(p.nume, spatiu["x"], spatiu["y"], pL, pl, rot))

                        # Taietura ghilotina: despicam spatiul ramas in doua
                        if spatiu["w"] - pL - kerf > 0:
                            spatii.append({
                                "x": spatiu["x"] + pL + kerf,
                                "y": spatiu["y"],
                                "w": spatiu["w"] - pL - kerf,
                                "h": pl
                            })
                        if spatiu["h"] - pl - kerf > 0:
                            spatii.append({
                                "x": spatiu["x"],
                                "y": spatiu["y"] + pl + kerf,
                                "w": spatiu["w"],
                                "h": spatiu["h"] - pl - kerf
                            })

                        spatii.sort(key=lambda s: (s["y"], s["x"]))
                        break

                if not gasit:
                    neplasate.append(p)

            if not piese_coala:
                break

            suprafata_utila = sum(p.lungime * p.latime for p in piese_coala)
            suprafata_coala = self.coala.lungime * self.coala.latime
            deseu = ((suprafata_coala - suprafata_utila) / suprafata_coala) * 100

            coli_generate.append(CoalaCalculata(idx_coala, piese_coala, suprafata_utila, deseu))
            piese_ramase = neplasate
            idx_coala += 1

        total_util = sum(c.suprafata_utila for c in coli_generate)
        total_aria = len(coli_generate) * (self.coala.lungime * self.coala.latime)
        deseu_mediu = ((total_aria - total_util) / total_aria) * 100 if total_aria > 0 else 0

        return RezultatOptimizare(coli_generate, piese_ramase, total_util, total_aria, deseu_mediu)