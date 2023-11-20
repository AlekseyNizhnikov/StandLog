import sqlite3
from threading import Thread

class DataBase(Thread):
    def __init__(self) -> None:
        self.connect = sqlite3.connect("Stands.db")
        self.cursor = self.connect.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Stands(
                                                                stand_id INT PRIMARY KEY,
                                                                number_stand TEXT,
                                                                name_stand TEXT,
                                                                invent_number INT,
                                                                factory_number INT,
                                                                storage_place TEXT,
                                                                responsible TEXT,
                                                                user TEXT,
                                                                team TEXT,
                                                                name_create TEXT,
                                                                name_client TEXT,
                                                                army TEXT,
                                                                version_stand INT,
                                                                software TEXT,
                                                                version_software TEXT,
                                                                date_of_creation TEXT);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Documentation(
                                                                doc_id INT PRIMARY KEY,
                                                                stand_id INT,
                                                                data BLOB);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS RepairStands(
                                                                repair_stand_id INT PRIMARY KEY,
                                                                stand_id INT,
                                                                number_stand TEXT,
                                                                name_stand TEXT,
                                                                invent_number INT,
                                                                factory_number INT,
                                                                storage_place TEXT,
                                                                user TEXT,
                                                                team TEXT,
                                                                delivery_date TEXT);""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CheckStands(
                                                                check_stand_id INT PRIMARY KEY,
                                                                stand_id INT,
                                                                number_protocol INT,
                                                                number_stand TEXT,
                                                                name_stand TEXT,
                                                                invent_number INT,
                                                                factory_number INT,
                                                                data_next_check TEXT,
                                                                boss_metrology  TEXT,
                                                                boss_quality  TEXT,
                                                                metrologist TEXT,
                                                                note TEXT,
                                                                suitability TEXT,
                                                                data_check TEXT);""")   
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS CancelStands(
                                                                cancel_id INT PRIMARY KEY,
                                                                name_stand TEXT,
                                                                number_protocol INT,
                                                                number_stand TEXT,
                                                                invent_number INT,
                                                                factory_number INT,
                                                                bottom TEXT);""")
        
        self.connect.commit()


if __name__ == "__main__":
    DataBase()
            