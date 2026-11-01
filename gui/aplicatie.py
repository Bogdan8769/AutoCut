import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
from core.modele import Coala, Piesa, PiesaAmplasata
from core.optimizator import OptimizatorDebitare, RezultatOptimizare, CoalaCalculata
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AplicatieAutoCut(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoCut Pro - Sistem Inteligent Debitare PAL")
        self.geometry("1240x780")
        self.minsize(1050, 680)

        self.lista_piese: list[Piesa] = []
        self.rezultat_curent: RezultatOptimizare | None = None
        self.coala_activa_idx: int = 0
        self.coala_setari: Coala | None = None

        self.construieste_interfata()

    def construieste_interfata(self):
        # 1. Panou Control Stânga (Scrollable pentru flexibilitate)
        panou_stanga = ctk.CTkScrollableFrame(self, width=380, corner_radius=12)
        panou_stanga.pack(side="left", fill="y", padx=15, pady=15)

        titlu_app = ctk.CTkLabel(
            panou_stanga, text="AutoCut Pro", font=ctk.CTkFont(size=22, weight="bold")
        )
        titlu_app.pack(anchor="w", pady=(5, 15))

        # --- Secțiunea 1: Parametri Coală ---
        cadru_coala = ctk.CTkFrame(panou_stanga, corner_radius=10)
        cadru_coala.pack(fill="x", pady=8, padx=5)

        ctk.CTkLabel(
            cadru_coala, text="1. Parametri Coală Brută (mm)", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 8))

        grid_coala = ctk.CTkFrame(cadru_coala, fg_color="transparent")
        grid_coala.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(grid_coala, text="Lungime:").grid(row=0, column=0, sticky="w", pady=4)
        self.camp_lungime_coala = ctk.CTkEntry(grid_coala, width=90)
        self.camp_lungime_coala.insert(0, "2800")
        self.camp_lungime_coala.grid(row=0, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_coala, text="Lățime:").grid(row=1, column=0, sticky="w", pady=4)
        self.camp_latime_coala = ctk.CTkEntry(grid_coala, width=90)
        self.camp_latime_coala.insert(0, "2070")
        self.camp_latime_coala.grid(row=1, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_coala, text="Pânză (disc):").grid(row=2, column=0, sticky="w", pady=4)
        self.camp_panza = ctk.CTkEntry(grid_coala, width=90)
        self.camp_panza.insert(0, "4")
        self.camp_panza.grid(row=2, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_coala, text="Tivire margine:").grid(row=3, column=0, sticky="w", pady=4)
        self.camp_tivire = ctk.CTkEntry(grid_coala, width=90)
        self.camp_tivire.insert(0, "10")
        self.camp_tivire.grid(row=3, column=1, padx=5, pady=4)

        # --- Secțiunea 2: Adăugare Piese ---
        cadru_piese = ctk.CTkFrame(panou_stanga, corner_radius=10)
        cadru_piese.pack(fill="x", pady=8, padx=5)

        ctk.CTkLabel(
            cadru_piese, text="2. Adăugare Piesă Nouă", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 8))

        grid_piese = ctk.CTkFrame(cadru_piese, fg_color="transparent")
        grid_piese.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(grid_piese, text="Denumire:").grid(row=0, column=0, sticky="w", pady=4)
        self.camp_nume_piesa = ctk.CTkEntry(grid_piese, width=130)
        self.camp_nume_piesa.insert(0, "Ușă dulap")
        self.camp_nume_piesa.grid(row=0, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_piese, text="Lungime:").grid(row=1, column=0, sticky="w", pady=4)
        self.camp_lungime_piesa = ctk.CTkEntry(grid_piese, width=130, placeholder_text="ex: 700")
        self.camp_lungime_piesa.grid(row=1, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_piese, text="Lățime:").grid(row=2, column=0, sticky="w", pady=4)
        self.camp_latime_piesa = ctk.CTkEntry(grid_piese, width=130, placeholder_text="ex: 450")
        self.camp_latime_piesa.grid(row=2, column=1, padx=5, pady=4)

        ctk.CTkLabel(grid_piese, text="Cantitate:").grid(row=3, column=0, sticky="w", pady=4)
        self.camp_cantitate_piesa = ctk.CTkEntry(grid_piese, width=130)
        self.camp_cantitate_piesa.insert(0, "2")
        self.camp_cantitate_piesa.grid(row=3, column=1, padx=5, pady=4)

        self.bifa_rotatie = ctk.BooleanVar(value=True)
        self.check_rotatie = ctk.CTkCheckBox(
            cadru_piese, text="Permite rotație (fibră)", variable=self.bifa_rotatie
        )
        self.check_rotatie.pack(anchor="w", padx=10, pady=(5, 10))

        btn_adauga = ctk.CTkButton(
            cadru_piese, text="➕ Adaugă în Comandă", fg_color="#27ae60", hover_color="#219150", command=self._adauga_piesa
        )
        btn_adauga.pack(fill="x", padx=10, pady=(0, 10))

        # --- Secțiunea 3: Tabel Piese ---
        cadru_tabel = ctk.CTkFrame(panou_stanga, corner_radius=10)
        cadru_tabel.pack(fill="both", expand=True, pady=8, padx=5)

        ctk.CTkLabel(
            cadru_tabel, text="3. Piese de Debitat", font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        # Stil modern pentru Treeview nativ
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            rowheight=26,
            font=("Segoe UI", 9)
        )
        stil.configure("Treeview.Heading", background="#1f1f1f", foreground="#3a7ebf", font=("Segoe UI", 9, "bold"))
        stil.map("Treeview", background=[("selected", "#1f538d")])

        self.tabel = ttk.Treeview(cadru_tabel, columns=("nume", "l", "w", "cant"), show="headings", height=6)
        self.tabel.heading("nume", text="Piesă")
        self.tabel.heading("l", text="L (mm)")
        self.tabel.heading("w", text="l (mm)")
        self.tabel.heading("cant", text="Buc")
        self.tabel.column("nume", width=120)
        self.tabel.column("l", width=60)
        self.tabel.column("w", width=60)
        self.tabel.column("cant", width=45)
        self.tabel.pack(fill="both", expand=True, padx=8, pady=5)

        btn_sterge = ctk.CTkButton(
            cadru_tabel, text="🗑️ Șterge Piesa Selectată", fg_color="#c0392b", hover_color="#962d22", height=28, command=self._sterge_piesa
        )
        btn_sterge.pack(fill="x", padx=8, pady=(0, 10))

        # Buton Principal de Calcul
        btn_calculeaza = ctk.CTkButton(
            panou_stanga, text="⚡ CALCULEAZĂ OPTIMIZARE", height=42, font=ctk.CTkFont(size=13, weight="bold"), command=self._ruleaza_optimizarea
        )
        btn_calculeaza.pack(fill="x", pady=15, padx=5)

        # --- Panoul din Dreapta: Schiță 2D și Navigare ---
        panou_dreapta = ctk.CTkFrame(self, corner_radius=12)
        panou_dreapta.pack(side="right", fill="both", expand=True, padx=(0, 15), pady=15)

        bara_navigare = ctk.CTkFrame(panou_dreapta, fg_color="transparent")
        bara_navigare.pack(fill="x", padx=15, pady=12)

        self.btn_prev = ctk.CTkButton(
            bara_navigare, text="◀ Înapoi", width=85, state="disabled", command=self._coala_anterioara
        )
        self.btn_prev.pack(side="left")

        self.lbl_pagina = ctk.CTkLabel(
            bara_navigare, text="Coala 0 / 0", font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_pagina.pack(side="left", padx=15)

        self.btn_next = ctk.CTkButton(
            bara_navigare, text="Înainte ▶", width=85, state="disabled", command=self._coala_urmatoare
        )
        self.btn_next.pack(side="left")

        self.btn_export = ctk.CTkButton(
            bara_navigare, 
            text="📷 Exportă Schița (PNG)", 
            width=140, 
            fg_color="#e67e22", 
            hover_color="#d35400", 
            command=self._exporta_schita
        )
        self.btn_export.pack(side="left", padx=10)

        self.eticheta_statistici = ctk.CTkLabel(
            bara_navigare,
            text="Adăugați piese și calculați debitarea",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        self.eticheta_statistici.pack(side="right")

        # Canvas grafic
        self.canvas_schita = tk.Canvas(panou_dreapta, bg="#181818", highlightthickness=0)
        self.canvas_schita.pack(fill="both", expand=True, padx=15, pady=(0, 15))

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

            self.tabel.insert("", "end", values=(nume, int(lungime), int(latime), cantitate))
            self.camp_lungime_piesa.delete(0, "end")
            self.camp_latime_piesa.delete(0, "end")
        except ValueError:
            messagebox.showerror("Eroare", "Dimensiunile și cantitatea trebuie să fie numere strict pozitive!")

    def _sterge_piesa(self):
        selectie = self.tabel.selection()
        if not selectie:
            messagebox.showinfo("Informație", "Selectează un rând din tabel pentru a-l șterge.")
            return

        for item in selectie:
            index = self.tabel.index(item)
            del self.lista_piese[index]
            self.tabel.delete(item)

    def _ruleaza_optimizarea(self):
        if not self.lista_piese:
            messagebox.showwarning("Atenție", "Adăugați cel puțin o piesă înainte de debitare!")
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
            messagebox.showerror("Eroare", "Piesele sunt prea mari chiar și pentru o coală goală!")
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

        self.lbl_pagina.configure(text=f"Coala {self.coala_activa_idx + 1} din {total_coli}")
        self.btn_prev.configure(state="normal" if self.coala_activa_idx > 0 else "disabled")
        self.btn_next.configure(state="normal" if self.coala_activa_idx < total_coli - 1 else "disabled")

        self.eticheta_statistici.configure(
            text=f"Total coli: {total_coli} | Deșeu coala {self.coala_activa_idx + 1}: {coala_curenta.procent_deseu:.1f}% | Deșeu global: {self.rezultat_curent.procent_mediu_deseu:.1f}%"
        )

        self._deseneaza_schita(self.coala_setari, coala_curenta.piese_amplasate)

    def _deseneaza_schita(self, coala: Coala, piese_amplasate: list[PiesaAmplasata]):
        self.canvas_schita.delete("all")
        latime_ecran = self.canvas_schita.winfo_width()
        inaltime_ecran = self.canvas_schita.winfo_height()

        if latime_ecran <= 50 or inaltime_ecran <= 50:
            return

        margine_canvas = 40
        spatiu_util_w = latime_ecran - 2 * margine_canvas
        spatiu_util_h = inaltime_ecran - 2 * margine_canvas

        scara = min(spatiu_util_w / coala.lungime, spatiu_util_h / coala.latime)

        orig_x = (latime_ecran - (coala.lungime * scara)) / 2
        orig_y = (inaltime_ecran - (coala.latime * scara)) / 2

        # 1. Umbră elegantă sub coala de PAL
        self.canvas_schita.create_rectangle(
            orig_x + 6, orig_y + 6,
            orig_x + (coala.lungime * scara) + 6,
            orig_y + (coala.latime * scara) + 6,
            fill="#101010", outline=""
        )

        # 2. Desenare Coală Brută (PAL bej deschis mat)
        self.canvas_schita.create_rectangle(
            orig_x, orig_y,
            orig_x + (coala.lungime * scara),
            orig_y + (coala.latime * scara),
            fill="#d9c3a3", outline="#ffffff", width=2
        )

        # 3. Linie punctată tivire (margine de siguranță)
        if coala.margine_tivire > 0:
            tx = coala.margine_tivire * scara
            self.canvas_schita.create_rectangle(
                orig_x + tx, orig_y + tx,
                orig_x + (coala.lungime * scara) - tx,
                orig_y + (coala.latime * scara) - tx,
                outline="#8c7b66", dash=(4, 4), width=1
            )

        # Paletă de culori profesionale pentru piese
        culori = ["#2980b9", "#27ae60", "#8e44ad", "#d35400", "#16a085", "#2c3e50"]

        # 4. Desenare Piese
        for idx, p in enumerate(piese_amplasate):
            px1 = orig_x + (p.x * scara)
            py1 = orig_y + (p.y * scara)
            px2 = px1 + (p.lungime * scara)
            py2 = py1 + (p.latime * scara)

            # Culoare stabilă bazată pe numele piesei
            culoare_umplere = culori[hash(p.nume_piesa) % len(culori)]

            self.canvas_schita.create_rectangle(
                px1, py1, px2, py2,
                fill=culoare_umplere, outline="#ffffff", width=1
            )

            w_box = px2 - px1
            h_box = py2 - py1

            # Afișare etichetă dacă piesa este suficient de vizibilă
            if w_box > 40 and h_box > 22:
                rot_indicator = " ⟳" if getattr(p, 'rotita', getattr(p, 'rotatia', False)) else ""
                text_eticheta = f"{p.nume_piesa}{rot_indicator}\n{int(p.lungime)}×{int(p.latime)}"
                self.canvas_schita.create_text(
                    (px1 + px2) / 2, (py1 + py2) / 2,
                    text=text_eticheta, fill="#ffffff",
                    font=("Segoe UI", 8, "bold"), justify="center"
                )
                
    def _exporta_schita(self):
        if not self.rezultat_curent or not self.coala_setari:
            messagebox.showwarning("Atenție", "Trebuie să calculați debitarea înainte de a exporta schița!")
            return

        cale_salvare = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Fișiere PNG", "*.png"), ("Toate fișierele", "*.*")],
            title="Salvează Fișa de Debitare"
        )

        if not cale_salvare:
            return

        coala = self.coala_setari
        coala_curenta = self.rezultat_curent.coli[self.coala_activa_idx]

        # Rezoluție înaltă pentru imprimare (2400 x 1600 px)
        latime_img = 2400
        inaltime_img = 1600
        imagine = Image.new("RGB", (latime_img, inaltime_img), color="#1e1e1e")
        desen = ImageDraw.Draw(imagine)

        # Calcul scalare
        margine = 120
        zona_w = latime_img - 2 * margine
        zona_h = inaltime_img - 2 * margine - 100  # spațiu pentru antet
        scara = min(zona_w / coala.lungime, zona_h / coala.latime)

        orig_x = (latime_img - (coala.lungime * scara)) / 2
        orig_y = ((inaltime_img - 100) - (coala.latime * scara)) / 2 + 100

        # Antet fișă tehnică
        antet_text = (
            f"FISA DE DEBITARE - COALA {self.coala_activa_idx + 1} DIN {len(self.rezultat_curent.coli)} | "
            f"Dimensiuni: {int(coala.lungime)}x{int(coala.latime)} mm | Tivire: {int(coala.margine_tivire)} mm | "
            f"Panza: {int(coala.grosime_panza)} mm | Deseu coala: {coala_curenta.procent_deseu:.1f}%"
        )
        desen.text((orig_x, 40), antet_text, fill="#ffffff")

        # Desenare placă brută
        desen.rectangle(
            [orig_x, orig_y, orig_x + (coala.lungime * scara), orig_y + (coala.latime * scara)],
            fill="#d9c3a3", outline="#ffffff", width=4
        )

        # Desenare margine tivire
        if coala.margine_tivire > 0:
            tx = coala.margine_tivire * scara
            desen.rectangle(
                [orig_x + tx, orig_y + tx, orig_x + (coala.lungime * scara) - tx, orig_y + (coala.latime * scara) - tx],
                outline="#8c7b66", width=2
            )

        # Paletă culori pentru piese
        culori = ["#2980b9", "#27ae60", "#8e44ad", "#d35400", "#16a085", "#2c3e50"]

        # Desenare piese decupate
        for p in coala_curenta.piese_amplasate:
            px1 = orig_x + (p.x * scara)
            py1 = orig_y + (p.y * scara)
            px2 = px1 + (p.lungime * scara)
            py2 = py1 + (p.latime * scara)

            culoare = culori[hash(p.nume_piesa) % len(culori)]
            desen.rectangle([px1, py1, px2, py2], fill=culoare, outline="#ffffff", width=2)

            # Text dimensiuni pe piesă
            w_box = px2 - px1
            h_box = py2 - py1
            if w_box > 60 and h_box > 40:
                rot_txt = " (R)" if getattr(p, 'rotita', getattr(p, 'rotatia', False)) else ""
                info_piesa = f"{p.nume_piesa}{rot_txt}\n{int(p.lungime)}x{int(p.latime)} mm"
                desen.text((px1 + 8, py1 + 8), info_piesa, fill="#ffffff")

        imagine.save(cale_salvare, "PNG")
        messagebox.showinfo("Succes", f"Fișa tehnică a fost salvată cu succes:\n{cale_salvare}")
                