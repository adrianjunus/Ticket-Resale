import os
import secrets

# Generate a random secret key
secret_key = secrets.token_hex(32)

# Create a .env file if it doesn’t exist
env_path = ".env"
if not os.path.exists(env_path):
    with open(env_path, "w") as f:
        f.write(f"SECRET_KEY={secret_key}\n")
    print(f"✅ Generated new SECRET_KEY and saved to {env_path}")
else:
    print("ℹ️ .env file already exists. Skipping secret key generation.")

# Notify user to proceed with installation
print("\n Setup done! Please run the following:")
print("1) Create & activate a virtual environment")
print("2) Install dependencies: pip install -r requirements.txt")
print("3) Run the Flask app: python run.py")