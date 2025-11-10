#!/usr/bin/env python3
import os
import subprocess

SECRETS_DIR = "secrets"
GPG_ID = "gadgetsaavy"  # ← your GPG identity

def get_path(service, key):
    return os.path.join(SECRETS_DIR, service, f"{key}.gpg")

def add_secret():
    service = input("🔧 Service name: ").strip()
    key = input("🔑 Secret name: ").strip()
    value = input("📝 Secret value: ").strip()

    os.makedirs(os.path.join(SECRETS_DIR, service), exist_ok=True)
    proc = subprocess.run(
        ["gpg", "--encrypt", "--armor", "-r", GPG_ID],
        input=value,
        text=True,
        capture_output=True
    )
    if proc.returncode == 0:
        with open(get_path(service, key), "w") as f:
            f.write(proc.stdout)
        print(f"✅ Secret saved: {service}/{key}")
    else:
        print(f"❌ Encryption failed:\n{proc.stderr}")

def remove_secret():
    service = input("🔧 Service name: ").strip()
    key = input("🔑 Secret name: ").strip()
    path = get_path(service, key)
    if os.path.exists(path):
        os.remove(path)
        print(f"🗑️ Removed: {service}/{key}")
    else:
        print(f"⚠️ Secret not found: {service}/{key}")

def list_secrets():
    print("📂 Stored secrets:")
    for root, _, files in os.walk(SECRETS_DIR):
        for file in files:
            if file.endswith(".gpg"):
                rel_path = os.path.relpath(os.path.join(root, file), SECRETS_DIR)
                print(f"🔐 {rel_path[:-4]}")  # remove .gpg

def decrypt_secret():
    service = input("🔧 Service name: ").strip()
    key = input("🔑 Secret name: ").strip()
    path = get_path(service, key)
    if not os.path.exists(path):
        print(f"⚠️ Secret not found: {service}/{key}")
        return

    proc = subprocess.run(
        ["gpg", "--decrypt", "--pinentry-mode", "loopback", path],
        capture_output=True,
        text=True
    )

    if proc.returncode == 0:
        print(f"🔓 Decrypted value:\n{proc.stdout.strip()}")
    else:
        print(f"❌ Decryption failed:\n{proc.stderr}")


def main():
    while True:
        print("\n🔒 GPG Secret Manager")
        print("1️⃣ Add secret")
        print("2️⃣ Remove secret")
        print("3️⃣ List secrets")
        print("4️⃣ Decrypt secret")
        print("5️⃣ Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_secret()
        elif choice == "2":
            remove_secret()
        elif choice == "3":
            list_secrets()
        elif choice == "4":
            decrypt_secret()
        elif choice == "5":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
