#%% Bibliothèque

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

#%% Fenêtre principale

def connect_db():
    return sqlite3.connect('C:/Users/teole/Documents/Aéro 4/Stage/Parc automobile/database.db', timeout=10)

def on_main_action_select():
    selected_action = main_action_var.get()
    if selected_action == "Ajouter un élément":
        add_frame.pack(pady=10)
        bilan_frame.pack_forget()
        consult_frame.pack_forget()
        modify_frame.pack_forget()
        verify_frame.pack_forget()
        export_frame.pack_forget()
    elif selected_action == "Faire un bilan financier":
        add_frame.pack_forget()
        bilan_frame.pack(pady=10)
        consult_frame.pack_forget()
        modify_frame.pack_forget()
        verify_frame.pack_forget()
        export_frame.pack_forget()
    elif selected_action == "Consulter des informations":
        add_frame.pack_forget()
        bilan_frame.pack_forget()
        consult_frame.pack(pady=10)
        modify_frame.pack_forget()
        verify_frame.pack_forget()
        export_frame.pack_forget()
    elif selected_action == "Modifier une information":
        add_frame.pack_forget()
        bilan_frame.pack_forget()
        consult_frame.pack_forget()
        modify_frame.pack(pady=10)
        verify_frame.pack_forget()
        export_frame.pack_forget()
    elif selected_action == "Informations importantes":
        add_frame.pack_forget()
        bilan_frame.pack_forget()
        consult_frame.pack_forget()
        modify_frame.pack_forget()
        verify_frame.pack(pady=10)
        export_frame.pack_forget()
    elif selected_action == "Exporter les données en Excel":
        add_frame.pack_forget()
        bilan_frame.pack_forget()
        consult_frame.pack_forget()
        modify_frame.pack_forget()
        verify_frame.pack_forget()
        export_frame.pack(pady=10)
    else:
        add_frame.pack_forget()
        bilan_frame.pack_forget()
        consult_frame.pack_forget()
        modify_frame.pack_forget()
        verify_frame.pack_forget()
        export_frame.pack_forget()

def on_add_action_select():
    selected_add_action = add_action_var.get()
    if selected_add_action == "Un véhicule":
        open_vehicle_form()
    elif selected_add_action == "Un plein":
        open_fuel_form()
    elif selected_add_action == "Un contrôle technique":
        open_ct_form()
    elif selected_add_action == "Une réparation":
        open_repair_form()
    elif selected_add_action == "Une révision":
        open_revision_form()

def on_bilan_action_select():
    bilan_action = bilan_action_var.get()
    if bilan_action == "Bilan mensuel d'un véhicule":
        ask_for_plate_and_date()
    elif bilan_action == "Bilan annuel d'un véhicule":
        ask_for_plate_and_year()
    elif bilan_action == "Bilan total d'un véhicule":
        ask_for_plate()
        
def on_consult_action_select():
    consult_action = consult_action_var.get()
    if consult_action == "Consulter les infos d'un véhicule":
        consult_vehicle_info()
    elif consult_action == "Consulter les pleins d'un véhicule":
        ask_for_plate_bis()
    elif consult_action == "Consulter les interventions d'un véhicule":
        ask_for_plate_ter()
        
def on_modify_action_select():
    modify_action = modify_action_var.get()
    if modify_action == "Modifier une informations sur un véhicule":
        ask_for_plate_and_modify()
    elif modify_action == "Supprimer une donnée":
        ask_for_deletion()
        
def on_verify_action_select():
    verify_action = verify_action_var.get()
    if verify_action == "Contrôle(s) technique(s) urgent(s)":
        afficher_controles_techniques()
    elif verify_action == "Voir le(s) révision(s) urgente(s)":
        afficher_revisions_prochaines()
    elif verify_action == "Voir les équipements manquants":
        afficher_equipements_manquants()
    elif verify_action == "Voir les remarques importantes":
        afficher_remarques()
        
def on_export_action_select():
    export_action = export_action_var.get()
    if export_action == "Exporter le tableau des voitures":
        exporter_tableau_voiture()
    elif export_action == "Exporter le tableau des réparations (12 derniers mois)":
        exporter_tableau_reparation()
    elif export_action == "Exporter le tableau des révisions (12 derniers mois)":
        exporter_tableau_revision()
    elif export_action == "Exporter le tableau des pleins (6 derniers mois)":
        exporter_tableau_plein()
    elif export_action == "Exporter le tableau des contrôles techniques (12 derniers mois)":
        exporter_tableau_ct()       

#%% Ajouter un véhicule

def calcul_révision(carburant, km):
    # Convertir km en entier si ce n'est pas déjà un entier
    try:
        km = int(km)
    except ValueError:
        raise ValueError("La valeur de 'km' doit être un entier ou une chaîne représentant un entier.")

    # Calcul de la prochaine révision en fonction du type de carburant
    carburantt = str(carburant)
    if carburantt == 'Gazole':
        for item in range(20000, 10000001, 20000):
            if item >= km:
                revision = item
                break
    elif carburantt in ['Essence', 'Essence-GPL', 'Hybride']:
        for item in range(15000, 10000001, 15000):
            if item >= km:
                revision = item
                break
    elif carburantt == 'Électrique':
        for item in range(30000, 10000001, 30000):
            if item >= km:
                revision = item
                break
    else:
        raise ValueError("Type de carburant inconnu.")

    return revision

def insert_vehicle(plaque, pole, marque_modele, en_service, nb_cles, carburant, date_mise_circulation, vignette, fin_assurance, equipement, km, remarques, contrat, utilisateur_associe):
    prochaine_revision = calcul_révision(carburant, km)
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO voiture (
                plaque_immatriculation, pôle, marque_modèle, en_service, nombre_de_clés, carburant, mise_en_circulation, vignette_crit_air, 
                fin_assurance, équipement, kilométrage, remarques, prochaine_revision, contrat, utilisateur
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            plaque, pole, marque_modele, en_service, nb_cles, carburant, date_mise_circulation, vignette, fin_assurance, 
            equipement, km , remarques, prochaine_revision, contrat, utilisateur_associe
        ))
        conn.commit()

