import unittest
import sqlite3
import os
import time

from store_database import StoreDB 


class Teststoredatabase(unittest.TestCase):
    
    def setUp(self):
        # Crée une instance de la base de données pour les tests
        self.db = StoreDB(':memory:')  # Utilisation d'une base de données en mémoire pour les tests
    
    def test_ajout_et_recuperation_employe(self):
        # Teste l'ajout d'un employé dans la base de données et sa récupération
        self.db.ajouter_employe('John', 'Doe', '2023-01-01', 'Lundi', 40, 1, 1)
        employes = self.db.get_employes()  # Récupère la liste des employés
        self.assertEqual(len(employes), 1)  # Vérifie s'il y a un employé dans la base de données
        employe_recupere = employes[0]
        self.assertEqual(employe_recupere[1], 'John')  # Vérifie le nom de l'employé récupéré
        
    def test_suppression_employe(self):
        # Teste l'ajout et la suppression d'un employé dans la base de données
        self.db.ajouter_employe('Jane', 'Smith', '2023-01-01', 'Mardi', 35, 1, 1)
        employes_avant_suppression = self.db.get_employes()  # Récupère la liste des employés avant la suppression
        self.assertEqual(len(employes_avant_suppression), 1)  # Vérifie s'il y a un employé dans la base de données
        employe_id = employes_avant_suppression[0][0]
        self.db.supprimer_employe(employe_id)  # Supprime l'employé
        employes_apres_suppression = self.db.get_employes()  # Récupère la liste des employés après la suppression
        self.assertEqual(len(employes_apres_suppression), 0)  # Vérifie s'il n'y a plus d'employé dans la base de données
        
    def test_ajout_et_recuperation_planning(self):
        # Teste l'ajout d'un planning et sa récupération
        self.db.ajouter_employe('Alice', 'Johnson', '2023-01-01', 'Mercredi', 30, 1, 1)
        employes = self.db.get_employes()  # Récupère la liste des employés
        employe_id = employes[0][0]
        self.db.ajouter_planning(employe_id, '2023-11-01', '09:00', '17:00')  # Ajoute un planning pour l'employé
        planning = self.db.get_planning(employe_id, '2023-11-01')  # Récupère le planning
        self.assertIsNotNone(planning)  # Vérifie que le planning a été ajouté
        self.assertEqual(planning[3], '09:00')  # Vérifie l'heure de début du planning


#### TESTS LIMITES 
        
    def test_ajout_employe_avec_valeurs_nulles(self):
        self.db.ajouter_employe('', '', '', '', 0, 0, 0)
        employes = self.db.get_employes()
        self.assertEqual(len(employes), 0)  # Aucun employé ne devrait être ajouté avec des valeurs nulles

    def test_recuperation_employe_inexistant(self):
        employe = self.db.get_employes(filtre='id = 999')
        self.assertEqual(len(employe), 0)  # Aucun employé ne devrait être récupéré pour un ID inexistant

    def test_suppression_employe_inexistant(self):
        resultat = self.db.supprimer_employe(999)
        self.assertFalse(resultat)  # La suppression d'un employé inexistant doit échouer

    def test_recuperation_planning_inexistant(self):
        planning = self.db.get_planning(999, '2023-11-01')
        self.assertIsNone(planning)  # Aucun planning ne devrait être récupéré pour un employé et une date inexistant

###################

#### TESTS INTEGRITES DATA
    def test_ajout_planning_pour_employe_inexistant(self):
        resultat = self.db.ajouter_planning(999, '2023-11-01', '09:00', '17:00')
        self.assertFalse(resultat)  # L'ajout de planning pour un employé inexistant doit échouer

    def test_recuperation_employes_pour_role_inexistant(self):
        employes = self.db.get_employes(filtre='role_id = 999')
        self.assertEqual(len(employes), 0)  # Aucun employé ne devrait être récupéré pour un rôle inexistant
###################

#### TESTS SCENARIOS MULTIPLES
    def test_ajout_et_suppression_multiples_employes(self):
        self.db.ajouter_employe('John', 'Doe', '2023-01-01', 'Lundi', 40, 1, 1)
        self.db.ajouter_employe('Jane', 'Smith', '2023-01-01', 'Mardi', 35, 1, 1)
        employes_avant_suppression = self.db.get_employes()
        self.assertEqual(len(employes_avant_suppression), 2)

        self.db.supprimer_employe(1)
        employes_apres_suppression = self.db.get_employes()
        self.assertEqual(len(employes_apres_suppression), 1)

        self.db.supprimer_employe(2)
        employes_apres_deuxieme_suppression = self.db.get_employes()
        self.assertEqual(len(employes_apres_deuxieme_suppression), 0)
###################

#### TESTS PERFORMANCES
    

    def test_performance_ajout_employes(self):
        debut = time.time()
        for i in range(1000):
            self.db.ajouter_employe(f'Nom{i}', f'Prenom{i}', '2023-01-01', 'Lundi', 40, 1, 1)
        fin = time.time()
        print(f'\nTemps pour ajouter 1000 employés : {fin - debut} secondes')
        employes = self.db.get_employes()
        self.assertEqual(len(employes), 1000)  # Vérifie si tous les employés ont été ajoutés
###################

    def tearDown(self):
        # Ferme la connexion à la base de données après chaque test
        self.db.close_connection()

        
if __name__ == '__main__':
    unittest.main()

