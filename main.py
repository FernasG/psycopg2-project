from database import DatabaseMananger
from datetime import datetime

if __name__ == "__main__":
    manager = DatabaseMananger()

    migrations = manager.find("SELECT * FROM public.migrations")
    for migration in migrations:
        _, timestamp, name = migration
        timestamp = datetime.fromtimestamp(timestamp / 1e3).strftime("%d/%m/%Y %H:%M")

        print(f"{name} - {timestamp}")

    manager.close()

