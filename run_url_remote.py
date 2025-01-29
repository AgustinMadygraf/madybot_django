"""
Path: run_url_remote.py

"""

from app.core_services.url_service import UrlService
from app.core_config.flask_config import FlaskConfig

flask_config = FlaskConfig()
config = flask_config.get_config()
url_ENDPOINT_NGROK_PHP = config['ENDPOINT_NGROK_PHP']
url_service = UrlService(url_ENDPOINT_NGROK_PHP)
url = url_service.get_public_url()
url_service.save_url(url)
print(url)
