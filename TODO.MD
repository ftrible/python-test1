Architecture technique du MVP
Front-end (interface utilisateur)

Site web responsive plutôt qu'une application native dans un premier temps
Interface simplifiée et accessible pour les seniors (gros boutons, texte lisible, navigation intuitive)

Interface administrative

Tableau de bord pour gérer les demandes, les bénévoles et les suivis
Django pour accélérer le développement

Back-end

API RESTful

Node.js/Django (Python)


Base de données

sqlite


Authentification

Django Authentication pour ne pas réinventer la roue


Fonctionnalités essentielles pour le MVP

Gestion des utilisateurs

Inscription/connexion pour administrateurs et bénévoles
Profils simplifiés pour les seniors (créés par les administrateurs)


Système de demandes

Formulaire simple pour créer une demande (par téléphone puis saisi par un opérateur)
Catégorisation des demandes (courses, livraison, transport)
Assignation manuelle des tâches aux bénévoles disponibles


Suivi des demandes

Tableau de bord pour visualiser l'état des demandes
Notifications par email/SMS pour les bénévoles
Rapport simple sur les services rendus


Communication

Notifications

Service d'emails comme SendGrid ou Mailjet
Notifications SMS via Twilio pour les seniors moins connectés


Système téléphonique simplifié

Numéro de téléphone dédié pour les seniors n'utilisant pas internet
Saisie manuelle des demandes par un opérateur dans un premier temps

Hébergement

Plateforme serverless comme Vercel ou Netlify pour le front-end
Heroku ou Digital Ocean pour le back-end (solutions simples et économiques)

Priorité pour le MVP
Concentrez-vous d'abord sur :

La simplicité d'utilisation pour tous les utilisateurs
La fiabilité du processus de demande et d'attribution
La capacité à suivre et mesurer l'activité
