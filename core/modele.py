class Coala:
    def __init__(self, lungime, latime, grosime_panza=4, margine_tivire=10):
        self.lungime = float(lungime)
        self.latime = float(latime)
        self.grosime_panza = float(grosime_panza)
        self.margine_tivire = float(margine_tivire)
        self.lungime_utila = self.lungime - (2 * self.margine_tivire)
        self.latime_utila = self.latime - (2 * self.margine_tivire)


class Piesa:
    def __init__(self, nume, lungime, latime, cantitate=1, permite_rotatie=True, cant_lungime=0.0, cant_latime=0.0, laturi_cant_l=0, laturi_cant_w=0):
        self.nume = str(nume)
        # Dimensiunea fizica taiata de circular (nu se scade nimic)
        self.lungime = float(lungime)
        self.latime = float(latime)
        self.cantitate = int(cantitate)
        self.permite_rotatie = bool(permite_rotatie)
        
        # Date cant
        self.cant_lungime = float(cant_lungime)
        self.cant_latime = float(cant_latime)
        self.laturi_cant_l = int(laturi_cant_l)
        self.laturi_cant_w = int(laturi_cant_w)

        # Dimensiunea finita a usii/piesei (PAL + grosimea cantului adaugat)
        self.lungime_finita = self.lungime + (self.laturi_cant_l * self.cant_lungime)
        self.latime_finita = self.latime + (self.laturi_cant_w * self.cant_latime)


class PiesaAmplasata:
    def __init__(self, nume, x, y, lungime, latime, rotita=False, piesa_originala=None):
        self.nume = nume
        self.x = x
        self.y = y
        self.lungime = lungime
        self.latime = latime
        self.rotita = rotita
        self.piesa_originala = piesa_originala