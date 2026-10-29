import tkinter as tk
from tkinter import ttk, messagebox
from core.modele import Coala, Piesa, PiesaAmplasata
from core.optimizator import OptimizatorDebitare, RezultatOptimizare, CoalaCalculata

class AplicatieAutoCut(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoCut - Optimizare Debitare PAL")
        self.geometry("1150x720")
        self.minsize(950,620)

        self.lista_piese: list[Piesa] = []
        self.rezultat_curent: RezultatOptimizare | None = None
        self.coala_activa_idx: int = 0
        self.coala_setari: Coala | None = None
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

        bara_sus = ttk.Frame(panou_dreapta)
        bara_sus.pack(fill=tk.X, pady=(0, 5))

        self.btn_prev = ttk.Button(bara_sus, text="◀ Înapoi", width=8, state=tk.DISABLED, command=self._coala_anterioara)
        self.btn_prev.pack(side=tk.LEFT)

        self.lbl_pagina = ttk.Label(bara_sus, text="Coala 0 / 0", font=("Arial", 10, "bold"), padding="5")
        self.lbl_pagina.pack(side=tk.LEFT, padx=10)

        self.btn_next = ttk.Button(bara_sus, text="Înainte ▶", width=8, state=tk.DISABLED, command=self._coala_urmatoare)
        self.btn_next.pack(side=tk.LEFT)

        self.eticheta_statistici = ttk.Label(bara_sus, text="Statistici: Introduceți datele și apăsați 'Calculează Debitare'", font=("Arial", 9))
        self.eticheta_statistici.pack(side=tk.RIGHT, padx=5)

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
            self.coala_setari = Coala(lungime_coala, latime_coala, grosime_panza=panza, margine_tivire=tivire)
        except ValueError:
            messagebox.showerror("Eroare", "Datele introduse pentru coală sunt invalide.")
            return

        optimizator = OptimizatorDebitare(self.coala_setari)
        self.rezultat_curent = optimizator.optimizeaza(self.lista_piese)

        if not self.rezultat_curent.coli:
            messagebox.showerror("Eroare", "Piesele sunt prea mari pentru această coală!")
            return

        if self.rezultat_curent.piese_neincapute:
            messagebox.showwarning(
                "Atenție",
                f"{len(self.rezultat_curent.piese_neincapute)} piese depășesc dimensiunile colii!"
            )

        self.coala_activa_idx = 0
        self._actualizeaza_vizualizare()

    def _coala_anterioara(self):
        if self.rezultat_curent and self.coala_activa_idx > 0:
            self.coala_activa_idx -= 1
            self._actualizeaza_vizualizare()

    def _coala_urmatoare(self):
        if self.rezultat_curent and self.coala_activa_idx < len(self.rezultat_curent.coli) - 1:
            self.coala_activa_idx += 1
            self._actualizeaza_vizualizare()

    def _actualizeaza_vizualizare(self):
        if not self.rezultat_curent or not self.coala_setari:
            return

        total_coli = len(self.rezultat_curent.coli)
        coala_curenta: CoalaCalculata = self.rezultat_curent.coli[self.coala_activa_idx]

        self.lbl_pagina.config(text=f"Coala {self.coala_activa_idx + 1} din {total_coli}")
        self.btn_prev.config(state=tk.NORMAL if self.coala_activa_idx > 0 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.coala_activa_idx < total_coli - 1 else tk.DISABLED)

        self.eticheta_statistici.config(
            text=f"Total coli: {total_coli} | Deșeu coală: {coala_curenta.procent_deseu:.1f}% | Deșeu mediu: {self.rezultat_curent.procent_mediu_deseu:.1f}%"
        )

        self._deseneaza_schita(self.coala_setari, coala_curenta.piese_amplasate)

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
        