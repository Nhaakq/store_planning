import sqlite3
import json

db_path = 'stores.db'

class StoreDB:
    def __init__(self, db_path):
        try:
            self.__dbconnection = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(f'Error with Sqlite Connexion for {db_path} : {e}')
            
        # CREATE ROLE TABLE
        msg = '''CREATE TABLE IF NOT EXISTS roles(
            id INTEGER PRIMARY KEY,
            nom_role TEXT NOT NULL
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()

        # CREATE USER TABLE
        msg = '''CREATE TABLE IF NOT EXISTS employes(
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            date_entree DATE NOT NULL,
            jour_repos TEXT NOT NULL,
            heures_semaine REAL NOT NULL,
            role_id INTEGER NOT NULL,
            magasin_id INTEGER NOT NULL,
            FOREIGN KEY (role_id) REFERENCES roles(id),
            FOREIGN KEY (magasin_id) REFERENCES magasin(id)
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()

        # CREATE MAGASIN TABLE
        msg = '''CREATE TABLE IF NOT EXISTS magasin(
            id INTEGER PRIMARY KEY,
            nom TEXT NOT NULL,
            adresse TEXT NOT NULL
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()

        # CREATE PLANNING TABLE
        msg = '''CREATE TABLE IF NOT EXISTS planning(
            id INTEGER PRIMARY KEY,
            employe_id INTEGER NOT NULL,
            date DATE NOT NULL,
            heure_debut TIME NOT NULL,
            heure_fin TIME NOT NULL,
            FOREIGN KEY (employe_id) REFERENCES employes(id)
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()

        # CREATE HEURES_SUPPLEMENTAIRES TABLE
        msg = '''CREATE TABLE IF NOT EXISTS heures_supplementaires(
            id INTEGER PRIMARY KEY,
            employe_id INTEGER NOT NULL,
            date DATE NOT NULL,
            heures_travaillees REAL NOT NULL,
            FOREIGN KEY (employe_id) REFERENCES employes(id)
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()

        # CREATE CONGES TABLE
        msg = '''CREATE TABLE IF NOT EXISTS conges(
            id INTEGER PRIMARY KEY,
            employe_id INTEGER NOT NULL,
            date_debut DATE NOT NULL,
            date_fin DATE NOT NULL,
            type_conge TEXT NOT NULL,
            FOREIGN KEY (employe_id) REFERENCES employes(id)
        )'''
        self.__dbconnection.execute(msg)
        self.__dbconnection.commit()


        
    def __del__(self):
        try:
            self.__dbconnection.close()
        except:
            return f"DB connexion does not exist"

    def close_connection(self):
        try:
            self.__dbconnection.close()
            return 'Connexion fermée avec succès.'
        except sqlite3.Error as e:
            return f'Erreur lors de la fermeture de la connexion : {e}'

    def ajouter_employe(self, nom, prenom, date_entree, jour_repos, heures_semaine, role_id, magasin_id):
        if not all((nom, prenom, date_entree, jour_repos, heures_semaine, role_id, magasin_id)):
            return f'Error data are empty or null'

        try:
            self.__dbconnection.execute('''
                INSERT INTO employes (nom, prenom, date_entree, jour_repos, heures_semaine, role_id, magasin_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nom, prenom, date_entree, jour_repos, heures_semaine, role_id, magasin_id))
            self.__dbconnection.commit()
            print('Employé ajouté avec succès.')
        except sqlite3.Error as e:
            print(f'Erreur lors de l\'ajout de l\'employé : {e}')

    def supprimer_employe(self, employe_id):
        try:
            self.__dbconnection.execute('DELETE FROM employes WHERE id = ?', (employe_id,))
            self.__dbconnection.commit()
            # print('Employé supprimé avec succès.')
        except sqlite3.Error as e:
            print(f'Erreur lors de la suppression de l\'employé : {e}')

    def ajouter_planning(self, employe_id, date, heure_debut, heure_fin):
        try:
            self.__dbconnection.execute('''
                INSERT INTO planning (employe_id, date, heure_debut, heure_fin)
                VALUES (?, ?, ?, ?)
            ''', (employe_id, date, heure_debut, heure_fin))
            self.__dbconnection.commit()
            # print('Planning ajouté avec succès.')
        except sqlite3.Error as e:
            print(f'Erreur lors de l\'ajout du planning : {e}')
            
    def get_employes(self, filtre=None):
        try:
            if filtre is None:
                requete = self.__dbconnection.execute('SELECT * FROM employes')
            else:
                # Utilisez le filtre pour personnaliser votre requête SQL
                requete = self.__dbconnection.execute('SELECT * FROM employes WHERE ' + filtre)

            employes = requete.fetchall()
            return employes
        
        except sqlite3.Error as e:
            print(f'Erreur lors de la récupération des employés : {e}')
            return None

    def get_planning(self, employe_id, date):
        try:
            request = self.__dbconnection.execute('SELECT * FROM planning WHERE employe_id = ? AND date = ?', (employe_id, date))
            planning = request.fetchone()
            return planning
        except sqlite3.Error as e:
            print(f'Erreur lors de la récupération du planning : {e}')
            return None

    def ajouter_role(self, nom_role):
        try:
            self.__dbconnection.execute('INSERT INTO roles (nom_role) VALUES (?)', (nom_role,))
            self.__dbconnection.commit()
            print('Rôle ajouté avec succès.')
        except sqlite3.Error as e:
            print(f'Erreur lors de l\'ajout du rôle : {e}')

    def ajouter_magasin(self, nom, adresse):
        try:
            self.__dbconnection.execute('INSERT INTO magasin (nom, adresse) VALUES (?, ?)', (nom, adresse))
            self.__dbconnection.commit()
            print('Magasin ajouté avec succès.')
        except sqlite3.Error as e:
            print(f'Erreur lors de l\'ajout du magasin : {e}')

    def get_roles(self):
        self.__dbconnection.execute('SELECT * FROM roles')
        roles = self.__dbconnection.fetchall()
        return roles

    def get_magasins(self):
        self.__dbconnection.execute('SELECT * FROM magasin')
        magasins = self.__dbconnection.fetchall()
        return magasins

    def import_depuis_json(self, fichier_json):
        with open(fichier_json, 'r') as file:
            data = json.load(file)
            
            for categorie in data:
                if categorie == 'magasin':
                    for mag in data['magasin']:
                        self.ajouter_magasin(
                            mag['nom'], mag['adresse']
                        )
                elif categorie == 'roles':
                    for role in data['roles']:
                        self.ajouter_role(role['nom_role']
                        )
                elif categorie == 'employes':
                    for employe in data['employes']:
                        self.ajouter_employe(
                            employe['nom'], employe['prenom'], employe['date_entree'],
                            employe['jour_repos'], employe['heures_semaine'],
                            employe['role_id'], employe['magasin_id']
                    )

    def get_table_data(self, table_name):
        try:
            query = f"SELECT * FROM {table_name}"
            cursor = self.__dbconnection.execute(query)
            data = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            return column_names, data
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données de la table {table_name}: {e}")
            return None

    def get_tables_list(self):
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='table';"
            cursor = self.__dbconnection.execute(query)
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des données de la liste des tables: {e}")
            return None

if __name__ == '__main__':
    print(StoreDB(db_path).get_employes())