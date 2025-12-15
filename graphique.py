import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def creer_figure_graphique():
    figure, axes = plt.subplots(figsize=(10, 5))
    return figure, axes


def configurer_axes_graphique(axes):
    axes.set_xlabel('Date')
    axes.set_ylabel('Nombre de personnes')
    axes.set_title('Évolution des indicateurs COVID-19 en France')
    axes.grid(True, alpha=0.3)
    axes.legend(loc='best')


def tracer_courbe_deces(axes, dates, valeurs_deces):
    axes.plot(dates, valeurs_deces, color='red', linewidth=1.5, label='Décès totaux')

def tracer_courbe_rea(axes, dates, valeurs_rea):
    axes.plot(dates, valeurs_rea, color='orange', linewidth=1.5, label='Réanimations')

def tracer_courbe_admission_hopital(axes, dates, valeurs_hosp):
    axes.plot(dates, valeurs_hosp, color='blue', linewidth=1.5, label='Hospitalisations')


def formater_affichage_dates():
    plt.xticks(rotation=45)
    plt.tight_layout()


def integrer_graphique_dans_fenetre_tkinter(fenetre, figure):
    canvas = FigureCanvasTkAgg(figure, fenetre)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return canvas


def afficher_graphique_dans_fenetre(fenetre, dataframe_prepare):
    figure, axes = creer_figure_graphique()
    
    dates = dataframe_prepare['date']
    
    if 'dc_tot' in dataframe_prepare.columns:
        tracer_courbe_deces(axes, dates, dataframe_prepare['dc_tot'])
    
    if 'hosp' in dataframe_prepare.columns:
        tracer_courbe_admission_hopital(axes, dates, dataframe_prepare['hosp'])
    
    if 'rea' in dataframe_prepare.columns:
        tracer_courbe_rea(axes, dates, dataframe_prepare['rea'])
    
    configurer_axes_graphique(axes)
    formater_affichage_dates()
    
    integrer_graphique_dans_fenetre_tkinter(fenetre, figure)

