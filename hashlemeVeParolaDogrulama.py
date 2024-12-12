import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def main():
    password = input("Enter a password to hash: ")
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")

    password_to_verify = input("Enter a password to verify: ")
    if verify_password(hashed_password, password_to_verify):
        print("Password verified successfully.")
    else:
        print("Invalid password.")

if __name__ == "__main__":
    main()