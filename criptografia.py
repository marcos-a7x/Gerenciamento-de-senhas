from cryptography.fernet import Fernet
import json
import os


class Crypto:
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()

        self.key = key
        self.cipher = Fernet(self.key)

    def encrypt(self, text):
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt(self, text):
        return self.cipher.decrypt(text.encode()).decode()


class PasswordManager:
    def __init__(self, file="senhas.json"):
        self.file = file
        self.crypto = Crypto()
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                return json.load(f)

        return {}

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_password(self, service, password):
        encrypted = self.crypto.encrypt(password)
        self.data[service] = encrypted
        self.save()
        print("Senha salva com sucesso!")

    def get_password(self, service):
        if service in self.data:
            return self.crypto.decrypt(self.data[service])

        return None

    def list_services(self):
        return list(self.data.keys())

    def remove_password(self, service):
        if service in self.data:
            del self.data[service]
            self.save()


pm = PasswordManager()

while True:
    print("\n1 - Adicionar senha")
    print("2 - Buscar senha")
    print("3 - Listar serviços")
    print("4 - Sair")

    op = input("Escolha: ")

    if op == "1":
        service = input("Serviço: ")
        password = input("Senha: ")
        pm.add_password(service, password)

    elif op == "2":
        service = input("Serviço: ")
        senha = pm.get_password(service)

        if senha:
            print("Senha:", senha)
        else:
            print("Serviço não encontrado.")

    elif op == "3":
        print(pm.list_services())

    elif op == "4":
        break
