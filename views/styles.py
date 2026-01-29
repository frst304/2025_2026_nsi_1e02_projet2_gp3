import tkinter as tk
from tkinter import ttk


def appliquer_styles(fenetre):
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure(
        "TCombobox",
        padding=6,
    )
    style.configure(
        "Titre.TLabel",
        font=("Segoe UI", 18, "bold"),
        background="#f4f6f8",
        foreground="#1f2a44",
    )
    style.configure(
        "Texte.TLabel",
        font=("Segoe UI", 11),
        background="#f4f6f8",
        foreground="#2d3b55",
    )
    style.configure(
        "Stats.TLabel",
        font=("Segoe UI", 12, "bold"),
        background="#f4f6f8",
        foreground="#1f2a44",
    )
    style.configure(
        "Nav.TButton",
        font=("Segoe UI", 10, "bold"),
        padding=8,
    )
    style.configure(
        "Action.TButton",
        font=("Segoe UI", 11, "bold"),
        padding=8,
    )
