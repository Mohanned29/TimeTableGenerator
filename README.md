# Système de Génération d'Emploi du Temps

## Vue d'ensemble de l'Architecture Système

![Texte alternatif](images.UML2.0.png)

Ce projet est une solution de planification avancée spécialement conçue pour la Faculté d'Informatique. Ce projet vise à automatiser et à rationaliser la création des emplois du temps, répondant aux défis spécifiques de planification rencontrés par les établissements académiques.

Le système de planification est conçu pour gérer et générer des emplois du temps pour diverses sections académiques au sein d'une institution. Il utilise plusieurs classes et méthodes interconnectées pour allouer efficacement des salles, des enseignants et des créneaux horaires pour les cours, tels que spécifiés dans la configuration JSON.

## Module : m_schedule_generator.py

### I) Classe : ScheduleGenerator

Cette classe encapsule la logique de génération des emplois du temps pour une section spécifique.

#### Attributs

- **year :** L'année académique pour laquelle l'emploi du temps est généré.
- **section :** La section académique pour laquelle l'emploi du temps est généré.
- **rooms :** Liste des salles disponibles pour la planification.
- **teachers :** Liste des enseignants disponibles, y compris leurs modules d'enseignement et leur disponibilité.
- **schedule :** Liste qui stocke les entrées de l'emploi du temps généré.
- **assigned_lectures :** Ensemble qui garde une trace des conférences déjà attribuées pour éviter les doublons.
- **assigned_group_sessions :** Ensemble pour suivre les sessions attribuées à des groupes spécifiques afin de prévenir les chevauchements.
- **teacher_commitments :** Dictionnaire pour suivre quand et où chaque enseignant est déjà planifié.
- **room_availability :** Dictionnaire pour suivre la disponibilité des salles.
- **time_slots :** Dictionnaire des créneaux horaires disponibles pour la planification des sessions.

#### Méthodes

1. **init_availability()**
   - **Objectif :** Initialise la disponibilité des salles et des enseignants.
   - **Explication :** Configure la disponibilité de chaque salle et enseignant pour tous les jours de la semaine.

2. **find_suitable_teacher(module_name, day)**
   - **Objectif :** Trouve un enseignant approprié pour un module donné un jour spécifique.
   - **Paramètres :**
     - **module_name :** Le nom du module.
     - **day :** Le jour pour lequel un enseignant est nécessaire.
   - **Retourne :** Le nom d'un enseignant approprié, ou None si aucun enseignant n'est disponible.

3. **find_available_room(session_type, day)**
   - **Objectif :** Trouve une salle disponible pour un type de session un jour spécifique.
   - **Paramètres :**
     - **session_type :** Le type de session (Conférence, TD, TP).
     - **day :** Le jour pour lequel une salle est nécessaire.
   - **Retourne :** Le nom d'une salle disponible, ou None si aucune salle n'est disponible.

4. **assign_session(group, module, session_type, day)**
   - **Objectif :** Assigne une session à un groupe, un module et un jour, en assurant la disponibilité des salles et des enseignants.
   - **Paramètres :**
     - **group :** Le groupe pour lequel la session est attribuée.
     - **module :** Le module pour lequel la session est attribuée.
     - **session_type :** Le type de session (Conférence, TD, TP).
     - **day :** Le jour de la session.
   - **Explication :** Vérifie la disponibilité des salles et des enseignants et assigne la session si possible.

5. **is_slot_available(slot, day)**
   - **Objectif :** Vérifie si un créneau spécifique est disponible pour une salle et un enseignant le jour donné.
   - **Paramètres :**
     - **slot :** Le créneau horaire vérifié.
     - **day :** Le jour vérifié.
   - **Retourne :** True si le créneau est disponible, sinon False.

6. **update_availability(room_name, teacher_name, day, slot)**
   - **Objectif :** Met à jour la disponibilité d'une salle et d'un enseignant pour un créneau et un jour spécifiques.
   - **Paramètres :**
     - **room_name :** Le nom de la salle.
     - **teacher_name :** Le nom de l'enseignant.
     - **day :** Le jour de la session.
     - **slot :** Le créneau horaire de la session.

7. **generate_schedule()**
   - **Objectif :** Génère l'emploi du temps complet pour tous les modules de la section.
   - **Retourne :** L'emploi du temps généré.
   - **Explication :** Itère à travers tous les groupes de modules dans la section et planifie les conférences, TD et TP pour chaque module en utilisant les méthodes de planification respectives.

## Module : schedule_manager.py

### II) Classe : ScheduleManager

Cette classe gère la génération des emplois du temps pour plusieurs sections.

#### Attributs

