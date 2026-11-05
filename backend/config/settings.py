
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --------------------------------
# BASIC DJANGO SETTINGS
# --------------------------------

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    x.strip()
    for x in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if x.strip()
]

# --------------------------------
# CORS AND CSRF SETTINGS
# --------------------------------

CORS_ALLOWED_ORIGINS = [
    x.strip()
    for x in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if x.strip()
]

CSRF_TRUSTED_ORIGINS = [
    x.strip()
    for x in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if x.strip()
]

# --------------------------------
# INSTALLED APPS
# --------------------------------

INSTALLED_APPS = [
    "corsheaders",

    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "mobility",
]

# --------------------------------
# MIDDLEWARE
# --------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------------------
# URL AND TEMPLATE SETTINGS
# --------------------------------

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "mobility.context_processors.global_site_theme",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --------------------------------
# DATABASE AND AIVEN MYSQL SSL
# --------------------------------

DB_SSL_CA = os.getenv("DB_SSL_CA", "certificates/ca.pem")
DB_SSL_CA_PATH = Path(DB_SSL_CA)

if not DB_SSL_CA_PATH.is_absolute():
    DB_SSL_CA_PATH = BASE_DIR / DB_SSL_CA

if os.getenv("DB_ENGINE", "sqlite").lower() == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "ntts_mobility"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "ssl": {
                    "ca": str(DB_SSL_CA_PATH),
                },
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --------------------------------
# PASSWORD VALIDATION
# --------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
]

# --------------------------------
# LANGUAGE AND TIME ZONE
# --------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# --------------------------------
# STATIC AND MEDIA FILES
# --------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------------
# LOGIN AND LOGOUT
# --------------------------------

LOGIN_REDIRECT_URL = "/cms/"
LOGOUT_REDIRECT_URL = "/cms/login/"

# --------------------------------
# WHATSAPP SETTINGS
# --------------------------------

WHATSAPP_OWNER_NUMBER = os.getenv("WHATSAPP_OWNER_NUMBER", "")

# --------------------------------
# BREVO EMAIL API SETTINGS
# --------------------------------

BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "")

# --------------------------------
# CUSTOMER EMAIL OTP SETTINGS
# --------------------------------

CUSTOMER_OTP_EXPIRY_SECONDS = 300
CUSTOMER_OTP_RESEND_SECONDS = 60
