import tkinter as tk
from tkinter import ttk, messagebox
from core.modele import Coala, Piesa, PiesaAmplasata

class AplicatieAutoCut(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoCut - Optimizare Debitare PAL")
        self.geometry("1150x720")
        self.minsize(950,620)

        self.lista_piese: list[Piesa] = []
        self.construieste_interfata()

    def construieste_interfata(self):
        
        panou_stanga = ttk.Frame(self, padding = "10")
        panou_stanga.pack(side = tk.LEFT, fill = tk.Y)

        cadru_coala = ttk.LabelFrame(panou_stanga, text ="1. Parametri Coală Brută (mm)", padding = "10")
        cadru_coala.pack(fill= tk.X, pady = 5)

        ttk.Label(cadru_coala, text = "Lungime:"). grid(row = 0, column= 0, sticky= "w")
        self.camp_lungime_coala = ttk.Entry(cadru_coala, width= 8)
        self.camp_lungime_coala.insert(0, "2800")
        self.camp_lungime_coala.grid(row= 0, column= 1, padx= 5, pady= 2)

        ttk.Label(cadru_coala, text= "Lățime: ").grid(row= 1, column= 0, sticky="w")
        self.camp_latime_coala = ttk.Entry(cadru_coala, width= 8)
        self.camp_latime_coala.insert(0, "2070")
        self.camp_latime_coala.grid(row= 1, column= 1, padx= 5, pady= 2)

        ttk.Label(cadru_coala, text= "Pâmză: ").grid(row=2 , column= 0, sticky= "w")
        self.camp_panza = ttk.Entry(cadru_coala, width = 8)
        self.camp_panza.insert(0, "4")
        self.camp_panza.grid(row = 2, column= 1, padx = 5, pady = 2)

        ttk.Label(cadru_coala, text= "Tivire margine: ").grid(row=3, column=0, sticky= "w")
        self.camp_tivire = ttk.Entry(cadru_coala, width = 8) 
        self.camp_tivire.insert(0, "10") 
        self.camp_tivire.grid(row= 3, column = 1, padx = 5, pady =2 )


        cadru_piese = ttk.LabelFrame(panou_stanga, text= "2. Adăugare piese mobilier", padding= "10")
        cadru_piese.pack(fill= tk.X, pady = 5)
        
        ttk.Label(cadru_piese, text = "Denumire: ").grid(row= 0, column= 0, sticky= "w")
        self.camp_nume_piesa = ttk.Entry(cadru_piese, width= 12)
        self.camp_nume_piesa.insert (0, "Ușă")
        self.camp_nume_piesa.grid(row = 0, column= 1, padx =5, pady =2 )

        ttk.Label(cadru_piese, text= "Lungime: ").grid(row= 1, column= 0, sticky= "w")
        self.camp_lungime_piesa =ttk.Entry(cadru_piese, width = 12)
        self.camp_lungime_piesa.grid( row= 1, column= 1, padx= 5, pady = 2)

        ttk.Label(cadru_piese, text = "Lățime: ").grid(row=2, column=0, sticky="w")
        self.camp_latime_piesa = ttk.Entry(cadru_piese, width = 12)
        self.camp_latime_piesa.grid( row= 2, column = 1, padx = 5, pady = 2)

        ttk.Label(cadru_piese, text= "Cantitate: ").grid(row= 3, column= 0, sticky=" w")
        self.camp_cantitate_piesa = ttk.Entry(cadru_piese, width = 12)
        self.camp_cantitate_piesa.insert(0, "1")
        self.camp_cantitate_piesa.grid(row= 3, column= 1, padx =5 , pady = 2)

        self.bifa_rotatie = tk.BooleanVar(value= True)
        ttk.Checkbutton(cadru_piese, text = "Permite rotație (fibră)", variable=self.bifa_rotatie).grid(row = 4, column= 0, columnspan= 2, pady =5 )
        ttk.Button(cadru_piese, text = "➕ Adaugă în Tabel", command= self._adauga_piesa).grid(row= 5, column= 0, columnspan= 2, sticky= "ew", pady =2)

        cadru_tabel = ttk.LabelFrame(panou_stanga, text="3. Piese de Debitat", padding= 5)
        cadru_tabel.pack(fill=tk.BOTH, expand=True, pady = 5)

        self.tabel = ttk.Treeview(cadru_tabel, columns=("nume","l","w","cant"), show = "headings", height= 7)
        self.tabel.heading("nume", text = "Piesă")
        self.tabel.heading("l", text = "L (mm)")
        self.tabel.heading("w", text = "l (mm)")
        self.tabel.heading("cant", text = "Buc")
        self.tabel.column("nume", width= 80)
        self.tabel.column("l", width= 55)
        self.tabel.column("w", width= 55)
        self.tabel.column("cant", width= 40)
        self.tabel.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

        
        ttk.Button(panou_stanga, text="Calculează Debitarea", command= self._ruleaza_optimizarea).pack(fill= tk.X, pady = 10)


        panou_dreapta = ttk.Frame(self, padding= "10")
        panou_dreapta.pack (side = tk.RIGHT, fill = tk.BOTH, expand= True)

        self.eticheta_statistici = ttk.Label(panou_dreapta, text="Statistici: Introduceți datele și apăsați 'Calculează Debitare'", font=("Arial", 10, "bold"))
        self.eticheta_statistici.pack(anchor= "w", pady = (0, 5,))

        self.canvas_schita = tk.Canvas(panou_dreapta, bg="#1e1e1e", highlightthickness=1, highlightbackground="#444")
        self.canvas_schita.pack(fill= tk.BOTH, expand= True)

    def _adauga_piesa(self):
        try:
            nume = self.camp_nume_piesa.get().strip() or "Piesă"
            lungime = float(self.camp_lungime_piesa.get())
            latime = float(self.camp_latime_piesa.get())
            cantitate = int(float(self.camp_cantitate_piesa.get()))
            permite_rotatie = self.bifa_rotatie.get()

            if lungime <= 0 or latime <= 0 or cantitate <= 0:
                raise ValueError

            piesa = Piesa(nume, lungime, latime, cantitate, permite_rotatie)
            self.lista_piese.append(piesa)

            self.tabel.insert("", tk.END, values =(nume, int(lungime), int(latime), cantitate))
            self.camp_lungime_piesa.delete(0, tk.END)
            self.camp_latime_piesa.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Eroare", "Dimensiunile și cantitatea trebuie să fie valori numerice strict pozitive!")

    def _ruleaza_optimizarea(self):
        if not self.lista_piese:
            messagebox.showwarning("Atenție", "Adăugați cel puțin o piesă în listă înainte de debitare!")
            return

        try:
            lungime_coala = float(self.camp_lungime_coala.get())
            latime_coala = float(self.camp_latime_coala.get())
            panza = float(self.camp_panza.get())
            tivire = float(self.camp_tivire.get())
            coala = Coala(lungime_coala, latime_coala, grosime_panza = panza, margine_tivire = tivire)
        except ValueError:
            messagebox.showerror("Eroare", "Datele introduse pentru coală sunt invalide.")
            return


        piese_amplasate: list[PiesaAmplasata] = []
        curent_x = coala.margine_tivire
        curent_y = coala.margine_tivire
        inaltime_maxima_rand = 0.0

        for p in self.lista_piese:
            for _ in range(int(p.cantitate)):
                lungime_p = p.lungime
                latime_p = p.latime

                if curent_x + lungime_p > (coala.lungime - coala.margine_tivire):
                    curent_x = coala.margine_tivire
                    curent_y += inaltime_maxima_rand + coala.grosime_panza
                    inaltime_maxima_rand = 0.0

                if curent_y + latime_p <= (coala.latime - coala.margine_tivire):
                    piese_amplasate.append(
                        PiesaAmplasata(p.nume, curent_x, curent_y, lungime_p, latime_p)
                    )
                    curent_x += lungime_p + coala.grosime_panza
                    inaltime_maxima_rand = max(inaltime_maxima_rand, latime_p)

        self._deseneaza_schita(coala, piese_amplasate)

    def _deseneaza_schita(self, coala: Coala, piese_amplasate: list[PiesaAmplasata]):
        self.canvas_schita.delete("all")
        latime_ecran = self.canvas_schita.winfo_width()
        inaltime_ecran = self.canvas_schita.winfo_height()

        margine_canvas = 30
        spatiu_util_w = latime_ecran - 2 * margine_canvas
        spatiu_util_h = inaltime_ecran - 2 * margine_canvas

        scara = min(spatiu_util_w / coala.lungime, spatiu_util_h / coala.latime)

        orig_x = (latime_ecran - (coala.lungime * scara)) / 2
        orig_y = (inaltime_ecran - (coala.latime * scara)) / 2


        self.canvas_schita.create_rectangle(
            orig_x, orig_y,
            orig_x + (coala.lungime * scara),
            orig_y + (coala.latime * scara),
            fill = "#d2b48c", outline = "#ffffff", width = 2
        )

        if coala.margine_tivire > 0:
            tx = coala.margine_tivire * scara
            self.canvas_schita.create_rectangle(
                orig_x + tx, orig_y + tx,
                orig_x + (coala.lungime * scara) - tx,
                orig_y + (coala.latime * scara) - tx,
                outline = "#888888" , dash = (3, 3), width= 1
            )

        suprafata_utila = 0.0
        for p in piese_amplasate:
            px1 = orig_x + (p.x * scara)
            py1 = orig_y + (p.y * scara)
            px2 = px1 + (p.lungime * scara)
            py2 = py1 + (p.latime * scara)

            self.canvas_schita.create_rectangle(px1, py1, px2, py2, fill= "#2980b9", outline = "#0f3057", width =1)

            if (px2 - px1 ) > 35 and (py2 - py1) > 18:
                self.canvas_schita.create_text(
                    (px1 + px2) / 2, (py1 + py2) / 2,
                    text =f"{p.nume_piesa}\n{int(p.lungime)}x{int(p.latime)}",
                    fill= "white", font = ("Arial", 8, "bold")
                )
            suprafata_utila += (p.lungime * p.latime)
        suprafata_totala = coala.lungime * coala.latime
        procent_deseu = max(0.0, ((suprafata_totala - suprafata_utila) / suprafata_totala) * 100)
        self.eticheta_statistici.config(
            text =f"Piese debitate: {len(piese_amplasate)} | Suprafață utilă: {suprafata_utila/1_000_000:.2f} m² | Deșeu: {procent_deseu:.1f}%"
        )                