- **years :** Contient des informations sur toutes les années académiques et leurs sections respectives.
- **rooms :** Contient des données sur les salles disponibles où les sessions peuvent être planifiées.
- **teachers :** Stocke les informations sur les enseignants disponibles pour mener des sessions.

#### Méthodes

- **__init__(self, years, rooms, teachers)**
   - **Objectif :** Initialise le ScheduleManager avec les années, les salles et les enseignants.
   - **Paramètres :**
     - **years :** Dictionnaire contenant les années académiques et leurs sections respectives.
     - **rooms :** Liste des salles disponibles pour la planification.
     - **teachers :** Liste des enseignants disponibles, y compris leurs modules d'enseignement et leur disponibilité.

- **generate_schedules_for_all(self)**
   - **Objectif :** Génère les emplois du temps pour toutes les sections en créant une instance de ScheduleGenerator pour chaque section et en générant des emplois du temps en utilisant les salles et les enseignants fournis.
   - **Retourne :** Une liste des emplois du temps générés pour toutes les années et sections.
   - **Explication :** 
     - Itère à travers chaque année et section, génère des emplois du temps en utilisant ScheduleGenerator, et les compile dans un emploi du temps final.
     - Pour chaque année, itère à travers les spécialités et leurs sections, créant une instance de ScheduleGenerator pour chaque section.
     - Génère l'emploi du temps pour chaque section, ajoutant l'emploi du temps généré aux informations de la section respective.
     - Compile les emplois du temps pour toutes les sections dans l'emploi du temps final pour chaque année.

## Interaction des Composants

1. **Configuration JSON :** Contient toutes les données nécessaires sur les sections, les modules, les enseignants et les salles. Ces données servent de fondation pour les opérations de planification.
2. **Classe ScheduleManager :** Agit comme l'unité de contrôle central qui gère la planification pour toutes les sections en utilisant les instances de ScheduleGenerator. Elle accède aux ressources globales telles que la disponibilité des salles et des enseignants et coordonne les activités de planification entre les différentes sections pour éviter les conflits.
3. **Classe ScheduleGenerator :** Responsable de la génération de l'emploi du temps pour une section spécifique. Elle interagit avec les couches de données pour récupérer la disponibilité des enseignants et les horaires des salles. Cette classe contient plusieurs méthodes pour gérer les différentes tâches de planification.
4. **Interaction avec la Couche de Données :** ScheduleManager et ScheduleGenerator interagissent fortement avec les données configurées en JSON pour récupérer et mettre à jour les informations de planification. Cela inclut la vérification de la disponibilité des salles et des enseignants et la mise à jour des emplois du temps au fur et à mesure que les sessions sont attribuées.
5. **Méthodes Utilitaires :** Des méthodes comme find_suitable_teacher et find_available_room fournissent un support utilitaire en vérifiant des conditions spécifiques qui influencent les décisions de planification, assurant qu'il n'y a pas de chevauchements ou de conflits dans les emplois du temps.
6. **Flux d'Exécution :** Le système démarre en créant une instance de ScheduleManager. ScheduleManager itère ensuite à travers chaque section et crée une instance de ScheduleGenerator pour chacune d'elles. ScheduleGenerator utilise ses méthodes pour générer un emploi du temps complet pour sa section en fonction des données disponibles et des contraintes. Les résultats sont compilés dans l'emploi du temps final pour toutes les sections et peuvent être traités ou affichés.

## Intégration avec l'Application Flask

Le système de planification utilise une application web Flask pour fournir une interface conviviale permettant de gérer et de visualiser les emplois du temps générés. Flask est un framework web léger particulièrement bien adapté aux petites et moyennes applications web comme ce système de planification.

### Structure de l'Application Flask

- **app.py :** C'est le fichier principal qui contient la configuration de l'application Flask, les routes et la logique du serveur.

### Fonctionnalités Clés

- **Interface Utilisateur :** Fournit une interface interactive et facile à naviguer pour les utilisateurs afin de visualiser et de gérer les emplois du temps.
- **Points de Terminaison API :** Les routes Flask gèrent les requêtes pour générer, mettre à jour ou récupérer des emplois du temps, en interfaçant avec le backend du système de planification.
- **Visualisation des Données :** Intègre des outils pour visualiser les emplois du temps sous forme de calendrier afin de faciliter la compréhension et la gestion.

### Mise en Route

**Pour configurer et exécuter le système de planification :**

- **Installation :** Assurez-vous que Python 3.x est installé avec Flask. Installez les autres dépendances listées dans requirements.txt.
- **Exécution :** Exécutez l'application Flask avec `python app.py` et utilisez les points de terminaison API fournis pour interagir avec le système.
