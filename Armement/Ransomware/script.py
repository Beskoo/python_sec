from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import shutil

# Fonction pour afficher un message
def print_message(message):
    print(f"\n--- {message} ---\n")

# Étape 1: Créer une clé privée et dériver la clé publique
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Étape 2: Sauvegarder les clés dans des fichiers distincts
with open("private_key.pem", "wb") as private_key_file:
    private_key_file.write(private_key)

with open("public_key.pem", "wb") as public_key_file:
    public_key_file.write(public_key)

print_message("Clés générées et sauvegardées")

# Étape 3: Parcourir le répertoire de test, copier son arborescence et chiffrer son contenu
source_directory = "Armement"
destination_directory = "Armement_chiffre"

if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Génération de la clé symétrique (AES)
symmetric_key = os.urandom(32)

# Chiffrement de la clé symétrique avec la clé publique RSA
rsa_key = RSA.import_key(open("public_key.pem").read())
cipher_rsa = PKCS1_OAEP.new(rsa_key)
encrypted_symmetric_key = cipher_rsa.encrypt(symmetric_key)

# Sauvegarde de la clé symétrique chiffrée
with open("encrypted_symmetric_key.bin", "wb") as key_file:
    key_file.write(encrypted_symmetric_key)

print_message("Clé symétrique générée et chiffrée avec succès")

for root, dirs, files in os.walk(source_directory):
    for file in files:
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(file_path, source_directory)
        destination_path = os.path.join(destination_directory, relative_path)

        with open(file_path, "rb") as original_file:
            data = original_file.read()

        # Chiffrement du fichier avec la clé symétrique
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(os.urandom(16)), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()

        with open(destination_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

print_message("Chiffrement terminé")

# Étape 4: Déchiffrer un fichier test
file_to_decrypt = "Armement_chiffre/fichier_a_chiffrer.txt"
with open(file_to_decrypt, "rb") as encrypted_file:
    encrypted_data = encrypted_file.read()

# Déchiffrement de la clé symétrique avec la clé privée RSA
cipher_rsa = PKCS1_OAEP.new(key)
symmetric_key = cipher_rsa.decrypt(encrypted_symmetric_key)

# Déchiffrement du fichier avec la clé symétrique
cipher = Cipher(algorithms.AES(symmetric_key), modes.CFB(os.urandom(16)), backend=default_backend())
decryptor = cipher.decryptor()
decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

decrypted_file_path = "Armement_dechiffre/fichier_a_dechiffrer.txt"
with open(decrypted_file_path, "wb") as decrypted_file:
    decrypted_file.write(decrypted_data)

print_message("Déchiffrement terminé")
