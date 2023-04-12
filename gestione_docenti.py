import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def setup_database():
    conn = sqlite3.connect('docenti.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            data_nascita TEXT NOT NULL,
            luogo_nascita TEXT NOT NULL,
            laurea TEXT NOT NULL,
            data_laurea TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schede_servizio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_docente INTEGER NOT NULL,
            anno_scolastico TEXT NOT NULL,
            data_inizio TEXT,
            data_fine TEXT,
            note TEXT,
            FOREIGN KEY (id_docente) REFERENCES docenti (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materie_scheda_servizio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_scheda INTEGER NOT NULL,
            materia TEXT NOT NULL,
            classi TEXT NOT NULL,
            moduli_diurno INTEGER,
            ore_serale INTEGER,
            FOREIGN KEY (id_scheda) REFERENCES schede_servizio (id)
        )
    ''')

    
    conn.commit()
    return conn, cursor

# Utilizza questa riga per creare il database e ottenere gli oggetti conn e cursor
conn, cursor = setup_database()

cursor = conn.cursor()

# Crea le tabelle nel database se non esistono
cursor.execute('''
CREATE TABLE IF NOT EXISTS docenti (
    id INTEGER PRIMARY KEY,
    nome TEXT,
    cognome TEXT,
    data_nascita TEXT,
    luogo_nascita TEXT,
    laurea TEXT,
    data_laurea TEXT
)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS schede_servizio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_docente INTEGER,
        anno_scolastico TEXT,
        data_inizio TEXT,
        data_fine TEXT,
        note TEXT, 
        FOREIGN KEY (id_docente) REFERENCES docenti (id)
    )
''')


conn.commit()

# Funzioni per interagire con il database
def inserisci_docente():
    print("\nInserisci i dati del docente:")

    nome = input("Nome: ")
    cognome = input("Cognome: ")
    data_nascita = input("Data di nascita (GG-MM-AAAA): ")
    luogo_nascita = input("Luogo di nascita: ")
    laurea = input("Laurea in: ")
    data_laurea = input("Data di laurea (GG-MM-AAAA): ")

    cursor.execute('''
    INSERT INTO docenti (nome, cognome, data_nascita, luogo_nascita, laurea, data_laurea)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome, cognome, data_nascita, luogo_nascita, laurea, data_laurea))

    conn.commit()
    print(f"\nDocente {nome} {cognome} inserito con successo.")


def visualizza_docenti():
    cursor.execute("SELECT * FROM docenti")
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print("\nNon ci sono docenti nel database.")
    else:
        print("\nElenco dei docenti:")
        for docente in docenti:
            print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

def cerca_docente(cognome):
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
    else:
        print(f"\nDocenti trovati con il cognome '{cognome}':")
        for docente in docenti:
            print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")


def modifica_docente(cognome):
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
        return

    print(f"\nDocenti trovati con il cognome '{cognome}':")
    for docente in docenti:
        print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    id_docente = int(input("\nInserisci l'ID del docente da modificare: "))
    cursor.execute("SELECT * FROM docenti WHERE id = ?", (id_docente,))
    docente = cursor.fetchone()

    if docente is None:
        print(f"\nNessun docente trovato con l'ID '{id_docente}'.")
        return

    print(f"\nDati del docente (lasciare vuoto per non modificare):")
    print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    nome = input("Nome: ")
    cognome = input("Cognome: ")
    data_nascita = input("Data di nascita (GG-MM-AAAA): ")
    luogo_nascita = input("Luogo di nascita: ")
    laurea = input("Laurea in: ")
    data_laurea = input("Data di laurea (GG-MM-AAAA): ")

    nome = nome if nome != '' else docente[1]
    cognome = cognome if cognome != '' else docente[2]
    data_nascita = data_nascita if data_nascita != '' else docente[3]
    luogo_nascita = luogo_nascita if luogo_nascita != '' else docente[4]
    laurea = laurea if laurea != '' else docente[5]
    data_laurea = data_laurea if data_laurea != '' else docente[6]

    cursor.execute('''
    UPDATE docenti
    SET nome = ?, cognome = ?, data_nascita = ?, luogo_nascita = ?, laurea = ?, data_laurea = ?
    WHERE id = ?
    ''', (nome, cognome, data_nascita, luogo_nascita, laurea, data_laurea, id_docente))

    conn.commit()
    print(f"\nDocente {nome} {cognome} modificato con successo.")

    conn.commit()
    print(f"\nDocente {nome} {cognome} modificato con successo.")