def open_vehicle_form():
    vehicle_form_window = tk.Toplevel(root)
    vehicle_form_window.title("Ajouter un véhicule")
    
    font_style = ("Helvetica", 8)

    def submit_vehicle_info():
        plaque = plaque_entry.get()
        pole = pole_var.get()
        marque_modele = marque_modele_entry.get()
        en_service = en_service_var.get()
        nb_cles = nb_cles_var.get()
        carburant = carburant_var.get()

        # Date de mise en circulation
        date_mise_circulation = f"{year_mise_circulation_var.get()}-{month_mise_circulation_var.get()}-{day_mise_circulation_var.get()}"
        
        # Vignette Crit'Air
        vignette = vignette_var.get()
        
        # Fin de l'assurance (qui est aussi la date du prochain contrôle technique)
        fin_assurance = f"{year_fin_assurance_var.get()}-{month_fin_assurance_var.get()}-{day_fin_assurance_var.get()}"
        
        equipement = []
        if roue_var.get():
            equipement.append("Roue de secours")
        if gilet_var.get():
            equipement.append("Gilet jaune")
        if triangle_var.get():
            equipement.append("Triangle")
        equipement = ", ".join(equipement)

        km = km_entry.get()
        remarques = remarques_entry.get()
        contrat = type_vehicule_var.get()  # Récupérer le type de véhicule
        
        # Nom ou statut de l'utilisateur
        utilisateur_associe = utilisateur_entry.get()

        if plaque and marque_modele:
            insert_vehicle(plaque, pole, marque_modele, en_service, nb_cles, carburant, date_mise_circulation, vignette, fin_assurance, equipement, km, remarques, contrat, utilisateur_associe)
            messagebox.showinfo("Succès", "Véhicule ajouté avec succès.")
            vehicle_form_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs obligatoires.")

    labels_texts = [
        "Immatriculation (ex: AA-000-BB)", "Voiture (ex: Renault Clio)", "Kilométrage (ex:15000)"
    ]

    entries = []
    for label_text in labels_texts:
        frame = tk.Frame(vehicle_form_window)
        frame.pack(fill=tk.X, padx=5, pady=2)
        label = tk.Label(frame, text=label_text, width=25, anchor='w', font=font_style)
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, font=font_style)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        entries.append(entry)

    # Extraction des entrées
    plaque_entry, marque_modele_entry, km_entry = entries

    # Pôle
    pole_frame = tk.Frame(vehicle_form_window)
    pole_frame.pack(fill=tk.X, padx=5, pady=2)
    pole_label = tk.Label(pole_frame, text="Pôle", width=25, anchor='w', font=font_style)
    pole_label.pack(side=tk.LEFT)
    
    pole_var = tk.StringVar(value="Ado")
    pole_options = ttk.Combobox(pole_frame, textvariable=pole_var, values=["MDE-Ado", "MDE-Enfant", "MDE-SESSAD", "SESSAD", "SITEPP"], font=font_style)
    pole_options.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # En service
    en_service_frame = tk.Frame(vehicle_form_window)
    en_service_frame.pack(fill=tk.X, padx=5, pady=2)
    en_service_label = tk.Label(en_service_frame, text="En service", width=25, anchor='w', font=font_style)
    en_service_label.pack(side=tk.LEFT)
    
    en_service_var = tk.StringVar(value="Oui")
    yes_button = tk.Radiobutton(en_service_frame, text="Oui", variable=en_service_var, value="Oui", font=font_style)
    yes_button.pack(side=tk.LEFT, padx=10)
    no_button = tk.Radiobutton(en_service_frame, text="Non", variable=en_service_var, value="Non", font=font_style)
    no_button.pack(side=tk.LEFT, padx=10)

    # Nombre de clés
    nb_cles_frame = tk.Frame(vehicle_form_window)
    nb_cles_frame.pack(fill=tk.X, padx=5, pady=2)
    nb_cles_label = tk.Label(nb_cles_frame, text="Nombre de clés", width=25, anchor='w', font=font_style)
    nb_cles_label.pack(side=tk.LEFT)
    
    nb_cles_var = tk.StringVar(value="1")
    nb_cles_options = ttk.Combobox(nb_cles_frame, textvariable=nb_cles_var, values=["0", "1", "2", "3"], font=font_style)
    nb_cles_options.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Carburant
    carburant_frame = tk.Frame(vehicle_form_window)
    carburant_frame.pack(fill=tk.X, padx=5, pady=2)
    carburant_label = tk.Label(carburant_frame, text="Carburant", width=25, anchor='w', font=font_style)
    carburant_label.pack(side=tk.LEFT)
    
    carburant_var = tk.StringVar(value="Essence")
    carburant_options = ttk.Combobox(carburant_frame, textvariable=carburant_var, values=["Gazole", "Essence", "Électrique", "Hybride", "Essence-GPL"], font=font_style)
    carburant_options.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Date de mise en circulation
    mise_circulation_frame = tk.Frame(vehicle_form_window)
    mise_circulation_frame.pack(fill=tk.X, padx=5, pady=2)
    
    mise_circulation_label = tk.Label(mise_circulation_frame, text="Date de mise en circulation", width=25, anchor='w', font=font_style)
    mise_circulation_label.pack(side=tk.LEFT)
    
    # Calcul des années pour la mise en circulation
    current_year = datetime.now().year
    years = [str(year) for year in range(2000, current_year + 1)]
    months = [str(i) for i in range(1, 13)]
    days = [f"{day:02d}" for day in range(1, 32)]
    
    # Année
    year_mise_circulation_frame = tk.Frame(mise_circulation_frame)
    year_mise_circulation_frame.pack(side=tk.LEFT, padx=5)
    year_mise_circulation_label = tk.Label(year_mise_circulation_frame, text="Année", width=8, anchor='w', font=font_style)
    year_mise_circulation_label.pack(side=tk.LEFT)
    year_mise_circulation_var = tk.StringVar()
    year_mise_circulation_options = ttk.Combobox(year_mise_circulation_frame, textvariable=year_mise_circulation_var, values=years, font=font_style, width=5)
    year_mise_circulation_options.pack(side=tk.LEFT)
    
    # Mois
    month_mise_circulation_frame = tk.Frame(mise_circulation_frame)
    month_mise_circulation_frame.pack(side=tk.LEFT, padx=5)
    month_mise_circulation_label = tk.Label(month_mise_circulation_frame, text="Mois", width=8, anchor='w', font=font_style)
    month_mise_circulation_label.pack(side=tk.LEFT)
    month_mise_circulation_var = tk.StringVar()
    month_mise_circulation_options = ttk.Combobox(month_mise_circulation_frame, textvariable=month_mise_circulation_var, values=months, font=font_style, width=5)
    month_mise_circulation_options.pack(side=tk.LEFT)
    
    # Jour
    day_mise_circulation_frame = tk.Frame(mise_circulation_frame)
    day_mise_circulation_frame.pack(side=tk.LEFT, padx=5)
    day_mise_circulation_label = tk.Label(day_mise_circulation_frame, text="Jour", width=8, anchor='w', font=font_style)
    day_mise_circulation_label.pack(side=tk.LEFT)
    day_mise_circulation_var = tk.StringVar()
    day_mise_circulation_options = ttk.Combobox(day_mise_circulation_frame, textvariable=day_mise_circulation_var, values=days, font=font_style, width=5)
    day_mise_circulation_options.pack(side=tk.LEFT)

    # Fin de l'assurance
    fin_assurance_frame = tk.Frame(vehicle_form_window)
    fin_assurance_frame.pack(fill=tk.X, padx=5, pady=2)
    
    fin_assurance_label = tk.Label(fin_assurance_frame, text="Prochain contrôle technique", width=25, anchor='w', font=font_style)
    fin_assurance_label.pack(side=tk.LEFT)
    
    # Calcul des années pour le contrôle technique
    current_year = datetime.now().year
    years_tech = [str(year) for year in range(current_year, current_year + 11)]
    
    # Année
    year_fin_assurance_frame = tk.Frame(fin_assurance_frame)
    year_fin_assurance_frame.pack(side=tk.LEFT, padx=5)
    year_fin_assurance_label = tk.Label(year_fin_assurance_frame, text="Année", width=8, anchor='w', font=font_style)
    year_fin_assurance_label.pack(side=tk.LEFT)
    year_fin_assurance_var = tk.StringVar()
    year_fin_assurance_options = ttk.Combobox(year_fin_assurance_frame, textvariable=year_fin_assurance_var, values=years_tech, font=font_style, width=5)
    year_fin_assurance_options.pack(side=tk.LEFT)
    
    # Mois
    month_fin_assurance_frame = tk.Frame(fin_assurance_frame)
    month_fin_assurance_frame.pack(side=tk.LEFT, padx=5)
    month_fin_assurance_label = tk.Label(month_fin_assurance_frame, text="Mois", width=8, anchor='w', font=font_style)
    month_fin_assurance_label.pack(side=tk.LEFT)
    month_fin_assurance_var = tk.StringVar()
    month_fin_assurance_options = ttk.Combobox(month_fin_assurance_frame, textvariable=month_fin_assurance_var, values=months, font=font_style, width=5)
    month_fin_assurance_options.pack(side=tk.LEFT)
    
    # Jour
    day_fin_assurance_frame = tk.Frame(fin_assurance_frame)
    day_fin_assurance_frame.pack(side=tk.LEFT, padx=5)
    day_fin_assurance_label = tk.Label(day_fin_assurance_frame, text="Jour", width=8, anchor='w', font=font_style)
    day_fin_assurance_label.pack(side=tk.LEFT)
    day_fin_assurance_var = tk.StringVar()
    day_fin_assurance_options = ttk.Combobox(day_fin_assurance_frame, textvariable=day_fin_assurance_var, values=days, font=font_style, width=5)
    day_fin_assurance_options.pack(side=tk.LEFT)

    # Vignette
    vignette_frame = tk.Frame(vehicle_form_window)
    vignette_frame.pack(fill=tk.X, padx=5, pady=2)
    vignette_label = tk.Label(vignette_frame, text="Vignette Crit'Air", width=25, anchor='w', font=font_style)
    vignette_label.pack(side=tk.LEFT)
    
    vignette_var = tk.StringVar(value="0")
    vignette_options = ttk.Combobox(vignette_frame, textvariable=vignette_var, values=["0", "1", "2", "3", "4", "5"], font=font_style)
    vignette_options.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Équipement
    equipement_frame = tk.Frame(vehicle_form_window)
    equipement_frame.pack(fill=tk.X, padx=5, pady=2)
    equipement_label = tk.Label(equipement_frame, text="Équipement", width=25, anchor='w', font=font_style)
    equipement_label.pack(side=tk.LEFT)
    
    roue_var = tk.BooleanVar()
    roue_check = tk.Checkbutton(equipement_frame, text="Roue de secours", variable=roue_var, font=font_style)
    roue_check.pack(side=tk.LEFT, padx=5)
    
    gilet_var = tk.BooleanVar()
    gilet_check = tk.Checkbutton(equipement_frame, text="Gilet jaune", variable=gilet_var, font=font_style)
    gilet_check.pack(side=tk.LEFT, padx=5)
    
    triangle_var = tk.BooleanVar()
    triangle_check = tk.Checkbutton(equipement_frame, text="Triangle", variable=triangle_var, font=font_style)
    triangle_check.pack(side=tk.LEFT, padx=5)

    # Remarques
    remarques_frame = tk.Frame(vehicle_form_window)
    remarques_frame.pack(fill=tk.X, padx=5, pady=2)
    remarques_label = tk.Label(remarques_frame, text="Remarques (si rien, tapez RAS)", width=25, anchor='w', font=font_style)
    remarques_label.pack(side=tk.LEFT)
    remarques_entry = tk.Entry(remarques_frame, font=font_style)
    remarques_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Type de véhicule
    type_vehicule_frame = tk.Frame(vehicle_form_window)
    type_vehicule_frame.pack(fill=tk.X, padx=5, pady=2)
    type_vehicule_label = tk.Label(type_vehicule_frame, text="Contrat", width=25, anchor='w', font=font_style)
    type_vehicule_label.pack(side=tk.LEFT)
    
    type_vehicule_var = tk.StringVar(value="Achat")
    achat_button = tk.Radiobutton(type_vehicule_frame, text="Achat", variable=type_vehicule_var, value="Achat", font=font_style)
    achat_button.pack(side=tk.LEFT, padx=10)
    location_button = tk.Radiobutton(type_vehicule_frame, text="Location", variable=type_vehicule_var, value="Location", font=font_style)
    location_button.pack(side=tk.LEFT, padx=10)

    # Utilisateur associé
    utilisateur_frame = tk.Frame(vehicle_form_window)
    utilisateur_frame.pack(fill=tk.X, padx=5, pady=2)
    
    utilisateur_label = tk.Label(utilisateur_frame, text="Utilisateur associé", width=25, anchor='w', font=font_style)
    utilisateur_label.pack(side=tk.LEFT)
    
    utilisateur_entry = tk.Entry(utilisateur_frame, font=font_style)
    utilisateur_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    submit_button = tk.Button(vehicle_form_window, text="Soumettre", command=submit_vehicle_info, font=font_style)
    submit_button.pack(pady=10)
    
#%% Ajouter un plein

