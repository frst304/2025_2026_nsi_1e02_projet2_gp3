import tkinter as tk

from .styles import appliquer_styles


class MainWindow:

    def __init__(self):
        self.fenetre = tk.Tk()
        self.fenetre.title("Projet python")
        self.fenetre.geometry("1000x600")
        self.fenetre.configure(bg="#f4f6f8")

        appliquer_styles(self.fenetre)

        self._build_nav_bar()
        self.contenu = tk.Frame(self.fenetre, bg="#f4f6f8")
        self.contenu.pack(fill="both", expand=True)
        self.contenu.grid_rowconfigure(0, weight=1)
        self.contenu.grid_columnconfigure(0, weight=1)

    def _build_nav_bar(self):
        self.nav_bar = tk.Frame(self.fenetre, bg="#1f2a44")
        self.nav_bar.pack(fill="x")

    def add_nav_button(self, text, command, width=12):
        btn = tk.Button(
            self.nav_bar,
            text=text,
            command=command,
            width=width,
            bg="#1f2a44",
            fg="#ffffff",
            activebackground="#2b3a5c",
            activeforeground="#ffffff",
            relief="flat",
        )
        btn.pack(side="left", padx=5, pady=5)
        return btn

    def add_page(self, view):
        view.frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, view):
        view.frame.tkraise()

    def mainloop(self):
        self.fenetre.mainloop()
