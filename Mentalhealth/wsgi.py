"""
WSGI config for Mentalhealth project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Usage
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mentalhealth.settings')

application = get_wsgi_application()