def insert_fuel(numero_facture, date_plein, nombre_litres, prix, plaque):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO plein (numéro_facture, date_du_plein, litre, prix, plaque_immatriculation)
            VALUES (?, ?, ?, ?, ?)
        ''', (numero_facture, date_plein, nombre_litres, prix, plaque))
        conn.commit()

def open_fuel_form():
    fuel_form_window = tk.Toplevel(root)
    fuel_form_window.title("Ajouter un plein de carburant")

    font_style = ("Helvetica", 8)

    # Options pour les menus déroulants
    jours = [str(i).zfill(2) for i in range(1, 32)]  # Jours de 01 à 31
    mois = [str(i).zfill(2) for i in range(1, 13)]  # Mois de 01 à 12
    annees = [str(i) for i in range(2000, 2031)]  # Années de 2000 à 2030

    # Fonction de soumission
    def submit_fuel_info():
        numero_facture = numero_facture_entry.get()
        annee_plein = annee_var.get()
        mois_plein = mois_var.get()
        jour_plein = jour_var.get()
        date_plein = f"{annee_plein}-{mois_plein}-{jour_plein}"
        nombre_litres = nombre_litres_entry.get()
        prix = prix_entry.get()
        plaque = plaque_var.get()

        if numero_facture and annee_plein and mois_plein and jour_plein and nombre_litres and prix and plaque:
            insert_fuel(numero_facture, date_plein, nombre_litres, prix, plaque)
            messagebox.showinfo("Succès", "Plein de carburant ajouté avec succès.")
            fuel_form_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs obligatoires.")

    # Numéro de facture
    numero_facture_frame = tk.Frame(fuel_form_window)
    numero_facture_frame.pack(fill=tk.X, padx=5, pady=2)
    numero_facture_label = tk.Label(numero_facture_frame, text="Numéro de facture", width=25, anchor='w', font=font_style)
    numero_facture_label.pack(side=tk.LEFT)
    numero_facture_entry = tk.Entry(numero_facture_frame, font=font_style)
    numero_facture_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Date du plein
    date_plein_frame = tk.Frame(fuel_form_window)
    date_plein_frame.pack(fill=tk.X, padx=5, pady=2)
    date_plein_label = tk.Label(date_plein_frame, text="Date du plein", width=25, anchor='w', font=font_style)
    date_plein_label.pack(side=tk.LEFT)
    
    annee_var = tk.StringVar(value=annees[0])
    mois_var = tk.StringVar(value=mois[0])
    jour_var = tk.StringVar(value=jours[0])

    annee_menu = tk.OptionMenu(date_plein_frame, annee_var, *annees)
    annee_menu.pack(side=tk.LEFT, padx=2)

    mois_menu = tk.OptionMenu(date_plein_frame, mois_var, *mois)
    mois_menu.pack(side=tk.LEFT, padx=2)

    jour_menu = tk.OptionMenu(date_plein_frame, jour_var, *jours)
    jour_menu.pack(side=tk.LEFT, padx=2)

    # Nombre de litres
    nombre_litres_frame = tk.Frame(fuel_form_window)
    nombre_litres_frame.pack(fill=tk.X, padx=5, pady=2)
    nombre_litres_label = tk.Label(nombre_litres_frame, text="Nombre de litres (ex: 34)", width=25, anchor='w', font=font_style)
    nombre_litres_label.pack(side=tk.LEFT)
    nombre_litres_entry = tk.Entry(nombre_litres_frame, font=font_style)
    nombre_litres_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Prix
    prix_frame = tk.Frame(fuel_form_window)
    prix_frame.pack(fill=tk.X, padx=5, pady=2)
    prix_label = tk.Label(prix_frame, text="Prix en euros (ex: 67.86)", width=25, anchor='w', font=font_style)
    prix_label.pack(side=tk.LEFT)
    prix_entry = tk.Entry(prix_frame, font=font_style)
    prix_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Plaque de la voiture
    plaque_frame = tk.Frame(fuel_form_window)
    plaque_frame.pack(fill=tk.X, padx=5, pady=2)
    plaque_label = tk.Label(plaque_frame, text="Immatriculation", width=25, anchor='w', font=font_style)
    plaque_label.pack(side=tk.LEFT)
    
    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]
    plaque_var = tk.StringVar(value=plaques[0] if plaques else "")

    plaque_combobox = ttk.Combobox(plaque_frame, textvariable=plaque_var, values=plaques, font=font_style)
    plaque_combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        fuel_form_window.destroy()
        return

    submit_button = tk.Button(fuel_form_window, text="Soumettre", command=submit_fuel_info, font=font_style)
    submit_button.pack(pady=10)


#%% Ajouter un contrôle technique

def insert_technical_check(numero_facture, plaque, date_ct, garage, prix, remarques, prochaine_fin_assurance):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contrôle_technique (numéro_facture, plaque_immatriculation, date_du_contrôle_technique, garage, prix, remarques)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero_facture, plaque, date_ct, garage, prix, remarques))
        conn.commit()

        # Mettre à jour la date de fin d'assurance (prochain contrôle technique) du véhicule
        cursor.execute('''
            UPDATE voiture
            SET fin_assurance = ?
            WHERE plaque_immatriculation = ?
        ''', (prochaine_fin_assurance, plaque))
        conn.commit()

def open_ct_form():
    technical_check_form_window = tk.Toplevel(root)
    technical_check_form_window.title("Ajouter un contrôle technique")

    font_style = ("Helvetica", 8)

    # Options pour les menus déroulants
    jours = [str(i).zfill(2) for i in range(1, 32)]  # Jours de 01 à 31
    mois = [str(i).zfill(2) for i in range(1, 13)]  # Mois de 01 à 12
    annees = [str(i) for i in range(2000, 2031)]    # Années de 2000 à 2030

    # Fonction de soumission
    def submit_technical_check_info():
        numero_facture = numero_facture_entry.get()
        plaque = plaque_var.get()
        annee_ct = annee_var.get()
        mois_ct = mois_var.get()
        jour_ct = jour_var.get()
        date_ct = f"{annee_ct}-{mois_ct}-{jour_ct}"
        garage = garage_entry.get()
        prix = prix_entry.get()
        remarques = remarque_var.get()  # Remarques récupérées depuis les boutons radio
        annee_fin_assurance = annee_fin_assurance_var.get()
        mois_fin_assurance = mois_fin_assurance_var.get()
        jour_fin_assurance = jour_fin_assurance_var.get()
        prochaine_fin_assurance = f"{annee_fin_assurance}-{mois_fin_assurance}-{jour_fin_assurance}"
        if numero_facture and plaque and annee_ct and mois_ct and jour_ct and garage and prix and annee_fin_assurance and mois_fin_assurance and jour_fin_assurance:
            insert_technical_check(numero_facture, plaque, date_ct, garage, prix, remarques, prochaine_fin_assurance)
            messagebox.showinfo("Succès", "Contrôle technique ajouté avec succès.")
            technical_check_form_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs obligatoires.")

    # Numéro de facture
    numero_facture_frame = tk.Frame(technical_check_form_window)
    numero_facture_frame.pack(fill=tk.X, padx=5, pady=2)
    numero_facture_label = tk.Label(numero_facture_frame, text="Numéro du PV", width=25, anchor='w', font=font_style)
    numero_facture_label.pack(side=tk.LEFT)
    numero_facture_entry = tk.Entry(numero_facture_frame, font=font_style)
    numero_facture_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Plaque d'immatriculation (remplacé par une Combobox)
    plaque_frame = tk.Frame(technical_check_form_window)
    plaque_frame.pack(fill=tk.X, padx=5, pady=2)
    plaque_label = tk.Label(plaque_frame, text="Immatriculation", width=25, anchor='w', font=font_style)
    plaque_label.pack(side=tk.LEFT)
    
    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]
    plaque_var = tk.StringVar(value=plaques[0] if plaques else "")

    plaque_combobox = ttk.Combobox(plaque_frame, textvariable=plaque_var, values=plaques, font=font_style)
    plaque_combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        technical_check_form_window.destroy()
        return

    # Date du contrôle technique
    date_ct_frame = tk.Frame(technical_check_form_window)
    date_ct_frame.pack(fill=tk.X, padx=5, pady=2)
    date_ct_label = tk.Label(date_ct_frame, text="Date du contrôle technique", width=25, anchor='w', font=font_style)
    date_ct_label.pack(side=tk.LEFT)
    
    annee_var = tk.StringVar(value=annees[0])
    mois_var = tk.StringVar(value=mois[0])
    jour_var = tk.StringVar(value=jours[0])

    annee_menu = tk.OptionMenu(date_ct_frame, annee_var, *annees)
    annee_menu.pack(side=tk.LEFT, padx=2)

    mois_menu = tk.OptionMenu(date_ct_frame, mois_var, *mois)
    mois_menu.pack(side=tk.LEFT, padx=2)

    jour_menu = tk.OptionMenu(date_ct_frame, jour_var, *jours)
    jour_menu.pack(side=tk.LEFT, padx=2)

    # Garage
    garage_frame = tk.Frame(technical_check_form_window)
    garage_frame.pack(fill=tk.X, padx=5, pady=2)
    garage_label = tk.Label(garage_frame, text="Garage", width=25, anchor='w', font=font_style)
    garage_label.pack(side=tk.LEFT)
    garage_entry = tk.Entry(garage_frame, font=font_style)
    garage_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Prix
    prix_frame = tk.Frame(technical_check_form_window)
    prix_frame.pack(fill=tk.X, padx=5, pady=2)
    prix_label = tk.Label(prix_frame, text="Prix en euros (ex: 45.98)", width=25, anchor='w', font=font_style)
    prix_label.pack(side=tk.LEFT)
    prix_entry = tk.Entry(prix_frame, font=font_style)
    prix_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Remarques (Remplacé par deux boutons radio)
    remarques_frame = tk.Frame(technical_check_form_window)
    remarques_frame.pack(fill=tk.X, padx=5, pady=2)
    remarques_label = tk.Label(remarques_frame, text="Remarques", width=25, anchor='w', font=font_style)
    remarques_label.pack(side=tk.LEFT)

    remarque_var = tk.StringVar(value="Favorable")  # Valeur par défaut

    favorable_rb = tk.Radiobutton(remarques_frame, text="Favorable", variable=remarque_var, value="Favorable", font=font_style)
    favorable_rb.pack(side=tk.LEFT, padx=5)

    non_favorable_rb = tk.Radiobutton(remarques_frame, text="Non favorable", variable=remarque_var, value="Non-favorable", font=font_style)
    non_favorable_rb.pack(side=tk.LEFT, padx=5)

    # Date de fin d'assurance (prochain contrôle technique)
    date_fin_assurance_frame = tk.Frame(technical_check_form_window)
    date_fin_assurance_frame.pack(fill=tk.X, padx=5, pady=2)
    date_fin_assurance_label = tk.Label(date_fin_assurance_frame, text="Prochaine date de fin d'assurance", width=25, anchor='w', font=font_style)
    date_fin_assurance_label.pack(side=tk.LEFT)
    
    annee_fin_assurance_var = tk.StringVar(value=annees[0])
    mois_fin_assurance_var = tk.StringVar(value=mois[0])
    jour_fin_assurance_var = tk.StringVar(value=jours[0])

    annee_fin_assurance_menu = tk.OptionMenu(date_fin_assurance_frame, annee_fin_assurance_var, *annees)
    annee_fin_assurance_menu.pack(side=tk.LEFT, padx=2)

    mois_fin_assurance_menu = tk.OptionMenu(date_fin_assurance_frame, mois_fin_assurance_var, *mois)
    mois_fin_assurance_menu.pack(side=tk.LEFT, padx=2)

    jour_fin_assurance_menu = tk.OptionMenu(date_fin_assurance_frame, jour_fin_assurance_var, *jours)
    jour_fin_assurance_menu.pack(side=tk.LEFT, padx=2)

    # Bouton de soumission
    submit_button = tk.Button(technical_check_form_window, text="Soumettre", command=submit_technical_check_info, font=font_style)
    submit_button.pack(pady=10)

    
#%% Ajouter une réparation

def insert_repair(numero_facture, plaque, libelle, date_repair, garage, prix):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO réparation (numéro_facture, plaque_immatriculation, libellé, date_de_la_réparation, garage, prix)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (numero_facture, plaque, libelle, date_repair, garage, prix))
        conn.commit()

def open_repair_form():
    repair_form_window = tk.Toplevel(root)
    repair_form_window.title("Ajouter une réparation")

    font_style = ("Helvetica", 8)

    # Options pour les menus déroulants
    jours = [str(i).zfill(2) for i in range(1, 32)]  # Jours de 01 à 31
    mois = [str(i).zfill(2) for i in range(1, 13)]  # Mois de 01 à 12
    annees = [str(i) for i in range(2000, 2031)]    # Années de 2020 à 2030

    # Fonction de soumission
    def submit_repair_info():
        numero_facture = numero_facture_entry.get()
        plaque = plaque_var.get()
        libelle = libelle_entry.get()
        annee_repair = annee_var.get()
        mois_repair = mois_var.get()
        jour_repair = jour_var.get()
        date_repair = f"{annee_repair}-{mois_repair}-{jour_repair}"
        garage = garage_entry.get()
        prix = prix_entry.get()

        if numero_facture and plaque and libelle and annee_repair and mois_repair and jour_repair and garage and prix:
            insert_repair(numero_facture, plaque, libelle, date_repair, garage, prix)
            messagebox.showinfo("Succès", "Réparation ajoutée avec succès.")
            repair_form_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs obligatoires.")

    # Numéro de facture
    numero_facture_frame = tk.Frame(repair_form_window)
    numero_facture_frame.pack(fill=tk.X, padx=5, pady=2)
    numero_facture_label = tk.Label(numero_facture_frame, text="Numéro de facture", width=25, anchor='w', font=font_style)
    numero_facture_label.pack(side=tk.LEFT)
    numero_facture_entry = tk.Entry(numero_facture_frame, font=font_style)
    numero_facture_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Plaque d'immatriculation (remplacé par une Combobox)
    plaque_frame = tk.Frame(repair_form_window)
    plaque_frame.pack(fill=tk.X, padx=5, pady=2)
    plaque_label = tk.Label(plaque_frame, text="Immatriculation", width=25, anchor='w', font=font_style)
    plaque_label.pack(side=tk.LEFT)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]
    plaque_var = tk.StringVar(value=plaques[0] if plaques else "")

    plaque_combobox = ttk.Combobox(plaque_frame, textvariable=plaque_var, values=plaques, font=font_style)
    plaque_combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        repair_form_window.destroy()
        return

    # Libellé
    libelle_frame = tk.Frame(repair_form_window)
    libelle_frame.pack(fill=tk.X, padx=5, pady=2)
    libelle_label = tk.Label(libelle_frame, text="Libellé", width=25, anchor='w', font=font_style)
    libelle_label.pack(side=tk.LEFT)
    libelle_entry = tk.Entry(libelle_frame, font=font_style)
    libelle_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Date de la réparation
    date_repair_frame = tk.Frame(repair_form_window)
    date_repair_frame.pack(fill=tk.X, padx=5, pady=2)
    date_repair_label = tk.Label(date_repair_frame, text="Date", width=25, anchor='w', font=font_style)
    date_repair_label.pack(side=tk.LEFT)

    annee_var = tk.StringVar(value=annees[0])
    mois_var = tk.StringVar(value=mois[0])
    jour_var = tk.StringVar(value=jours[0])

    annee_menu = tk.OptionMenu(date_repair_frame, annee_var, *annees)
    annee_menu.pack(side=tk.LEFT, padx=2)

    mois_menu = tk.OptionMenu(date_repair_frame, mois_var, *mois)
    mois_menu.pack(side=tk.LEFT, padx=2)

    jour_menu = tk.OptionMenu(date_repair_frame, jour_var, *jours)
    jour_menu.pack(side=tk.LEFT, padx=2)

    # Garage
    garage_frame = tk.Frame(repair_form_window)
    garage_frame.pack(fill=tk.X, padx=5, pady=2)
    garage_label = tk.Label(garage_frame, text="Garage", width=25, anchor='w', font=font_style)
    garage_label.pack(side=tk.LEFT)
    garage_entry = tk.Entry(garage_frame, font=font_style)
    garage_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Prix
    prix_frame = tk.Frame(repair_form_window)
    prix_frame.pack(fill=tk.X, padx=5, pady=2)
    prix_label = tk.Label(prix_frame, text="Prix en euros (ex: 45.32)", width=25, anchor='w', font=font_style)
    prix_label.pack(side=tk.LEFT)
    prix_entry = tk.Entry(prix_frame, font=font_style)
    prix_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    submit_button = tk.Button(repair_form_window, text="Soumettre", command=submit_repair_info, font=font_style)
    submit_button.pack(pady=10)

#%% Ajouter une révision

def insert_revision(numero_facture, plaque, libelle, date_revision, garage, prix, remarques):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO révision (numéro_facture, plaque_immatriculation, révision_kilometre, date_de_la_révision, garage, prix, remarques)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (numero_facture, plaque, libelle, date_revision, garage, prix, remarques))
        conn.commit()

def open_revision_form():
    revision_form_window = tk.Toplevel(root)
    revision_form_window.title("Ajouter une révision")

    font_style = ("Helvetica", 8)

    # Options pour les menus déroulants
    jours = [str(i).zfill(2) for i in range(1, 32)]  # Jours de 01 à 31
    mois = [str(i).zfill(2) for i in range(1, 13)]  # Mois de 01 à 12
    annees = [str(i) for i in range(2000, 2031)]    # Années de 2000 à 2030

    # Fonction de soumission
    def submit_revision_info():
        numero_facture = numero_facture_entry.get()
        plaque = plaque_var.get()
        libelle = libelle_entry.get()
        annee_revision = annee_var.get()
        mois_revision = mois_var.get()
        jour_revision = jour_var.get()
        date_revision = f"{annee_revision}-{mois_revision}-{jour_revision}"
        garage = garage_entry.get()
        prix = prix_entry.get()
        remarques = remarques_entry.get()

        if numero_facture and plaque and libelle and annee_revision and mois_revision and jour_revision and garage and prix:
            insert_revision(numero_facture, plaque, libelle, date_revision, garage, prix, remarques)
            messagebox.showinfo("Succès", "Révision ajoutée avec succès.")
            revision_form_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez remplir tous les champs obligatoires.")

    # Numéro de facture
    numero_facture_frame = tk.Frame(revision_form_window)
    numero_facture_frame.pack(fill=tk.X, padx=5, pady=2)
    numero_facture_label = tk.Label(numero_facture_frame, text="Numéro de facture", width=25, anchor='w', font=font_style)
    numero_facture_label.pack(side=tk.LEFT)
    numero_facture_entry = tk.Entry(numero_facture_frame, font=font_style)
    numero_facture_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Plaque d'immatriculation (remplacé par une Combobox)
    plaque_frame = tk.Frame(revision_form_window)
    plaque_frame.pack(fill=tk.X, padx=5, pady=2)
    plaque_label = tk.Label(plaque_frame, text="Immatriculation", width=25, anchor='w', font=font_style)
    plaque_label.pack(side=tk.LEFT)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]
    plaque_var = tk.StringVar(value=plaques[0] if plaques else "")

    plaque_combobox = ttk.Combobox(plaque_frame, textvariable=plaque_var, values=plaques, font=font_style)
    plaque_combobox.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        revision_form_window.destroy()
        return

    # Libellé de révision
    libelle_frame = tk.Frame(revision_form_window)
    libelle_frame.pack(fill=tk.X, padx=5, pady=2)
    libelle_label = tk.Label(libelle_frame, text="Libellé de révision", width=25, anchor='w', font=font_style)
    libelle_label.pack(side=tk.LEFT)
    libelle_entry = tk.Entry(libelle_frame, font=font_style)
    libelle_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Date de révision
    date_revision_frame = tk.Frame(revision_form_window)
    date_revision_frame.pack(fill=tk.X, padx=5, pady=2)
    date_revision_label = tk.Label(date_revision_frame, text="Date de révision", width=25, anchor='w', font=font_style)
    date_revision_label.pack(side=tk.LEFT)

    annee_var = tk.StringVar(value=annees[0])
    mois_var = tk.StringVar(value=mois[0])
    jour_var = tk.StringVar(value=jours[0])

    annee_menu = tk.OptionMenu(date_revision_frame, annee_var, *annees)
    annee_menu.pack(side=tk.LEFT, padx=2)

    mois_menu = tk.OptionMenu(date_revision_frame, mois_var, *mois)
    mois_menu.pack(side=tk.LEFT, padx=2)

    jour_menu = tk.OptionMenu(date_revision_frame, jour_var, *jours)
    jour_menu.pack(side=tk.LEFT, padx=2)

    # Garage
    garage_frame = tk.Frame(revision_form_window)
    garage_frame.pack(fill=tk.X, padx=5, pady=2)
    garage_label = tk.Label(garage_frame, text="Garage", width=25, anchor='w', font=font_style)
    garage_label.pack(side=tk.LEFT)
    garage_entry = tk.Entry(garage_frame, font=font_style)
    garage_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Prix
    prix_frame = tk.Frame(revision_form_window)
    prix_frame.pack(fill=tk.X, padx=5, pady=2)
    prix_label = tk.Label(prix_frame, text="Prix en euros (ex: 45.78)", width=25, anchor='w', font=font_style)
    prix_label.pack(side=tk.LEFT)
    prix_entry = tk.Entry(prix_frame, font=font_style)
    prix_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    # Remarques
    remarques_frame = tk.Frame(revision_form_window)
    remarques_frame.pack(fill=tk.X, padx=5, pady=2)
    remarques_label = tk.Label(remarques_frame, text="Remarques", width=25, anchor='w', font=font_style)
    remarques_label.pack(side=tk.LEFT)
    remarques_entry = tk.Entry(remarques_frame, font=font_style)
    remarques_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

    submit_button = tk.Button(revision_form_window, text="Soumettre", command=submit_revision_info, font=font_style)
    submit_button.pack(pady=10)

    
#%% Demande de bilan financier mensuel

def calculate_monthly_financial_report(plaque, month, year):
    costs = {
        "plein": 0,
        "révision": 0,
        "réparation": 0,
        "contrôle_technique": 0
    }

    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Calculer le coût des pleins
        cursor.execute('SELECT SUM(prix) FROM plein WHERE plaque_immatriculation = ? AND strftime("%Y-%m", date_du_plein) = ?', (plaque, f"{year}-{month:02d}"))
        plein_cost = cursor.fetchone()[0]
        if plein_cost:
            costs["plein"] = plein_cost
        
        # Calculer le coût des révisions
        cursor.execute('SELECT SUM(prix) FROM révision WHERE plaque_immatriculation = ? AND strftime("%Y-%m", date_de_la_révision) = ?', (plaque, f"{year}-{month:02d}"))
        revision_cost = cursor.fetchone()[0]
        if revision_cost:
            costs["révision"] = revision_cost
        
        # Calculer le coût des réparations
        cursor.execute('SELECT SUM(prix) FROM réparation WHERE plaque_immatriculation = ? AND strftime("%Y-%m", date_de_la_réparation) = ?', (plaque, f"{year}-{month:02d}"))
        reparation_cost = cursor.fetchone()[0]
        if reparation_cost:
            costs["réparation"] = reparation_cost
        
        # Calculer le coût des contrôles techniques
        cursor.execute('SELECT SUM(prix) FROM contrôle_technique WHERE plaque_immatriculation = ? AND strftime("%Y-%m", date_du_contrôle_technique) = ?', (plaque, f"{year}-{month:02d}"))
        controle_technique_cost = cursor.fetchone()[0]
        if controle_technique_cost:
            costs["contrôle_technique"] = controle_technique_cost
    
    return costs

def ask_for_plate_and_date():
    def submit_plate_month_year():
        plate = plate_var.get()
        month = month_var.get()
        year = year_var.get()
        if plate and month and year:
            costs = calculate_monthly_financial_report(plate, int(month), int(year))
            total_cost = sum(costs.values())
            messagebox.showinfo("Bilan Financier Mensuel", 
                                    f"Le coût mensuel pour le véhicule avec la plaque {plate} en {month}/{year} est de {total_cost} euros.\n\n"
                                    f"Détails :\n"
                                    f" - Pleins : {costs['plein']} euros\n"
                                    f" - Révisions : {costs['révision']} euros\n"
                                    f" - Réparations : {costs['réparation']} euros\n"
                                    f" - Contrôles Techniques : {costs['contrôle_technique']} euros")
            plate_month_year_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une plaque d'immatriculation, un mois et une année.")

    plate_month_year_window = tk.Toplevel(root)
    plate_month_year_window.title("Entrer la plaque d'immatriculation, le mois et l'année")

    font_style = ("Helvetica", 10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]

    # Plaque d'immatriculation
    plate_label = tk.Label(plate_month_year_window, text="Plaque d'immatriculation", font=font_style)
    plate_label.pack(pady=10)
    
    plate_var = tk.StringVar()
    plate_var.set(plaques[0] if plaques else "")

    plate_combobox = ttk.Combobox(plate_month_year_window, textvariable=plate_var, values=plaques, font=font_style)
    plate_combobox.pack(pady=5)
    
    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_month_year_window.destroy()
        return

    # Mois
    month_label = tk.Label(plate_month_year_window, text="Mois", font=font_style)
    month_label.pack(pady=10)
    
    months = [str(i).zfill(2) for i in range(1, 13)]
    month_var = tk.StringVar(plate_month_year_window)
    month_var.set(months[0])  # Valeur par défaut
    
    month_menu = tk.OptionMenu(plate_month_year_window, month_var, *months)
    month_menu.pack(pady=5)
    
    # Année
    year_label = tk.Label(plate_month_year_window, text="Année", font=font_style)
    year_label.pack(pady=10)
    
    years = list(range(2020, 2031))
    year_var = tk.StringVar(plate_month_year_window)
    year_var.set(years[0])  # Valeur par défaut
    
    year_menu = tk.OptionMenu(plate_month_year_window, year_var, *years)
    year_menu.pack(pady=5)
    
    submit_button = tk.Button(plate_month_year_window, text="Soumettre", command=submit_plate_month_year, font=font_style)
    submit_button.pack(pady=10)


#%% Demande de bilan financier annuel

def calculate_annual_financial_report(plaque, year):
    costs = {
        "plein": 0,
        "révision": 0,
        "réparation": 0,
        "contrôle_technique": 0
    }

    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Calculer le coût des pleins
        cursor.execute('SELECT SUM(prix) FROM plein WHERE plaque_immatriculation = ? AND strftime("%Y", date_du_plein) = ?', (plaque, f"{year}"))
        plein_cost = cursor.fetchone()[0]
        if plein_cost:
            costs["plein"] = plein_cost
        
        # Calculer le coût des révisions
        cursor.execute('SELECT SUM(prix) FROM révision WHERE plaque_immatriculation = ? AND strftime("%Y", date_de_la_révision) = ?', (plaque, f"{year}"))
        revision_cost = cursor.fetchone()[0]
        if revision_cost:
            costs["révision"] = revision_cost
        
        # Calculer le coût des réparations
        cursor.execute('SELECT SUM(prix) FROM réparation WHERE plaque_immatriculation = ? AND strftime("%Y", date_de_la_réparation) = ?', (plaque, f"{year}"))
        reparation_cost = cursor.fetchone()[0]
        if reparation_cost:
            costs["réparation"] = reparation_cost
        
        # Calculer le coût des contrôles techniques
        cursor.execute('SELECT SUM(prix) FROM contrôle_technique WHERE plaque_immatriculation = ? AND strftime("%Y", date_du_contrôle_technique) = ?', (plaque, f"{year}"))
        controle_technique_cost = cursor.fetchone()[0]
        if controle_technique_cost:
            costs["contrôle_technique"] = controle_technique_cost
    
    return costs

def ask_for_plate_and_year():
    def submit_plate_year():
        plate = plate_var.get()
        year = year_var.get()
        if plate and year:
            costs = calculate_annual_financial_report(plate, int(year))
            total_cost = sum(costs.values())
            messagebox.showinfo("Bilan Financier Annuel", 
                                f"Le coût annuel pour le véhicule avec la plaque {plate} en {year} est de {total_cost} euros.\n\n"
                                f"Détails :\n"
                                f" - Pleins : {costs['plein']} euros\n"
                                f" - Révisions : {costs['révision']} euros\n"
                                f" - Réparations : {costs['réparation']} euros\n"
                                f" - Contrôles Techniques : {costs['contrôle_technique']} euros")
            plate_year_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une plaque d'immatriculation et une année.")

    plate_year_window = tk.Toplevel(root)
    plate_year_window.title("Entrer la plaque d'immatriculation et l'année")

    font_style = ("Helvetica", 10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]

    # Plaque d'immatriculation
    plate_label = tk.Label(plate_year_window, text="Plaque d'immatriculation", font=font_style)
    plate_label.pack(pady=10)
    
    plate_var = tk.StringVar()
    plate_var.set(plaques[0] if plaques else "")

    plate_combobox = ttk.Combobox(plate_year_window, textvariable=plate_var, values=plaques, font=font_style)
    plate_combobox.pack(pady=5)
    
    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_year_window.destroy()
        return

    # Année
    year_label = tk.Label(plate_year_window, text="Année", font=font_style)
    year_label.pack(pady=10)
    
    years = list(range(2020, 2031))
    year_var = tk.StringVar(plate_year_window)
    year_var.set(years[0])  # Valeur par défaut
    
    year_menu = tk.OptionMenu(plate_year_window, year_var, *years)
    year_menu.pack(pady=5)
    
    submit_button = tk.Button(plate_year_window, text="Soumettre", command=submit_plate_year, font=font_style)
    submit_button.pack(pady=10)
    
#%% Demande de bilan financier total

def calculate_financial_report(plaque):
    costs = {
        "plein": 0,
        "révision": 0,
        "réparation": 0,
        "contrôle_technique": 0
    }

    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Calculer le coût des pleins
        cursor.execute('SELECT SUM(prix) FROM plein WHERE plaque_immatriculation = ?', (plaque,))
        plein_cost = cursor.fetchone()[0]
        if plein_cost:
            costs["plein"] = plein_cost
        
        # Calculer le coût des révisions
        cursor.execute('SELECT SUM(prix) FROM révision WHERE plaque_immatriculation = ?', (plaque,))
        revision_cost = cursor.fetchone()[0]
        if revision_cost:
            costs["révision"] = revision_cost
        
        # Calculer le coût des réparations
        cursor.execute('SELECT SUM(prix) FROM réparation WHERE plaque_immatriculation = ?', (plaque,))
        reparation_cost = cursor.fetchone()[0]
        if reparation_cost:
            costs["réparation"] = reparation_cost
        
        # Calculer le coût des contrôles techniques
        cursor.execute('SELECT SUM(prix) FROM contrôle_technique WHERE plaque_immatriculation = ?', (plaque,))
        controle_technique_cost = cursor.fetchone()[0]
        if controle_technique_cost:
            costs["contrôle_technique"] = controle_technique_cost
    
    return costs

def ask_for_plate():
    def submit_plate():
        plate = plate_var.get()
        if plate:
            costs = calculate_financial_report(plate)
            total_cost = sum(costs.values())
            messagebox.showinfo("Bilan Financier Total", 
                                f"Le coût total pour le véhicule avec la plaque {plate} est de {total_cost} euros.\n\n"
                                f"Détails :\n"
                                f" - Pleins : {costs['plein']} euros\n"
                                f" - Révisions : {costs['révision']} euros\n"
                                f" - Réparations : {costs['réparation']} euros\n"
                                f" - Contrôles Techniques : {costs['contrôle_technique']} euros")
            plate_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une plaque d'immatriculation.")

    plate_window = tk.Toplevel(root)
    plate_window.title("Sélectionner la plaque d'immatriculation")

    font_style = ("Helvetica", 10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]

    # Plaque d'immatriculation
    plate_label = tk.Label(plate_window, text="Plaque d'immatriculation", font=font_style)
    plate_label.pack(pady=10)
    
    plate_var = tk.StringVar()
    plate_var.set(plaques[0] if plaques else "")

    plate_combobox = ttk.Combobox(plate_window, textvariable=plate_var, values=plaques, font=font_style)
    plate_combobox.pack(pady=5)
    
    if not plaques:  # Si aucune plaque n'est disponible
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_window.destroy()
        return

    submit_button = tk.Button(plate_window, text="Soumettre", command=submit_plate, font=font_style)
    submit_button.pack(pady=10)


#%% Consulter des infos sur un véhicule

def consult_vehicle_info():
    def submit_plate():
        plate = plate_var.get()
        if plate:
            with connect_db() as conn:
                cursor = conn.cursor()
                
                # Récupérer les informations du véhicule
                cursor.execute('''
                    SELECT plaque_immatriculation, pôle, marque_modèle, en_service, nombre_de_clés, carburant, mise_en_circulation, 
                           vignette_crit_air, fin_assurance, équipement, kilométrage, remarques, prochaine_revision, contrat, utilisateur
                    FROM voiture 
                    WHERE plaque_immatriculation = ?
                ''', (plate,))
                vehicle_info = cursor.fetchone()
                
                if vehicle_info:
                    info_text = (f"Informations du véhicule pour la plaque {plate}:\n\n"
                                 f"Pôle : {vehicle_info[1]}\n"
                                 f"Marque : {vehicle_info[2]}\n"
                                 f"En service : {vehicle_info[3]}\n"
                                 f"Nombre de clés : {vehicle_info[4]}\n"
                                 f"Carburant : {vehicle_info[5]}\n"
                                 f"Mise en circulation : {vehicle_info[6]}\n"
                                 f"Vignette Crit'Air : {vehicle_info[7]}\n"
                                 f"Prochain Contrôle technique : {vehicle_info[8]}\n"
                                 f"Equipements : {vehicle_info[9]}\n"
                                 f"Remarques : {vehicle_info[10]}\n"
                                 f"Kilométrage : {vehicle_info[11]} km\n"
                                 f"Prochaine révision : {vehicle_info[12]} km\n"
                                 f"Contrat : {vehicle_info[13]}\n"
                                 f"Utilisateur associé : {vehicle_info[14]}\n")
                    messagebox.showinfo("Informations du véhicule", info_text)
                else:
                    messagebox.showwarning("Avertissement", "Aucun véhicule trouvé avec cette plaque d'immatriculation.")
                
            plate_window.destroy()
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une plaque d'immatriculation.")

    plate_window = tk.Toplevel(root)
    plate_window.title("Sélectionner la plaque d'immatriculation")

    plate_label = tk.Label(plate_window, text="Plaque d'immatriculation", font=("Helvetica", 10))
    plate_label.pack(pady=10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()
    
    # Convertir la liste des plaques en un format approprié pour le menu déroulant
    plaques = [plaque[0] for plaque in plaques]
    plate_var = tk.StringVar(plate_window)
    plate_var.set(plaques[0])  # Valeur par défaut

    plate_menu = tk.OptionMenu(plate_window, plate_var, *plaques)
    plate_menu.pack(pady=5)

    submit_button = tk.Button(plate_window, text="Soumettre", command=submit_plate, font=("Helvetica", 10))
    submit_button.pack(pady=10)

#%% Consulter les frais d'essence mensuel d'une voiture

def ask_for_plate_bis():
    def submit_plate():
        plate = plate_var.get().strip()
        year = year_combobox.get()
        if plate and year:
            try:
                show_detailed_fuel_expenses(plate, year)
                plate_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une plaque d'immatriculation et sélectionner une année valides.")

    plate_window = tk.Toplevel(root)
    plate_window.title("Entrer la plaque d'immatriculation et sélectionner une année")

    plate_label = tk.Label(plate_window, text="Plaque d'immatriculation", font=("Helvetica", 10))
    plate_label.pack(pady=10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour le menu déroulant
    plaques = [plaque[0] for plaque in plaques]
    plate_var = tk.StringVar(plate_window)
    if plaques:  # Vérifier s'il y a des plaques disponibles
        plate_var.set(plaques[0])  # Valeur par défaut
        plate_menu = ttk.Combobox(plate_window, textvariable=plate_var, values=plaques, font=("Helvetica", 10))
        plate_menu.pack(pady=5)
    else:
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_window.destroy()
        return

    year_label = tk.Label(plate_window, text="Sélectionner l'année", font=("Helvetica", 10))
    year_label.pack(pady=10)

    # Combobox pour la sélection de l'année
    years = [str(year) for year in range(2020, 2031)]
    year_combobox = ttk.Combobox(plate_window, values=years, font=("Helvetica", 10))
    year_combobox.pack(pady=5)

    submit_button = tk.Button(plate_window, text="Soumettre", command=submit_plate, font=("Helvetica", 10))
    submit_button.pack(pady=10)

def show_detailed_fuel_expenses(plaque, year):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date_du_plein, litre, prix FROM plein WHERE plaque_immatriculation = ? AND strftime("%Y", date_du_plein) = ?', (plaque, year))
        records = cursor.fetchall()

    if records:
        details = "\n".join([f"Date: {date}, Litres: {litres}, Prix: {prix} euros" for date, litres, prix in records])
        messagebox.showinfo("Frais d'essence détaillés", f"Frais d'essence pour la plaque {plaque} en {year}:\n\n{details}")
    else:
        messagebox.showinfo("Frais d'essence détaillés", f"Aucun frais d'essence trouvé pour la plaque {plaque} en {year}.")
        
#%% Consulter les interventions d'une voiture

def ask_for_plate_ter():
    def submit_plate():
        plate = plate_var.get().strip()
        if plate:
            try:
                show_vehicle_details(plate)
                plate_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez entrer une plaque d'immatriculation valide.")

    plate_window = tk.Toplevel(root)
    plate_window.title("Entrer la plaque d'immatriculation")

    plate_label = tk.Label(plate_window, text="Plaque d'immatriculation", font=("Helvetica", 10))
    plate_label.pack(pady=10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    # Convertir la liste des plaques en un format approprié pour la combobox
    plaques = [plaque[0] for plaque in plaques]
    plate_var = tk.StringVar(plate_window)
    if plaques:  # Vérifier s'il y a des plaques disponibles
        plate_var.set(plaques[0])  # Valeur par défaut
        plate_combobox = ttk.Combobox(plate_window, textvariable=plate_var, values=plaques, font=("Helvetica", 10))
        plate_combobox.pack(pady=5)
    else:
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_window.destroy()
        return

    submit_button = tk.Button(plate_window, text="Soumettre", command=submit_plate, font=("Helvetica", 10))
    submit_button.pack(pady=10)

def show_vehicle_details(plaque):
    repairs = get_repairs(plaque)
    revisions = get_revisions(plaque)
    technical_controls = get_technical_controls(plaque)

    details = ""

    if repairs:
        details += "Réparations:\n" + "\n".join([f"Date: {date}, Description: {description}, Prix: {prix} euros, Garage: {garage}" for date, description, prix, garage in repairs]) + "\n\n"
    else:
        details += "Aucune réparation trouvée pour cette plaque.\n\n"

    if revisions:
        details += "Révisions:\n" + "\n".join([f"Date: {date}, Kilomètres: {kilometres}, Prix: {prix} euros, Garage: {garage}, Remarques: {remarques}" for date, kilometres, prix, garage, remarques in revisions]) + "\n\n"
    else:
        details += "Aucune révision trouvée pour cette plaque.\n\n"

    if technical_controls:
        details += "Contrôles Techniques:\n" + "\n".join([f"Date: {date}, Garage: {garage}, Prix: {prix} euros, Remarques: {remarques}" for date, garage, prix, remarques in technical_controls])
    else:
        details += "Aucun contrôle technique trouvé pour cette plaque."

    messagebox.showinfo("Détails du véhicule", f"Détails pour la plaque {plaque}:\n\n{details}")

def get_repairs(plaque):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date_de_la_réparation, libellé, prix, garage FROM réparation WHERE plaque_immatriculation = ? ORDER BY date_de_la_réparation DESC', (plaque,))
        return cursor.fetchall()

def get_revisions(plaque):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date_de_la_révision, révision_kilometre, prix, garage, remarques FROM révision WHERE plaque_immatriculation = ? ORDER BY date_de_la_révision DESC', (plaque,))
        return cursor.fetchall()

def get_technical_controls(plaque):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT date_du_contrôle_technique, garage, prix, remarques FROM contrôle_technique WHERE plaque_immatriculation = ? ORDER BY date_du_contrôle_technique DESC', (plaque,))
        return cursor.fetchall()


#%% Modifier une information sur un véhicule

def ask_for_plate_and_modify():
    def submit_plate():
        plate = plate_var.get()
        if plate:
            try:
                modify_vehicle_detail(plate)
                plate_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")
        else:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une plaque d'immatriculation valide.")

    plate_window = tk.Toplevel(root)
    plate_window.title("Sélectionner la plaque d'immatriculation")

    font_style = ("Helvetica", 10)

    # Récupérer les plaques d'immatriculation depuis la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT plaque_immatriculation FROM voiture')
        plaques = cursor.fetchall()

    plaques = [plaque[0] for plaque in plaques]

    if not plaques:
        messagebox.showwarning("Avertissement", "Aucune plaque d'immatriculation disponible.")
        plate_window.destroy()
        return

    plate_label = tk.Label(plate_window, text="Plaque d'immatriculation", font=font_style)
    plate_label.pack(pady=10)

    plate_var = tk.StringVar()
    plate_var.set(plaques[0])  # Valeur par défaut

    plate_combobox = ttk.Combobox(plate_window, textvariable=plate_var, values=plaques, font=font_style)
    plate_combobox.pack(pady=5)

    submit_button = tk.Button(plate_window, text="Soumettre", command=submit_plate, font=font_style)
    submit_button.pack(pady=10)

def modify_vehicle_detail(plaque):
    # Liste des champs modifiables
    fields = [
        "pôle", "marque_modèle", "en_service", "nombre_de_clés", "carburant", 
        "mise_en_circulation", "vignette_crit_air", "fin_assurance", "équipement", 
        "remarques", "dernière_révision", "prochaine_révision", "kilométrage", "utilisateur_associe"
    ]

    def submit_selection():
        selected_fields = [field for field, var in check_vars.items() if var.get()]
        if not selected_fields:
            messagebox.showwarning("Avertissement", "Aucun champ sélectionné.")
            return
        # Demander la nouvelle valeur pour chaque champ sélectionné
        for field in selected_fields:
            if field == "équipement":
                # Ouvrir la fenêtre pour modifier l'équipement
                modify_equipment(plaque)
            else:
                new_value = simpledialog.askstring("Nouvelle valeur", f"Entrer la nouvelle valeur pour {field}:")
                if not new_value:
                    messagebox.showwarning("Avertissement", f"Valeur invalide pour {field}.")
                    return
                update_field(field, new_value, plaque)
        messagebox.showinfo("Succès", "Les champs ont été mis à jour avec succès.")
        modify_window.destroy()

    modify_window = tk.Toplevel(root)
    modify_window.title("Modifier les détails du véhicule")

    font_style = ("Helvetica", 10)

    check_vars = {}
    for field in fields:
        var = tk.BooleanVar()
        check_vars[field] = var
        checkbutton = tk.Checkbutton(modify_window, text=field, variable=var, font=font_style)
        checkbutton.pack(anchor="w")

    submit_button = tk.Button(modify_window, text="Soumettre", command=submit_selection, font=font_style)
    submit_button.pack(pady=10)

def modify_equipment(plaque):
    def submit_equipment():
        equipment_values = {
            "Roue de secours": roue_var.get(),
            "Gilet jaune": gilet_var.get(),
            "Triangle": triangle_var.get()
        }
        # Construire la nouvelle valeur d'équipement
        new_equipment = ', '.join([key for key, value in equipment_values.items() if value])
        update_field("équipement", new_equipment, plaque)
        messagebox.showinfo("Succès", "L'équipement a été mis à jour avec succès.")
        equip_window.destroy()

    equip_window = tk.Toplevel(root)
    equip_window.title("Modifier l'équipement")

    font_style = ("Helvetica", 10)

    # Création des cases à cocher pour les équipements
    equip_frame = tk.Frame(equip_window)
    equip_frame.pack(padx=10, pady=10)

    roue_var = tk.BooleanVar()
    gilet_var = tk.BooleanVar()
    triangle_var = tk.BooleanVar()

    tk.Checkbutton(equip_frame, text="Roue de secours", variable=roue_var, font=font_style).pack(anchor='w')
    tk.Checkbutton(equip_frame, text="Gilet jaune", variable=gilet_var, font=font_style).pack(anchor='w')
    tk.Checkbutton(equip_frame, text="Triangle", variable=triangle_var, font=font_style).pack(anchor='w')

    submit_button = tk.Button(equip_window, text="Soumettre", command=submit_equipment, font=font_style)
    submit_button.pack(pady=10)

def update_field(field, new_value, plaque):
    # Mise à jour de la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        query = f"UPDATE voiture SET {field} = ? WHERE plaque_immatriculation = ?"
        cursor.execute(query, (new_value, plaque))
        conn.commit()

#%% Supprimer une donnée

def ask_for_deletion():
    def submit_selection():
        plate = plate_combobox.get().strip()
        table = table_combobox.get()

        if not plate or not table:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner la plaque d'immatriculation et le tableau.")
            return

        try:
            # Récupérer les données pour la plaque et le tableau sélectionnés
            data, columns = get_data_for_plate_and_table(plate, table)
            if not data:
                messagebox.showwarning("Avertissement", "Aucune donnée trouvée pour cette plaque et ce tableau.")
                return
            
            # Afficher les données dans une nouvelle fenêtre
            show_data_for_deletion(data, columns, plate, table)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def get_tables():
        # Obtenir les noms des tables de la base de données
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
        return tables

    def get_plates():
        # Obtenir les plaques d'immatriculation disponibles
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT plaque_immatriculation FROM plein UNION SELECT DISTINCT plaque_immatriculation FROM révision UNION SELECT DISTINCT plaque_immatriculation FROM réparation UNION SELECT DISTINCT plaque_immatriculation FROM contrôle_technique;")
            plates = [row[0] for row in cursor.fetchall()]
        return plates

    # Créer la fenêtre principale pour la suppression
    deletion_window = tk.Toplevel(root)
    deletion_window.title("Supprimer une donnée")

    plate_label = tk.Label(deletion_window, text="Plaque d'immatriculation", font=("Helvetica", 10))
    plate_label.pack(pady=10)

    # Menu déroulant pour sélectionner la plaque d'immatriculation
    plate_combobox = ttk.Combobox(deletion_window, values=get_plates(), font=("Helvetica", 10))
    plate_combobox.pack(pady=5)
    
    table_label = tk.Label(deletion_window, text="Sélectionner le tableau", font=("Helvetica", 10))
    table_label.pack(pady=10)

    # Menu déroulant pour sélectionner le tableau
    table_combobox = ttk.Combobox(deletion_window, values=get_tables(), font=("Helvetica", 10))
    table_combobox.pack(pady=5)

    submit_button = tk.Button(deletion_window, text="Supprimer", command=submit_selection, font=("Helvetica", 10))
    submit_button.pack(pady=10)

def get_data_for_plate_and_table(plate, table):
    # Récupérer les données correspondant à la plaque et au tableau
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [row[1] for row in cursor.fetchall()]
        query = f"SELECT * FROM {table} WHERE plaque_immatriculation = ?"
        cursor.execute(query, (plate,))
        rows = cursor.fetchall()
    return rows, columns

def show_data_for_deletion(data, columns, plate, table):
    def delete_row():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner une ligne à supprimer.")
            return
        # Obtenir le numéro de facture de la ligne sélectionnée
        item_values = tree.item(selected_item[0])['values']
        num_facture = item_values[columns.index("numéro_facture")]
        try:
            delete_data_from_table(num_facture, table)
            messagebox.showinfo("Succès", "La donnée a été supprimée avec succès.")
            delete_window.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    delete_window = tk.Toplevel(root)
    delete_window.title("Choisir la donnée à supprimer")

    # Créer un tableau pour afficher les données
    tree = ttk.Treeview(delete_window, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill='both')

    for row in data:
        tree.insert('', 'end', values=row)
    
    delete_button = tk.Button(delete_window, text="Supprimer", command=delete_row, font=("Helvetica", 10))
    delete_button.pack(pady=10)

def delete_data_from_table(numéro_facture, table):
    # Supprimer la ligne de la base de données
    with connect_db() as conn:
        cursor = conn.cursor()
        query = f"DELETE FROM {table} WHERE numéro_facture = ?"
        cursor.execute(query, (numéro_facture,))
        conn.commit()


#%% Retourner les informations importantes

#Contrôle technique

def verifier_controles_techniques():
    aujourd_hui = datetime.now()
    date_limite = aujourd_hui + timedelta(days=30)

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT plaque_immatriculation, marque_modèle, fin_assurance
            FROM voiture
            WHERE fin_assurance BETWEEN ? AND ?
        ''', (aujourd_hui.date(), date_limite.date()))
        
        resultats = cursor.fetchall()

    return resultats

