import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tkinter.ttk import Progressbar

TEXTO = {
    'es': {
        'titulo': "CookieHunter",
        'tab1': "Extraer",
        'tab2': "Buscar",
        'archivo': "Archivo",
        'examinar': "Examinar",
        'extraer': "Extraer",
        'original': "Original",
        'limpia': "Limpia",
        'copiar': "Copiar",
        'carpeta': "Carpeta",
        'buscar': "Buscar",
        'resultados': "Resultados",
        'listo': "Listo",
        'copiada_orig': "Original copiada",
        'copiada_clean': "Limpia copiada",
        'error_archivo': "Archivo inválido",
        'error_cookie': "Cookie no encontrada",
        'error_carpeta': "Carpeta inválida",
        'sin_cookie': "Extrae una cookie primero",
        'sin_archivos': "Sin archivos",
        'encontrada': "Cookie en {} archivo(s)",
        'no_encontrada': "Cookie no encontrada",
        'guardar': "Guardar lista",
        'guardado': "Lista guardada",
        'dev_activo': "Modo dev activo",
        'dev_inactivo': "Modo normal",
        'config_titulo': "Configuración",
        'dev_label': "Modo desarrollador",
        'by': "by Elias"
    },
    'en': {
        'titulo': "CookieHunter",
        'tab1': "Extract",
        'tab2': "Search",
        'archivo': "File",
        'examinar': "Browse",
        'extraer': "Extract",
        'original': "Original",
        'limpia': "Clean",
        'copiar': "Copy",
        'carpeta': "Folder",
        'buscar': "Search",
        'resultados': "Results",
        'listo': "Ready",
        'copiada_orig': "Original copied",
        'copiada_clean': "Clean copied",
        'error_archivo': "Invalid file",
        'error_cookie': "Cookie not found",
        'error_carpeta': "Invalid folder",
        'sin_cookie': "Extract a cookie first",
        'sin_archivos': "No files",
        'encontrada': "Cookie in {} file(s)",
        'no_encontrada': "Cookie not found",
        'guardar': "Save list",
        'guardado': "List saved",
        'dev_activo': "Dev mode on",
        'dev_inactivo': "Normal mode",
        'config_titulo': "Settings",
        'dev_label': "Developer mode",
        'by': "by Elias"
    },
    'ru': {
        'titulo': "CookieHunter",
        'tab1': "Извлечь",
        'tab2': "Найти",
        'archivo': "Файл",
        'examinar': "Обзор",
        'extraer': "Извлечь",
        'original': "Оригинал",
        'limpia': "Очищенная",
        'copiar': "Копировать",
        'carpeta': "Папка",
        'buscar': "Найти",
        'resultados': "Результаты",
        'listo': "Готово",
        'copiada_orig': "Оригинал скопирован",
        'copiada_clean': "Очищенная скопирована",
        'error_archivo': "Неверный файл",
        'error_cookie': "Кука не найдена",
        'error_carpeta': "Неверная папка",
        'sin_cookie': "Сначала извлеките куку",
        'sin_archivos': "Нет файлов",
        'encontrada': "Кука в {} файле(ах)",
        'no_encontrada': "Кука не найдена",
        'guardar': "Сохранить список",
        'guardado': "Список сохранён",
        'dev_activo': "Dev режим",
        'dev_inactivo': "Обычный режим",
        'config_titulo': "Настройки",
        'dev_label': "Режим разработчика",
        'by': "от Elias"
    }
}

