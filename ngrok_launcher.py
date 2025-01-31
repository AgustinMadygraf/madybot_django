"""
Path: run_url_remote.py
"""

from app.components.services.ngrok.ngrok_coordinator import NgrokCoordinator


if __name__ == "__main__":
    coordinator = NgrokCoordinator()
    coordinator.execute()
