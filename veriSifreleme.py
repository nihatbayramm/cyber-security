from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import base64

class AESCipher:
    def __init__(self, password: str, salt: bytes = None):
        self.backend = default_backend()
        self.salt = salt if salt else os.urandom(16)
        self.key = self._derive_key(password, self.salt)

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=self.backend
        )
        return kdf.derive(password.encode())

    def encrypt(self, plaintext: str) -> dict:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return {
            "ciphertext": base64.b64encode(ciphertext).decode(),
            "iv": base64.b64encode(iv).decode(),
            "salt": base64.b64encode(self.salt).decode()
        }

    def decrypt(self, ciphertext: str, iv: str, salt: str) -> str:
        self.key = self._derive_key(password, base64.b64decode(salt))
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(base64.b64decode(iv)), backend=self.backend)
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()
        return decrypted.decode()

def main():
    print("AES Encryption & Decryption Utility")
    password = input("Enter encryption password: ").strip()
    aes = AESCipher(password)
    
    data = input("Enter the data to encrypt: ").strip()
    encrypted_data = aes.encrypt(data)
    print(f"\nEncrypted Data: {encrypted_data['ciphertext']}")
    print(f"IV: {encrypted_data['iv']}")
    print(f"Salt: {encrypted_data['salt']}")

    print("\n--- Decryption ---")
    enc_ciphertext = input("Enter ciphertext: ").strip()
    enc_iv = input("Enter IV: ").strip()
    enc_salt = input("Enter Salt: ").strip()

    decrypted_data = aes.decrypt(enc_ciphertext, enc_iv, enc_salt)
    print(f"Decrypted Data: {decrypted_data}")

if __name__ == "__main__":
    main()