import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageDraw
from core.modele import Coala, Piesa
from core.optimizator import OptimizatorDebitare

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AplicatieAutoCut(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AutoCut - Debitare PAL & Cantuire")
        self.geometry("1340x800")

        self.lista_piese = []
        self.rezultat = None
        self.pagina_curenta = 0
        self.coala_setari = None

        self.tipare_cant = {
            "Fără": (0, 0),
            "│": (1, 0),
            "║": (2, 0),
            "─": (0, 1),
            "═": (0, 2),
            "└": (1, 1),
            "⊐": (1, 2),
            "⊔": (2, 1), 
            "□": (2, 2)  
        }
        self.profil_selectat = "Fără"

        self.creeaza_gui()

    def creeaza_gui(self):
        # --- Panou Stanga ---
        panou_stanga = ctk.CTkFrame(self, width=420, corner_radius=10)
        panou_stanga.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(panou_stanga, text="1. Parametri Coală (mm)", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=10, pady=(8, 2))

        f_coala = ctk.CTkFrame(panou_stanga, fg_color="transparent")
        f_coala.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(f_coala, text="Lungime:").grid(row=0, column=0, sticky="w", pady=2)
        self.txt_L_coala = ctk.CTkEntry(f_coala, width=75)
        self.txt_L_coala.insert(0, "2800")
        self.txt_L_coala.grid(row=0, column=1, padx=5, pady=2)

        ctk.CTkLabel(f_coala, text="Lățime:").grid(row=0, column=2, sticky="w", pady=2, padx=(10, 0))
        self.txt_l_coala = ctk.CTkEntry(f_coala, width=75)
        self.txt_l_coala.insert(0, "2070")
        self.txt_l_coala.grid(row=0, column=3, padx=5, pady=2)

        ctk.CTkLabel(f_coala, text="Pânză:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_panza = ctk.CTkEntry(f_coala, width=75)
        self.txt_panza.insert(0, "4")
        self.txt_panza.grid(row=1, column=1, padx=5, pady=2)

        ctk.CTkLabel(f_coala, text="Tivire:").grid(row=1, column=2, sticky="w", pady=2, padx=(10, 0))
        self.txt_tivire = ctk.CTkEntry(f_coala, width=75)
        self.txt_tivire.insert(0, "10")
        self.txt_tivire.grid(row=1, column=3, padx=5, pady=2)

        # 2. Adaugare Piesa
        ctk.CTkLabel(panou_stanga, text="2. Adăugare Piesă", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=10, pady=(10, 2))

        f_piesa = ctk.CTkFrame(panou_stanga, fg_color="transparent")
        f_piesa.pack(fill="x", padx=10, pady=2)

        ctk.CTkLabel(f_piesa, text="Nume:").grid(row=0, column=0, sticky="w", pady=2)
        self.txt_nume = ctk.CTkEntry(f_piesa, width=120)
        self.txt_nume.insert(0, "Ușă")
        self.txt_nume.grid(row=0, column=1, padx=5, pady=2)

        ctk.CTkLabel(f_piesa, text="Cantitate:").grid(row=0, column=2, sticky="w", pady=2, padx=(5, 0))
        self.txt_cantitate = ctk.CTkEntry(f_piesa, width=65)
        self.txt_cantitate.insert(0, "1")
        self.txt_cantitate.grid(row=0, column=3, padx=5, pady=2)

        ctk.CTkLabel(f_piesa, text="Lungime:").grid(row=1, column=0, sticky="w", pady=2)
        self.txt_L_piesa = ctk.CTkEntry(f_piesa, width=120)
        self.txt_L_piesa.grid(row=1, column=1, padx=5, pady=2)

        ctk.CTkLabel(f_piesa, text="Lățime:").grid(row=1, column=2, sticky="w", pady=2, padx=(5, 0))
        self.txt_l_piesa = ctk.CTkEntry(f_piesa, width=65)
        self.txt_l_piesa.grid(row=1, column=3, padx=5, pady=2)

        # Zona Simboluri Cant
        f_cant = ctk.CTkFrame(panou_stanga, corner_radius=6)
        f_cant.pack(fill="x", padx=10, pady=6)

        f_grosime = ctk.CTkFrame(f_cant, fg_color="transparent")
        f_grosime.pack(fill="x", padx=8, pady=(4, 2))

        ctk.CTkLabel(f_grosime, text="Grosime cant (mm):", font=("Segoe UI", 11, "bold")).pack(side="left")
        self.combo_grosime_cant = ctk.CTkComboBox(f_grosime, values=["0.4", "0.8", "1", "2"], width=75)
        self.combo_grosime_cant.set("2")
        self.combo_grosime_cant.pack(side="left", padx=10)

        ctk.CTkLabel(f_cant, text="Selectează laturile cantuite:", font=("Segoe UI", 10)).pack(anchor="w", padx=8, pady=(4, 2))

        f_butoane_cant = ctk.CTkFrame(f_cant, fg_color="transparent")
        f_butoane_cant.pack(fill="x", padx=6, pady=(0, 6))

        self.butoane_profil = {}
        profiluri = ["Fără", "│", "║", "─", "═", "└", "⊐", "⊔", "□"]

        for idx, p in enumerate(profiluri):
            r = idx // 5  # asezam cate 5 pe rand ca sa incapa frumos
            c = idx % 5
            culoare_bg = "#1f538d" if p == "Fără" else "#333333"
            marime_font = 10 if p == "Fără" else 14

            btn = ctk.CTkButton(
                f_butoane_cant,
                text=p,
                width=38,
                height=28,
                font=("Segoe UI", marime_font, "bold"),
                fg_color=culoare_bg,
                command=lambda val=p: self._selecteaza_profil_cant(val)
            )
            btn.grid(row=r, column=c, padx=2, pady=2)
            self.butoane_profil[p] = btn

        self.bifa_rotatie = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(panou_stanga, text="Permite rotire", variable=self.bifa_rotatie).pack(anchor="w", padx=15, pady=4)

        ctk.CTkButton(panou_stanga, text="Adaugă Piesă", fg_color="#27ae60", hover_color="#219150", command=self.adauga_piesa).pack(fill="x", padx=10, pady=5)

        # Stil Dark Mode pentru Tabel
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("Treeview", background="#252525", foreground="#ffffff", fieldbackground="#252525", rowheight=24, borderwidth=0, font=("Segoe UI", 9))
        stil.configure("Treeview.Heading", background="#333333", foreground="#38b6ff", relief="flat", font=("Segoe UI", 9, "bold"))
        stil.map("Treeview", background=[("selected", "#1f538d")])

        self.tabel = ttk.Treeview(panou_stanga, columns=("nume", "L", "l", "cant", "profil", "L_fin", "l_fin"), show="headings", height=6)
        self.tabel.heading("nume", text="Piesă")
        self.tabel.heading("L", text="Lungime")
        self.tabel.heading("l", text="Lățime")
        self.tabel.heading("cant", text="Buc")
        self.tabel.heading("profil", text="Cant")
        self.tabel.heading("L_fin", text="L Fin")
        self.tabel.heading("l_fin", text="l Fin")

        self.tabel.column("nume", width=75)
        self.tabel.column("L", width=55, anchor="center")
        self.tabel.column("l", width=50, anchor="center")
        self.tabel.column("cant", width=35, anchor="center")
        self.tabel.column("profil", width=65, anchor="center")
        self.tabel.column("L_fin", width=45, anchor="center")
        self.tabel.column("l_fin", width=45, anchor="center")
        self.tabel.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(panou_stanga, text="Șterge Piesă", fg_color="#c0392b", hover_color="#962d22", height=28, command=self.sterge_piesa).pack(fill="x", padx=10, pady=3)
        ctk.CTkButton(panou_stanga, text="CALCULEAZĂ", height=38, font=("Segoe UI", 12, "bold"), command=self.calculeaza).pack(fill="x", padx=10, pady=(10, 8))

        # --- Panou Dreapta ---
        panou_dreapta = ctk.CTkFrame(self, corner_radius=10)
        panou_dreapta.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        nav = ctk.CTkFrame(panou_dreapta, fg_color="transparent")
        nav.pack(fill="x", padx=10, pady=5)

        self.btn_inapoi = ctk.CTkButton(nav, text="◀ Înapoi", width=80, state="disabled", command=self.pagina_inapoi)
        self.btn_inapoi.pack(side="left")

        self.lbl_pag = ctk.CTkLabel(nav, text="Coala 0/0", font=("Segoe UI", 12, "bold"))
        self.lbl_pag.pack(side="left", padx=12)

        self.btn_inainte = ctk.CTkButton(nav, text="Înainte ▶", width=80, state="disabled", command=self.pagina_inainte)
        self.btn_inainte.pack(side="left")

        self.btn_export = ctk.CTkButton(nav, text="📷 Export Schiță", width=110, fg_color="#d35400", hover_color="#b94600", command=self.exporta_schita)
        self.btn_export.pack(side="left", padx=12)

        self.lbl_stat = ctk.CTkLabel(nav, text="", font=("Segoe UI", 11))
        self.lbl_stat.pack(side="right")

        self.canvas = tk.Canvas(panou_dreapta, bg="#181818", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def _selecteaza_profil_cant(self, profil):
        self.profil_selectat = profil
        for nume_b, btn in self.butoane_profil.items():
            if nume_b == profil:
                btn.configure(fg_color="#1f538d")
            else:
                btn.configure(fg_color="#333333")

    def adauga_piesa(self):
        try:
            nume = self.txt_nume.get() or "Piesă"
            L = float(self.txt_L_piesa.get())
            l = float(self.txt_l_piesa.get())
            cant = int(self.txt_cantitate.get())

            if L <= 0 or l <= 0 or cant <= 0:
                return

            grosime_cant = float(self.combo_grosime_cant.get())
            lat_L, lat_l = self.tipare_cant[self.profil_selectat]

            piesa = Piesa(
                nume, L, l, cant, self.bifa_rotatie.get(),
                cant_lungime=grosime_cant,
                cant_latime=grosime_cant,
                laturi_cant_l=lat_L,
                laturi_cant_w=lat_l
            )
            self.lista_piese.append(piesa)

            text_cant_tabel = f"{self.profil_selectat} ({grosime_cant})" if self.profil_selectat != "Fără" else "-"

            self.tabel.insert("", "end", values=(
                nume,
                int(piesa.lungime),
                int(piesa.latime),
                cant,
                text_cant_tabel,
                f"{piesa.lungime_finita:.1f}".rstrip('0').rstrip('.'),
                f"{piesa.latime_finita:.1f}".rstrip('0').rstrip('.')
            ))
            self.txt_L_piesa.delete(0, "end")
            self.txt_l_piesa.delete(0, "end")
        except ValueError:
            messagebox.showerror("Eroare", "Date invalide!")

    def sterge_piesa(self):
        sel = self.tabel.selection()
        for item in sel:
            idx = self.tabel.index(item)
            del self.lista_piese[idx]
            self.tabel.delete(item)

    def calculeaza(self):
        if not self.lista_piese:
            return

        try:
            self.coala_setari = Coala(self.txt_L_coala.get(), self.txt_l_coala.get(), self.txt_panza.get(), self.txt_tivire.get())
        except ValueError:
            return

        opt = OptimizatorDebitare(self.coala_setari)
        self.rezultat = opt.optimizeaza(self.lista_piese)
        self.pagina_curenta = 0
        self.afiseaza_coala()

    def pagina_inapoi(self):
        if self.rezultat and self.pagina_curenta > 0:
            self.pagina_curenta -= 1
            self.afiseaza_coala()

    def pagina_inainte(self):
        if self.rezultat and self.pagina_curenta < len(self.rezultat.coli) - 1:
            self.pagina_curenta += 1
            self.afiseaza_coala()

    def afiseaza_coala(self):
        if not self.rezultat or not self.rezultat.coli:
            return

        total = len(self.rezultat.coli)
        c = self.rezultat.coli[self.pagina_curenta]

        self.lbl_pag.configure(text=f"Coala {self.pagina_curenta + 1}/{total}")
        self.btn_inapoi.configure(state="normal" if self.pagina_curenta > 0 else "disabled")
        self.btn_inainte.configure(state="normal" if self.pagina_curenta < total - 1 else "disabled")
        self.lbl_stat.configure(text=f"Deșeu: {c.procent_deseu:.1f}% | Deșeu mediu: {self.rezultat.procent_mediu_deseu:.1f}%")

        self.deseneaza(c.piese_amplasate)

    def deseneaza(self, piese):
        self.canvas.delete("all")
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        coala = self.coala_setari
        scara = min((cw - 40) / coala.lungime, (ch - 40) / coala.latime)
        ox = (cw - coala.lungime * scara) / 2
        oy = (ch - coala.latime * scara) / 2

        self.canvas.create_rectangle(ox, oy, ox + coala.lungime * scara, oy + coala.latime * scara, fill="#d9c3a3", outline="white", width=2)

        if coala.margine_tivire > 0:
            t = coala.margine_tivire * scara
            self.canvas.create_rectangle(ox + t, oy + t, ox + coala.lungime * scara - t, oy + coala.latime * scara - t, outline="#8c7b66", dash=(4, 4))

        culori = ["#2980b9", "#27ae60", "#8e44ad", "#d35400", "#16a085"]

        for p in piese:
            x1 = ox + p.x * scara
            y1 = oy + p.y * scara
            x2 = x1 + p.lungime * scara
            y2 = y1 + p.latime * scara

            col = culori[hash(p.nume) % len(culori)]
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=col, outline="#ffffff")

            # Linii de cant (galbene)
            orig = p.piesa_originala
            if orig:
                lat_L = orig.laturi_cant_l
                lat_l = orig.laturi_cant_w

                lat_oriz = lat_l if p.rotita else lat_L
                lat_vert = lat_L if p.rotita else lat_l

                if lat_oriz >= 1:
                    self.canvas.create_line(x1, y1, x2, y1, fill="#f1c40f", width=3)
                if lat_oriz == 2:
                    self.canvas.create_line(x1, y2, x2, y2, fill="#f1c40f", width=3)

                if lat_vert >= 1:
                    self.canvas.create_line(x1, y1, x1, y2, fill="#f1c40f", width=3)
                if lat_vert == 2:
                    self.canvas.create_line(x2, y1, x2, y2, fill="#f1c40f", width=3)

            if (x2 - x1) > 35 and (y2 - y1) > 20:
                txt = f"{p.nume}\n{int(p.lungime)}x{int(p.latime)}"
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=txt, fill="white", font=("Segoe UI", 8, "bold"))

    def exporta_schita(self):
        if not self.rezultat or not self.coala_setari:
            messagebox.showwarning("Atenție", "Calculează debitarea înainte de export!")
            return

        cale = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagine PNG", "*.png")], title="Salvează schița de debitare")
        if not cale:
            return

        coala = self.coala_setari
        coala_curenta = self.rezultat.coli[self.pagina_curenta]

        w_img, h_img = 2200, 1500
        img = Image.new("RGB", (w_img, h_img), color="#1e1e1e")
        draw = ImageDraw.Draw(img)

        scara = min((w_img - 160) / coala.lungime, (h_img - 240) / coala.latime)
        ox = (w_img - coala.lungime * scara) / 2
        oy = ((h_img - 100) - coala.latime * scara) / 2 + 100

        info = f"AutoCut - Coala {self.pagina_curenta + 1}/{len(self.rezultat.coli)} | Dim: {int(coala.lungime)}x{int(coala.latime)} mm | Deșeu: {coala_curenta.procent_deseu:.1f}%"
        draw.text((ox, 40), info, fill="white")

        draw.rectangle([ox, oy, ox + coala.lungime * scara, oy + coala.latime * scara], fill="#d9c3a3", outline="white", width=3)

        if coala.margine_tivire > 0:
            t = coala.margine_tivire * scara
            draw.rectangle([ox + t, oy + t, ox + coala.lungime * scara - t, oy + coala.latime * scara - t], outline="#8c7b66", width=2)

        culori = ["#2980b9", "#27ae60", "#8e44ad", "#d35400", "#16a085"]

        for p in coala_curenta.piese_amplasate:
            x1 = ox + p.x * scara
            y1 = oy + p.y * scara
            x2 = x1 + p.lungime * scara
            y2 = y1 + p.latime * scara

            col = culori[hash(p.nume) % len(culori)]
            draw.rectangle([x1, y1, x2, y2], fill=col, outline="white", width=2)

            orig = p.piesa_originala
            if orig:
                lat_L = orig.laturi_cant_l
                lat_l = orig.laturi_cant_w

                lat_oriz = lat_l if p.rotita else lat_L
                lat_vert = lat_L if p.rotita else lat_l

                if lat_oriz >= 1:
                    draw.line([(x1, y1), (x2, y1)], fill="#f1c40f", width=4)
                if lat_oriz == 2:
                    draw.line([(x1, y2), (x2, y2)], fill="#f1c40f", width=4)
                if lat_vert >= 1:
                    draw.line([(x1, y1), (x1, y2)], fill="#f1c40f", width=4)
                if lat_vert == 2:
                    draw.line([(x2, y1), (x2, y2)], fill="#f1c40f", width=4)

            if (x2 - x1) > 50 and (y2 - y1) > 30:
                txt = f"{p.nume} ({int(p.lungime)}x{int(p.latime)})"
                draw.text((x1 + 6, y1 + 6), txt, fill="white")

        img.save(cale, "PNG")
        messagebox.showinfo("Succes", f"Schița a fost exportată cu succes:\n{cale}")