def elimina_docente(cognome):
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
        return

    print(f"\nDocenti trovati con il cognome '{cognome}':")
    for docente in docenti:
        print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    id_docente = int(input("\nInserisci l'ID del docente da eliminare: "))
    cursor.execute("SELECT * FROM docenti WHERE id = ?", (id_docente,))
    docente = cursor.fetchone()

    if docente is None:
        print(f"\nNessun docente trovato con l'ID '{id_docente}'.")
        return

    cursor.execute("DELETE FROM docenti WHERE id = ?", (id_docente,))
    conn.commit()
    print(f"\nDocente {docente[1]} {docente[2]} eliminato con successo.")


def inserisci_scheda_servizio():
    cognome = input("Inserisci il cognome del docente per il quale vuoi inserire una scheda di servizio: ")
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
        return

    print(f"\nDocenti trovati con il cognome '{cognome}':")
    for docente in docenti:
        print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    id_docente = int(input("\nInserisci l'ID del docente per il quale vuoi inserire una scheda di servizio: "))

    anno_scolastico = input("Anno scolastico (es. 2022-2023): ")
    data_inizio_input = input("Data di inizio servizio (GG-MM-AAAA, lascia vuoto se non applicabile): ")
    if data_inizio_input == "":
        data_inizio = None
    else:
        data_inizio = data_inizio_input

    data_fine_input = input("Data di fine servizio (GG-MM-AAAA, lascia vuoto se non applicabile): ")
    if data_fine_input == "":
        data_fine = None
    else:
        data_fine = data_fine_input

    materie = []
    for i in range(1, 6):
        materia = input(f"Materia {i} (lascia vuoto per terminare): ")
        if materia == "":
            break
        classi = input(f"Classi in cui la materia {i} è insegnata (es. 1A, 2B, 3C): ")

        moduli_diurno_input = input(f"Numero di moduli al diurno per la materia {i} (lascia vuoto se non applicabile): ")
        if moduli_diurno_input == "":
            moduli_diurno = None
        else:
            moduli_diurno = int(moduli_diurno_input)

        ore_serale_input = input(f"Numero di ore al serale per la materia {i} (lascia vuoto se non applicabile): ")
        if ore_serale_input == "":
            ore_serale = None
        else:
            ore_serale = int(ore_serale_input)

    materie.append((materia, classi, moduli_diurno, ore_serale))

    note_input = input("Note aggiuntive (lascia vuoto se non applicabile): ")
    if note_input == "":
        note = None
    else:
        note = note_input



    cursor.execute('''
        INSERT INTO schede_servizio (id_docente, anno_scolastico, data_inizio, data_fine, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_docente, anno_scolastico, data_inizio, data_fine, note))

    id_scheda = cursor.lastrowid

    for materia, classi, moduli_diurno, ore_serale in materie:
        cursor.execute('''
            INSERT INTO materie_scheda_servizio (id_scheda, materia, classi, moduli_diurno, ore_serale)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_scheda, materia, classi, moduli_diurno or None, ore_serale or None))

    conn.commit()
    print("\nScheda di servizio inserita con successo.")
    

def modifica_scheda_servizio():
    cognome = input("Inserisci il cognome del docente per il quale vuoi modificare una scheda di servizio: ")
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
        return

    print(f"\nDocenti trovati con il cognome '{cognome}':")
    for docente in docenti:
        print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    id_docente = int(input("\nInserisci l'ID del docente per il quale vuoi modificare una scheda di servizio: "))

    cursor.execute("SELECT * FROM schede_servizio WHERE id_docente=?", (id_docente,))
    schede = cursor.fetchall()

    if len(schede) == 0:
        print(f"\nNessuna scheda di servizio trovata per il docente con ID '{id_docente}'.")
        return

    print(f"\nSchede di servizio trovate per il docente con ID '{id_docente}':")
    for scheda in schede:
        print(f"ID: {scheda[0]}, Anno scolastico: {scheda[2]}, Data di inizio servizio: {scheda[3]}, Data di fine servizio: {scheda[4]}, Note: {scheda[5]}")

    id_scheda = int(input("\nInserisci l'ID della scheda di servizio che vuoi modificare: "))

    anno_scolastico = input("Anno scolastico (es. 2022-2023): ")
    data_inizio = input("Data di inizio servizio (AAAA-MM-GG): ")
    data_fine = input("Data di fine servizio (AAAA-MM-GG): ")
    note = input("Note aggiuntive: ")

    cursor.execute('''
        UPDATE schede_servizio
        SET anno_scolastico=?, data_inizio=?, data_fine=?, note=?
        WHERE id=?
    ''', (anno_scolastico, data_inizio, data_fine, note, id_scheda))

    conn.commit()
    print("\nScheda di servizio modificata con successo.")


