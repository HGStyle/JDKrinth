import sqlite3
import sys
import os

if __name__ != "__main__":
    sys.exit()

print("JDKrinth - a database editor to force Modrinth to use a certain Java version")
print("Created by HGStyle - https://github.com/HGStyle/JDKrinth")
print("Free and open-source software released under the MIT license - https://mit-license.org/")

def exit(c):
    input('Press enter to exit...')
    sys.exit(c)

if not os.path.exists(r'C:\Users\hgsty\AppData\Roaming\ModrinthApp\app.db'):
    if os.name != 'nt':
        print('Sorry, this program only supports Windows for now. Open an issue on GitHub and we will try to add support for your OS if you help us a little. https://github.com/HGStyle/JDKrinth')
        exit(2)
    else:
        print('Sorry, you are not using the latest version of Modrinth. Please update and transfer all your data manually, then use this software.')
        exit(2)

db = sqlite3.connect(r'C:\Users\hgsty\AppData\Roaming\ModrinthApp\app.db')

arch = db.execute('SELECT architecture FROM java_versions LIMIT 1').fetchmany()
if not arch:
    print('Sorry, you need to install atleast one default Java installation inside Modrinth to continue.')
    exit(2)
else:
    arch = arch[0][0]

while True:
    print('==================================================')
    print('Scanning for JDKs known to Modrinth...')
    sql = db.execute('SELECT full_version, path FROM java_versions')
    jdk = sql.fetchmany()
    while jdk:
        print(f"Found Java {jdk[0][0]} at {jdk[0][1]}")
        jdk = sql.fetchmany()
    action = input('What should we do ? (i/d/e/q) -> ')
    while action not in "ideq":
        print('Please enter a valid action.')
        print(' - "i" for insert')
        print(' - "d" for delete')
        print(' - "e" or "q" for exit/quit')
        action = input('What should we do ? (i/d/e/q) -> ')
    if action == "i":
        major = input('Enter major Java version (example: 17) -> ')
        full = input('Enter full Java version (example: 17.0.12) -> ')
        while major not in full or not(major.isdigit()):
            print('Sorry, but the major version should be a number that is inclued inside the full version name.')
            major = input('Enter major Java version (example: 17) -> ')
            full = input('Enter full Java version (example: 17.0.12) -> ')
        path = input('Enter Java executable path (example: C:\\Program Files\\Oracle\\Java\\bin\\java.exe) -> ')
        path = (path[::-1].replace('java.exe'[::-1], 'javaw.exe'[::-1], 1))[::-1]
        while not os.path.isfile(path):
            print('Sorry, but this executable does not exists, or the Java version you wanna use does not provide a background service (JavaW).')
            path = input('Enter Java executable path (example: C:\\Program Files\\Oracle\\Java\\bin\\java.exe) -> ')
            path = (path[::-1].replace('java.exe'[::-1], 'javaw.exe'[::-1], 1))[::-1]
        with db:
            try:
                db.execute(f"INSERT INTO java_versions (major_version, full_version, architecture, path) VALUES (?, ?, ?, ?)", (major, full, arch, path))
            except sqlite3.IntegrityError:
                print(f'Sorry, you firstly have to delete the old row using Java major version {major}.')
        print("Successfully added Java entry inside Modrinth's application data !")
    elif action == "d":
        info = input('Enter an exact information to delete one or multiple entries -> ')
        with db:
            db.execute('DELETE FROM java_versions WHERE major_version = ? OR full_version = ? OR path = ?', (info, info, info))
        print("Successfully removed Java entry inside Modrinth's application data !")
    else:
        print('Saving...')
        db.commit()
        db.close()
        print('Exiting...')
        sys.exit(0)