def afficher_controles_techniques():
    resultats = verifier_controles_techniques()

    # Créer la fenêtre principale (invisible)
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Préparer le message à afficher
    if resultats:
        message = "Contrôles techniques à venir dans les 30 jours :\n\n"
        for plaque, marque, fin_assurance in resultats:
            message += f"Plaque : {plaque}, Marque/Modèle : {marque}, Date du Contrôle : {fin_assurance}\n"
    else:
        message = "Aucun contrôle technique prévu dans les 30 jours."

    # Afficher les résultats dans une boîte de dialogue
    messagebox.showinfo("Contrôles Techniques à Venir", message)
    
    # Détruire la fenêtre principale après la fermeture de la boîte de dialogue
    root.destroy()

#Révision

def verifier_revisions():
    aujourd_hui = datetime.now()
    date_limite = aujourd_hui + timedelta(days=30)
    
    voitures_a_reviser = []

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT v.plaque_immatriculation, v.marque_modèle, v.mise_en_circulation, v.kilométrage, 
                   r.date_de_la_révision, v.prochaine_revision
            FROM voiture v
            LEFT JOIN révision r ON v.plaque_immatriculation = r.plaque_immatriculation
        ''')
        resultats = cursor.fetchall()

    for plaque, marque, date_mise_en_circulation, kilométrage, date_derniere_revision, prochaine_révision_km in resultats:
        besoin_revision = False

        # Vérifier la date de la dernière révision
        if date_derniere_revision:
            date_prochaine_revision = datetime.strptime(date_derniere_revision, "%Y-%m-%d") + timedelta(days=730)
            if aujourd_hui <= date_prochaine_revision <= date_limite:
                besoin_revision = True

        # Si aucune révision n'a été faite, vérifier la date de mise en circulation
        if not besoin_revision and date_mise_en_circulation:
            date_prochaine_revision = datetime.strptime(date_mise_en_circulation, "%Y-%m-%d") + timedelta(days=730)
            if aujourd_hui <= date_prochaine_revision <= date_limite:
                besoin_revision = True

        # Vérifier le kilométrage par rapport à la prochaine révision prévue
        if not besoin_revision and prochaine_révision_km:
            if kilométrage >= (prochaine_révision_km - 500):
                besoin_revision = True

        if besoin_revision:
            voitures_a_reviser.append((plaque, marque, date_mise_en_circulation, kilométrage, date_derniere_revision, prochaine_révision_km))

    return voitures_a_reviser

def afficher_revisions_prochaines():
    resultats = verifier_revisions()

    # Créer la fenêtre principale (invisible)
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Préparer le message à afficher
    if resultats:
        message = "Véhicules nécessitant une révision prochaine :\n\n"
        for plaque, marque, date_mise_en_circulation, kilometrage, date_derniere_revision, prochaine_revision_km in resultats:
            message += f"Plaque : {plaque}, Marque/Modèle : {marque}\n"
            message += f"  - Date de mise en circulation : {date_mise_en_circulation}\n"
            message += f"  - Kilométrage : {kilometrage} km\n"
            if date_derniere_revision:
                message += f"  - Dernière révision : {date_derniere_revision}\n"
            if prochaine_revision_km:
                message += f"  - Prochaine révision prévue à : {prochaine_revision_km} km\n"
            message += "\n"
    else:
        message = "Aucun véhicule ne nécessite une révision prochaine."

    # Afficher les résultats dans une boîte de dialogue
    messagebox.showinfo("Révisions Prochaines", message)
    
    # Détruire la fenêtre principale après la fermeture de la boîte de dialogue
    root.destroy()

#Manque d'équipement

def verifier_equipements():
    # Les équipements essentiels
    equipements_essentiels = ["Gilet jaune", "Triangle"]
    
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT plaque_immatriculation, marque_modèle, équipement
            FROM voiture
        ''')
        resultats = cursor.fetchall()

    # Identifier les équipements manquants pour chaque véhicule
    vehicules_manquants = []
    for plaque, marque, equipement in resultats:
        equipements_presentes = set(equipement.split(', '))
        equipements_manquants = [e for e in equipements_essentiels if e not in equipements_presentes]
        if equipements_manquants:
            vehicules_manquants.append((plaque, marque, equipements_manquants))

    return vehicules_manquants