def elimina_scheda_servizio():
    cognome = input("Inserisci il cognome del docente per il quale vuoi eliminare una scheda di servizio: ")
    cursor.execute("SELECT * FROM docenti WHERE cognome LIKE ?", (f"%{cognome}%",))
    docenti = cursor.fetchall()

    if len(docenti) == 0:
        print(f"\nNessun docente trovato con il cognome '{cognome}'.")
        return

    print(f"\nDocenti trovati con il cognome '{cognome}':")
    for docente in docenti:
        print(f"ID: {docente[0]}, Nome: {docente[1]}, Cognome: {docente[2]}, Data di nascita: {docente[3]}, Luogo di nascita: {docente[4]}, Laurea in: {docente[5]}, Data di laurea: {docente[6]}")

    id_docente = int(input("\nInserisci l'ID del docente per il quale vuoi eliminare una scheda di servizio: "))

    cursor.execute("SELECT * FROM schede_servizio WHERE id_docente=?", (id_docente,))
    schede = cursor.fetchall()

    if len(schede) == 0:
        print(f"\nNessuna scheda di servizio trovata per il docente con ID '{id_docente}'.")
        return

    print(f"\nSchede di servizio trovate per il docente con ID '{id_docente}':")
    for scheda in schede:
        print(f"ID: {scheda[0]}, Anno scolastico: {scheda[2]}, Data di inizio servizio: {scheda[3]}, Data di fine servizio: {scheda[4]}, Note: {scheda[5]}")

    id_scheda = int(input("\nInserisci l'ID della scheda di servizio che vuoi eliminare: "))

    cursor.execute("DELETE FROM materie_scheda_servizio WHERE id_scheda=?", (id_scheda,))
    cursor.execute("DELETE FROM schede_servizio WHERE id=?", (id_scheda,))

    conn.commit()
    print("\nScheda di servizio eliminata con successo.")


def stampa_nomina():
    pass

def stampa_certificato_servizio(id_docente):
    pass  # Aggiungi il codice per generare la stampa dei certificati di servizio utilizzando reportlab

# Menu principale
def main():
    while True:
        print("\nMenu:")
        print("1. Inserisci un nuovo docente")
        print("2. Visualizza tutti i docenti")
        print("3. Cerca un docente per cognome")
        print("4. Modifica un docente per cognome")
        print("5. Elimina un docente per cognome")
        print("6. Inserisci una scheda di servizio")
        print("7. Modifica una scheda di servizio")
        print("8. Elimina una scheda di servizio")
        print("9. Stampa nomina")
        print("10. Esci")



        scelta = input("Seleziona un'opzione: ")

        if scelta == "1":
            inserisci_docente()
        elif scelta == "2":
            visualizza_docenti()
        elif scelta == "3":
            cognome = input("Inserisci il cognome del docente: ")
            cerca_docente(cognome)
        elif scelta == "4":
            cognome = input("Inserisci il cognome del docente da modificare: ")
            modifica_docente(cognome)
        elif scelta == "5":
            cognome = input("Inserisci il cognome del docente da eliminare: ")
            elimina_docente(cognome)
        elif scelta == "6":
            inserisci_scheda_servizio()
        elif scelta == "7":
            modifica_scheda_servizio()
        elif scelta == "8":
            elimina_scheda_servizio()
        elif scelta == "9":
            stampa_nomina()
        elif scelta == "10":
            print("Arrivederci!")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

# Ricorda di chiudere la connessione al database alla fine del programma
conn.close()
