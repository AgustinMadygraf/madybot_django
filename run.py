"""
Path: run.py
Punto de entrada para iniciar la aplicación Flask.
"""

from app.core_launcher.server_launcher import ServerLauncher

if __name__ == '__main__':
    server = ServerLauncher()
    server.register_blueprints()
    server.run()
