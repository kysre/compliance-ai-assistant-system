import os

import dj_database_url

from compliance_ai_assistant.settings.base import *  # NOQA

DEBUG = False

ALLOWED_HOSTS = []
ALLOWED_HOSTS.extend(
    filter(
        None,
        os.environ.get("ALLOWED_HOSTS", "").split(","),
    )
)

DATABASES["default"] = dj_database_url.parse(os.environ["DATABASE_URL"])

CORS_ALLOWED_ORIGINS = []
