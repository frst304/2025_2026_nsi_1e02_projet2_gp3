import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def creer_figure_graphique_deces():
    figure, axes = plt.subplots(figsize=(10, 5))
    return figure, axes


def configurer_axes_graphique_deces(axes):
    axes.set_xlabel('Date')
    axes.set_ylabel('Nombre de décès')
    axes.set_title('Évolution des décès COVID-19 en France')
    axes.grid(True, alpha=0.3)


def tracer_courbe_deces(axes, dates, valeurs_deces):
    axes.plot(dates, valeurs_deces, color='red', linewidth=1.5)


def formater_affichage_dates():
    plt.xticks(rotation=45)
    plt.tight_layout()


def integrer_graphique_dans_fenetre_tkinter(fenetre, figure):
    canvas = FigureCanvasTkAgg(figure, fenetre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas


def afficher_graphique_deces_dans_fenetre(fenetre, dataframe_prepare):
    figure, axes = creer_figure_graphique_deces()
    
    tracer_courbe_deces(axes, dataframe_prepare['date'], dataframe_prepare['dc_tot'])
    configurer_axes_graphique_deces(axes)
    formater_affichage_dates()
    
    integrer_graphique_dans_fenetre_tkinter(fenetre, figure)

