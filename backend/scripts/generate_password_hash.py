import sys

def generate_hash(password: str) -> str:
    pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = input("Digite a senha para gerar o hash: ")
    
    hashed = generate_hash(password)
    print(f"\nHash gerado:")
    print(hashed)
    print(f"\nAdicione ao seu arquivo .env:")
    print(f"ADMIN_PASSWORD_HASH={hashed}")