class CookieHunter:
    def __init__(self, root):
        self.root = root
        self.idioma = 'es'
        self.t = TEXTO[self.idioma]
        self.root.title(self.t['titulo'])
        self.root.geometry("920x780")
        self.root.minsize(850, 700)
        self.root.configure(bg="#2c3e50")

        self.cookie_original = ""
        self.cookie_limpia = ""
        self.prefijo = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"
        self.patron_cookie = re.compile(re.escape(self.prefijo) + r'([A-Za-z0-9_\-\.]{100,800})')
        self.modo_dev = False
        self.tema = "claro"

        self.setup_ui()
        self.aplicar_tema()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1a252f", height=50)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.idioma_var = tk.StringVar(value="es")
        combo_idioma = ttk.Combobox(header, textvariable=self.idioma_var, values=["es","en","ru"], width=3, state="readonly")
        combo_idioma.place(x=10, y=12)
        combo_idioma.bind("<<ComboboxSelected>>", self.cambiar_idioma)

        self.tema_var = tk.StringVar(value="claro")
        combo_tema = ttk.Combobox(header, textvariable=self.tema_var, values=["claro","oscuro","azul"], width=6, state="readonly")
        combo_tema.place(x=70, y=12)
        combo_tema.bind("<<ComboboxSelected>>", self.cambiar_tema)

        self.dev_btn = tk.Button(header, text="⚙️", font=("", 12), command=self.abrir_config, bd=0, bg="#1a252f", fg="white", activebackground="#2c3e50")
        self.dev_btn.place(x=150, y=8)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.tab1 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text=self.t['tab1'])

        f1 = tk.LabelFrame(self.tab1, text=self.t['archivo'])
        f1.pack(fill="x", padx=10, pady=8)
        self.entry_file = tk.Entry(f1)
        self.entry_file.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        tk.Button(f1, text=self.t['examinar'], command=self.seleccionar_archivo).pack(side="right", padx=5)

        self.btn_extraer = tk.Button(self.tab1, text=self.t['extraer'], command=self.extraer, bg="#27ae60", fg="white", font=("", 10, "bold"))
        self.btn_extraer.pack(pady=10)

        tk.Label(self.tab1, text=self.t['original'], anchor="w").pack(fill="x", padx=10)
        self.txt_orig = scrolledtext.ScrolledText(self.tab1, height=6, wrap=tk.WORD)
        self.txt_orig.pack(fill="x", padx=10, pady=5)

        tk.Label(self.tab1, text=self.t['limpia'], anchor="w").pack(fill="x", padx=10)
        self.txt_clean = scrolledtext.ScrolledText(self.tab1, height=6, wrap=tk.WORD)
        self.txt_clean.pack(fill="x", padx=10, pady=5)

        cb = tk.Frame(self.tab1)
        cb.pack(pady=5)
        self.btn_copiar_orig = tk.Button(cb, text=f"{self.t['copiar']} Original", command=self.copiar_original)
        self.btn_copiar_orig.pack(side="left", padx=5)
        self.btn_copiar_clean = tk.Button(cb, text=f"{self.t['copiar']} Limpia", command=self.copiar_limpia)
        self.btn_copiar_clean.pack(side="left", padx=5)

        self.tab2 = tk.Frame(self.notebook)
        self.notebook.add(self.tab2, text=self.t['tab2'])

        f2 = tk.LabelFrame(self.tab2, text=self.t['carpeta'])
        f2.pack(fill="x", padx=10, pady=8)
        self.entry_folder = tk.Entry(f2)
        self.entry_folder.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        tk.Button(f2, text=self.t['examinar'], command=self.seleccionar_carpeta).pack(side="right", padx=5)

        self.progress = Progressbar(self.tab2, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.btn_buscar = tk.Button(self.tab2, text=self.t['buscar'], command=self.buscar, bg="#2980b9", fg="white", font=("", 10, "bold"))
        self.btn_buscar.pack(pady=10)

        tk.Label(self.tab2, text=self.t['resultados'], anchor="w").pack(fill="x", padx=10)
        self.txt_resultados = scrolledtext.ScrolledText(self.tab2, height=18, wrap=tk.WORD)
        self.txt_resultados.pack(fill="both", expand=True, padx=10, pady=5)

        self.status = tk.Label(self.root, text=self.t['listo'], bd=1, relief=tk.SUNKEN, anchor="w")
        self.status.pack(side="bottom", fill="x")

    def aplicar_tema(self):
        paletas = {
            "claro": {"bg": "#f0f2f5", "fg": "#000000", "entry": "#ffffff", "frame": "#e0e4e8", "btn": "#d5dbdf"},
            "oscuro": {"bg": "#1e1e1e", "fg": "#e0e0e0", "entry": "#2d2d2d", "frame": "#2a2a2a", "btn": "#3c3c3c"},
            "azul": {"bg": "#1e2a3a", "fg": "#ecf0f1", "entry": "#2c3e50", "frame": "#243342", "btn": "#2c3e50"}
        }
        p = paletas[self.tema]
        self.root.configure(bg=p["bg"])
        for tab in [self.tab1, self.tab2]:
            tab.configure(bg=p["bg"])
        for widget in self.tab1.winfo_children() + self.tab2.winfo_children():
            if isinstance(widget, (tk.LabelFrame, tk.Frame)):
                widget.configure(bg=p["frame"])
                for sub in widget.winfo_children():
                    if isinstance(sub, tk.Label):
                        sub.configure(bg=p["frame"], fg=p["fg"])
                    elif isinstance(sub, tk.Entry):
                        sub.configure(bg=p["entry"], fg=p["fg"], insertbackground=p["fg"])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=p["bg"], fg=p["fg"])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=p["entry"], fg=p["fg"], insertbackground=p["fg"])
        self.txt_orig.configure(bg=p["entry"], fg=p["fg"])
        self.txt_clean.configure(bg=p["entry"], fg=p["fg"])
        self.txt_resultados.configure(bg=p["entry"], fg=p["fg"])
        self.status.configure(bg=p["bg"], fg=p["fg"])
        self.btn_extraer.config(bg="#27ae60" if self.tema=="claro" else "#1e8449")
        self.btn_buscar.config(bg="#2980b9" if self.tema=="claro" else "#1f618d")

    def cambiar_tema(self, event=None):
        self.tema = self.tema_var.get()
        self.aplicar_tema()

    def abrir_config(self):
        ventana = tk.Toplevel(self.root)
        ventana.title(self.t['config_titulo'])
        ventana.geometry("260x140")
        ventana.resizable(False, False)
        ventana.configure(bg="#2c3e50")
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 130
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 70
        ventana.geometry(f"+{x}+{y}")

        var_dev = tk.BooleanVar(value=self.modo_dev)
        def toggle():
            self.modo_dev = var_dev.get()
            if self.modo_dev:
                self.status.config(text=self.t['dev_activo'])
            else:
                self.status.config(text=self.t['dev_inactivo'])

        chk = tk.Checkbutton(ventana, text=self.t['dev_label'], variable=var_dev, command=toggle, bg="#2c3e50", fg="white", selectcolor="#2c3e50")
        chk.pack(pady=15)

        tk.Label(ventana, text=self.t['by'], bg="#2c3e50", fg="#bdc3c7").pack(pady=5)

        btn_cerrar = tk.Button(ventana, text="OK", command=ventana.destroy, bg="#27ae60", fg="white", width=10)
        btn_cerrar.pack(pady=10)

    def seleccionar_archivo(self):
        tipos = [("Archivos soportados", "*.har *.txt")]
        if self.modo_dev:
            tipos = [("Todos", "*.*")]
        r = filedialog.askopenfilename(filetypes=tipos)
        if r:
            self.entry_file.delete(0, tk.END)
            self.entry_file.insert(0, r)

    def seleccionar_carpeta(self):
        r = filedialog.askdirectory()
        if r:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, r)

    def extraer(self):
        ruta = self.entry_file.get().strip()
        if not ruta or not os.path.exists(ruta):
            messagebox.showerror("", self.t['error_archivo'])
            return
        try:
            with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                data = f.read()
            m = self.patron_cookie.search(data)
            if not m:
                m = re.search(re.escape(self.prefijo) + r'([^\n]{100,800})', data)
            if m:
                var = m.group(1)
                self.cookie_original = self.prefijo + var
                var_clean = re.sub(r'[^A-Za-z0-9_\-\.]', '', var)
                self.cookie_limpia = self.prefijo + var_clean
                self.txt_orig.delete(1.0, tk.END)
                self.txt_orig.insert(tk.END, self.cookie_original)
                self.txt_clean.delete(1.0, tk.END)
                self.txt_clean.insert(tk.END, self.cookie_limpia)
                self.status.config(text=f"Extraída | Original:{len(self.cookie_original)} Limpia:{len(self.cookie_limpia)}")
            else:
                messagebox.showwarning("", self.t['error_cookie'])
        except Exception as e:
            messagebox.showerror("", str(e))

    def copiar_original(self):
        if self.cookie_original:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.cookie_original)
            self.status.config(text=self.t['copiada_orig'])
            self.popup(self.t['copiada_orig'])
        else:
            messagebox.showwarning("", self.t['sin_cookie'])

    def copiar_limpia(self):
        if self.cookie_limpia:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.cookie_limpia)
            self.status.config(text=self.t['copiada_clean'])
            self.popup(self.t['copiada_clean'])
        else:
            messagebox.showwarning("", self.t['sin_cookie'])

    def popup(self, msg):
        p = tk.Toplevel(self.root)
        p.geometry("180x35")
        p.overrideredirect(True)
        x = self.root.winfo_x() + self.root.winfo_width()//2 - 90
        y = self.root.winfo_y() + self.root.winfo_height()//2 - 20
        p.geometry(f"+{x}+{y}")
        tk.Label(p, text=msg, bg="#2c3e50", fg="white", font=("", 9)).pack(fill="both", expand=True)
        p.after(1200, p.destroy)

    def buscar(self):
        if not self.cookie_limpia:
            messagebox.showwarning("", self.t['sin_cookie'])
            return
        carpeta = self.entry_folder.get().strip()
        if not carpeta or not os.path.isdir(carpeta):
            messagebox.showerror("", self.t['error_carpeta'])
            return

        self.txt_resultados.delete(1.0, tk.END)
        self.txt_resultados.insert(tk.END, "🔍 Buscando...\n")
        self.status.config(text="Recopilando...")
        self.root.update()

        archivos = []
        for raiz, _, files in os.walk(carpeta):
            for f in files:
                if self.modo_dev:
                    archivos.append(os.path.join(raiz, f))
                elif f.lower().endswith(('.har', '.txt')):
                    archivos.append(os.path.join(raiz, f))

        if not archivos:
            self.txt_resultados.insert(tk.END, self.t['sin_archivos'])
            self.status.config(text=self.t['sin_archivos'])
            return

        total = len(archivos)
        self.progress["maximum"] = total
        self.progress["value"] = 0
        encontrados = []

        for i, r in enumerate(archivos):
            self.status.config(text=f"Procesando {i+1}/{total}")
            self.root.update()
            self.progress["value"] = i+1
            try:
                with open(r, 'r', encoding='utf-8', errors='ignore') as f:
                    if self.cookie_limpia in f.read():
                        encontrados.append(r)
            except:
                continue

        self.txt_resultados.delete(1.0, tk.END)
        if encontrados:
            msg = self.t['encontrada'].format(len(encontrados))
            self.txt_resultados.insert(tk.END, f"✅ {msg}\n\n")
            for r in encontrados:
                rel = os.path.relpath(r, carpeta)
                self.txt_resultados.insert(tk.END, f"📄 {rel}\n")
            self.status.config(text=msg)
            if messagebox.askyesno("", self.t['guardar']):
                guardar = filedialog.asksaveasfilename(defaultextension=".txt")
                if guardar:
                    with open(guardar, 'w') as f:
                        f.write("\n".join(encontrados))
                    messagebox.showinfo("", self.t['guardado'])
        else:
            self.txt_resultados.insert(tk.END, f"❌ {self.t['no_encontrada']}")
            self.status.config(text=self.t['no_encontrada'])

    def cambiar_idioma(self, event=None):
        self.idioma = self.idioma_var.get()
        self.t = TEXTO[self.idioma]
        self.root.title(self.t['titulo'])
        self.notebook.tab(0, text=self.t['tab1'])
        self.notebook.tab(1, text=self.t['tab2'])
        self.btn_extraer.config(text=self.t['extraer'])
        self.btn_buscar.config(text=self.t['buscar'])
        self.btn_copiar_orig.config(text=f"{self.t['copiar']} Original")
        self.btn_copiar_clean.config(text=f"{self.t['copiar']} Limpia")
        self.status.config(text=self.t['listo'])
        for child in self.tab1.winfo_children():
            if isinstance(child, tk.LabelFrame) and child.cget('text') in ["Archivo", "File", "Файл"]:
                child.config(text=self.t['archivo'])
        for child in self.tab2.winfo_children():
            if isinstance(child, tk.LabelFrame) and child.cget('text') in ["Carpeta", "Folder", "Папка"]:
                child.config(text=self.t['carpeta'])
        # Actualizar textos de los labels "Original" y "Limpia"
        for child in self.tab1.winfo_children():
            if isinstance(child, tk.Label) and child.cget('text') in ["Original", "Оригинал", "Clean", "Limpia", "Очищенная"]:
                if child.cget('text') == self.t['original'] or child.cget('text') == self.t['limpia']:
                    continue
                child.config(text=self.t['original'] if "Original" in str(child) else self.t['limpia'])

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieHunter(root)
    root.mainloop()
