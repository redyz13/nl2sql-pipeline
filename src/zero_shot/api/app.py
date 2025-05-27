import connexion
from zero_shot.config.config import APP_ENV

app = connexion.App(__name__, specification_dir=".")
app.env = APP_ENV
app.add_api("openapi.json")

print(f"\033[92m[BOOT]\033[0m App running in \033[1m{APP_ENV.upper()}\033[0m mode")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
