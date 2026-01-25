from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")

# Treat missing DEBUG env var as True (dev safe)
DEBUG = os.environ.get("DEBUG", "").lower() not in ("0", "false", "no")

# Always provide allowed hosts even in dev
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Optional env extension: ALLOWED_HOSTS="example.com,.herokuapp.com"
env_hosts = os.environ.get("ALLOWED_HOSTS", "")
if env_hosts:ALLOWED_HOSTS += [h.strip() for h in env_hosts.split(",") if h.strip()]

INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",
"core",
"accounts",
"orders",
]

MIDDLEWARE = [
"django.middleware.security.SecurityMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
"BACKEND": "django.template.backends.django.DjangoTemplates",
"DIRS": [BASE_DIR / "templates"],
"APP_DIRS": True,
"OPTIONS": {
"context_processors": [
"django.template.context_processors.debug",
"django.template.context_processors.request",
"django.contrib.auth.context_processors.auth",
"django.contrib.messages.context_processors.messages",
],
},
},
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
"default": {
"ENGINE": "django.db.backends.sqlite3",
"NAME": BASE_DIR / "db.sqlite3",
}
}

AUTH_PASSWORD_VALIDATORS = [
{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media (for file uploads: deliverables)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "orders:order_list"
LOGOUT_REDIRECT_URL = "core:home"