def afficher_equipements_manquants():
    resultats = verifier_equipements()

    # Créer la fenêtre principale (invisible)
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Préparer le message à afficher
    if resultats:
        message = "Équipements manquants pour certains véhicules :\n\n"
        for plaque, marque, equipements_manquants in resultats:
            message += f"Plaque : {plaque}, Marque/Modèle : {marque}, Équipements manquants : {', '.join(equipements_manquants)}\n"
    else:
        message = "Tous les véhicules ont les équipements essentiels."

    # Afficher les résultats dans une boîte de dialogue
    messagebox.showinfo("Équipements Manquants", message)
    
    # Détruire la fenêtre principale après la fermeture de la boîte de dialogue
    root.destroy()

#Remarques voiture

def verifier_remarques():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT plaque_immatriculation, marque_modèle, remarques
            FROM voiture
            WHERE remarques IS NULL OR remarques <> 'RAS'
        ''')
        resultats = cursor.fetchall()

    return resultats

def afficher_remarques():
    resultats = verifier_remarques()

    # Créer la fenêtre principale (invisible)
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale

    # Préparer le message à afficher
    if resultats:
        message = "Remarques des véhicules :\n\n"
        for plaque, marque, remarques in resultats:
            remarques_affiche = remarques if remarques else "Aucune remarque"
            message += f"Plaque : {plaque}, Marque/Modèle : {marque}, Remarque : {remarques_affiche}\n"
    else:
        message = "Toutes les remarques sont marquées comme 'RAS' ou les champs sont vides."

    # Afficher les résultats dans une boîte de dialogue
    messagebox.showinfo("Remarques des Véhicules", message)
    
    # Détruire la fenêtre principale après la fermeture de la boîte de dialogue
    root.destroy()
    
#%% Exporter les données en tableau Excel

def exporter_tableau_voiture():
    db_file = 'database.db'  # Nom du fichier SQLite
    table_name = 'voiture'   # Nom de la table à exporter
    output_file = 'Voitures.xlsx'  # Nom du fichier Excel de sortie
    try:
        conn = sqlite3.connect(db_file)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        df.to_excel(output_file, index=False, engine='openpyxl')
        messagebox.showinfo("Exportation réussie", f"La table {table_name} a été exportée avec succès vers {output_file}.")  
    except Exception as e:
        messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite : {str(e)}")    
    finally:
        if conn:
            conn.close()

# Fonction d'exportation pour les autres tables (à implémenter)
def exporter_tableau_reparation():
    db_file = 'database.db'  # Nom du fichier SQLite
    table_name = 'réparation'  # Nom de la table à exporter
    output_file = 'Réparations.xlsx'  # Nom du fichier Excel de sortie
    try:
        # Se connecter à la base de données SQLite
        conn = sqlite3.connect(db_file)
        # Calculer la date de 12 mois avant aujourd'hui
        date_limite = datetime.now() - timedelta(days=365)
        date_limite_str = date_limite.strftime('%Y-%m-%d')
        # Lire la table SQL avec un filtre sur la date
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE date_de_la_réparation >= ?
        """
        df = pd.read_sql(query, conn, params=(date_limite_str,))
        # Écrire le DataFrame dans un fichier Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        # Afficher un message de succès
        messagebox.showinfo("Exportation réussie", f"La table {table_name} a été exportée avec succès vers {output_file}.")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception
        messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite : {str(e)}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            conn.close()

def exporter_tableau_revision():
    db_file = 'database.db'  # Nom du fichier SQLite
    table_name = 'révision'  # Nom de la table à exporter
    output_file = 'Révisions.xlsx'  # Nom du fichier Excel de sortie
    try:
        # Se connecter à la base de données SQLite
        conn = sqlite3.connect(db_file)
        # Calculer la date de 12 mois avant aujourd'hui
        date_limite = datetime.now() - timedelta(days=365)
        date_limite_str = date_limite.strftime('%Y-%m-%d')
        # Lire la table SQL avec un filtre sur la date
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE date_de_la_révision >= ?
        """
        df = pd.read_sql(query, conn, params=(date_limite_str,))
        # Écrire le DataFrame dans un fichier Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        # Afficher un message de succès
        messagebox.showinfo("Exportation réussie", f"La table {table_name} a été exportée avec succès vers {output_file}.")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception
        messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite : {str(e)}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            conn.close()

def exporter_tableau_plein():
    db_file = 'database.db'  # Nom du fichier SQLite
    table_name = 'plein'  # Nom de la table à exporter
    output_file = 'Pleins.xlsx'  # Nom du fichier Excel de sortie
    try:
        # Se connecter à la base de données SQLite
        conn = sqlite3.connect(db_file)
        # Calculer la date de 12 mois avant aujourd'hui
        date_limite = datetime.now() - timedelta(days=183)
        date_limite_str = date_limite.strftime('%Y-%m-%d')
        # Lire la table SQL avec un filtre sur la date
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE date_du_plein >= ?
        """
        df = pd.read_sql(query, conn, params=(date_limite_str,))
        # Écrire le DataFrame dans un fichier Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        # Afficher un message de succès
        messagebox.showinfo("Exportation réussie", f"La table {table_name} a été exportée avec succès vers {output_file}.")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception
        messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite : {str(e)}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            conn.close()

def exporter_tableau_ct():
    db_file = 'database.db'  # Nom du fichier SQLite
    table_name = 'contrôle_technique'  # Nom de la table à exporter
    output_file = 'Contrôles_techniques.xlsx'  # Nom du fichier Excel de sortie
    try:
        # Se connecter à la base de données SQLite
        conn = sqlite3.connect(db_file)
        # Calculer la date de 12 mois avant aujourd'hui
        date_limite = datetime.now() - timedelta(days=365)
        date_limite_str = date_limite.strftime('%Y-%m-%d')
        # Lire la table SQL avec un filtre sur la date
        query = f"""
        SELECT * 
        FROM {table_name}
        WHERE date_du_contrôle_technique >= ?
        """
        df = pd.read_sql(query, conn, params=(date_limite_str,))
        # Écrire le DataFrame dans un fichier Excel
        df.to_excel(output_file, index=False, engine='openpyxl')
        # Afficher un message de succès
        messagebox.showinfo("Exportation réussie", f"La table {table_name} a été exportée avec succès vers {output_file}.")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception
        messagebox.showerror("Erreur d'exportation", f"Une erreur s'est produite : {str(e)}")
    finally:
        # Fermer la connexion à la base de données
        if conn:
            conn.close()


#%% Lancement du script

root = tk.Tk()
root.title("Gestion de Parc Automobile")

main_frame = tk.Frame(root)
main_frame.pack(pady=10)

main_label = tk.Label(main_frame, text="Que voulez-vous faire ?", font=("Helvetica", 10))
main_label.pack()

main_action_var = tk.StringVar()
main_actions = ["Ajouter un élément", "Faire un bilan financier", "Consulter des informations","Modifier une information","Informations importantes","Exporter les données en Excel"]
for action in main_actions:
    radio = tk.Radiobutton(main_frame, text=action, variable=main_action_var, value=action, command=on_main_action_select, font=("Helvetica", 10))
    radio.pack(anchor='w')

# Frame pour les options d'ajout
add_frame = tk.Frame(root)
add_label = tk.Label(add_frame, text="Quel type d'élément voulez-vous ajouter ?", font=("Helvetica", 10))
add_label.pack(anchor='w')

add_action_var = tk.StringVar()
add_actions = ["Un véhicule", "Un plein", "Un contrôle technique", "Une réparation", "Une révision"]
for action in add_actions:
    radio = tk.Radiobutton(add_frame, text=action, variable=add_action_var, value=action, command=on_add_action_select, font=("Helvetica", 10))
    radio.pack(anchor='w')

# Frame pour les options de bilan
bilan_frame = tk.Frame(root)
bilan_label = tk.Label(bilan_frame, text="Quel type de bilan voulez-vous faire ?", font=("Helvetica", 10))
bilan_label.pack(anchor='w')

bilan_action_var = tk.StringVar()
bilan_actions = ["Bilan mensuel d'un véhicule", "Bilan annuel d'un véhicule", "Bilan total d'un véhicule"]
for action in bilan_actions:
    radio = tk.Radiobutton(bilan_frame, text=action, variable=bilan_action_var, value=action, command=on_bilan_action_select, font=("Helvetica", 10))
    radio.pack(anchor='w')
    
consult_action_var = tk.StringVar()
consult_frame = tk.Frame(root)
consult_action_label = tk.Label(consult_frame, text="Que voulez-vous consulter ?")
consult_action_label.pack(pady=10)
consult_options = ["Consulter les infos d'un véhicule", "Consulter les pleins d'un véhicule", "Consulter les interventions d'un véhicule"]
for option in consult_options:
    rb = tk.Radiobutton(consult_frame, text=option, variable=consult_action_var, value=option, command=on_consult_action_select)
    rb.pack(anchor="w")

modify_action_var = tk.StringVar()
modify_frame = tk.Frame(root)
modify_action_label = tk.Label(modify_frame, text="Que voulez-vous modifier ?")
modify_action_label.pack(pady=10)
modify_options = ["Modifier une informations sur un véhicule", "Supprimer une donnée"]
for option in modify_options:
    rb = tk.Radiobutton(modify_frame, text=option, variable=modify_action_var, value=option, command=on_modify_action_select)
    rb.pack(anchor="w")

verify_action_var = tk.StringVar()
verify_frame = tk.Frame(root)
verify_action_label = tk.Label(verify_frame, text="Que voulez-vous voir ?")
verify_action_label.pack(pady=10)
verify_options = ["Contrôle(s) technique(s) urgent(s)","Voir le(s) révision(s) urgente(s)","Voir les équipements manquants","Voir les remarques importantes"]
for option in verify_options:
    rb = tk.Radiobutton(verify_frame, text=option, variable=verify_action_var, value=option, command=on_verify_action_select)
    rb.pack(anchor="w")
    
export_action_var = tk.StringVar()
export_frame = tk.Frame(root)
export_action_label = tk.Label(export_frame, text="Que voulez-vous exporter ?")
export_action_label.pack(pady=10)
export_options = ["Exporter le tableau des voitures","Exporter le tableau des réparations (12 derniers mois)","Exporter le tableau des révisions (12 derniers mois)","Exporter le tableau des pleins (6 derniers mois)","Exporter le tableau des contrôles techniques (12 derniers mois)"]
for option in export_options:
    rb = tk.Radiobutton(export_frame, text=option, variable=export_action_var, value=option, command=on_export_action_select)
    rb.pack(anchor="w")

# Lancement de la boucle principale
root.mainloop()