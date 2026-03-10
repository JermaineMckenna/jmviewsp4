from pathlib import Path
import os

try:
	import dj_database_url  # type: ignore
except ImportError:
	dj_database_url = None  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")

DEBUG = os.getenv("DEBUG", "False") == "True"

# --- Hosts / Domains ---
# Keep env-driven, but ensure your custom domain + herokuapp are included by default
ALLOWED_HOSTS = [
	h.strip()
	for h in os.getenv(
		"ALLOWED_HOSTS",
		"127.0.0.1,localhost,.herokuapp.com,jmviews.co.uk,www.jmviews.co.uk",
	).split(",")
	if h.strip()
]

# CSRF trusted origins MUST include https origins for your custom domain in production
CSRF_TRUSTED_ORIGINS = [
	o.strip()
	for o in os.getenv(
		"CSRF_TRUSTED_ORIGINS",
		"http://127.0.0.1,http://localhost,"
		"https://*.herokuapp.com,"
		"https://jmviews.co.uk,https://www.jmviews.co.uk",
	).split(",")
	if o.strip()
]

# --- Heroku / Proxy / SSL ---
# Heroku terminates SSL at the router, so Django must trust X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# Only force HTTPS in production
SECURE_SSL_REDIRECT = not DEBUG

# Cookies should be secure in production
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Helpful security headers (safe defaults)
SECURE_HSTS_SECONDS = 0 if DEBUG else 60  # start small; can increase later
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = False  # enable later when you're 100% sure
SECURE_CONTENT_TYPE_NOSNIFF = True

ROOT_URLCONF = "config.urls"

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
"core.middleware.WwwToRootRedirectMiddleware",
"whitenoise.middleware.WhiteNoiseMiddleware",
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

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

if dj_database_url:
	DATABASES = {
		"default": dj_database_url.config(
			default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",  # type: ignore
			conn_max_age=600,
			ssl_require=not DEBUG,  # type: ignore
		)
	}
else:
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

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
	BASE_DIR / "static",
]

STORAGES = {
	"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
	"staticfiles": {
		"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
	},
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "orders:order_list"
LOGOUT_REDIRECT_URL = "core:home"

# --- Stripe ---
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

# Used for Stripe success/cancel URLs
# Default to production domain when DEBUG is False
SITE_URL = os.environ.get("SITE_URL", "http://127.0.0.1:8000" if DEBUG else "https://www.jmviews.co.uk")

STRIPE_CURRENCY = "gbp"