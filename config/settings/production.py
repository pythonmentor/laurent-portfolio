"""
Project: mysite

Production configuration.

For more information, the complete list of configuration variables is available in the official documentation here:
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import pymysql

from .base import *  # noqa: F403
from .base import env

# GENERAL
# SECURITY WARNING: The secret key used in production is a sensitive value.
# https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-SECRET_KEY
SECRET_KEY = env("DJANGO_SECRET_KEY")

# DEBUG: Ensure it is False in production
DEBUG = False

# ALLOWED HOSTS
# A list of strings representing domain/host names that this Django site can serve.
# It’s a security measure to prevent HTTP Host header attacks, which are possible even
# with many seemingly secure web server configurations.
# https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")

# DATABASE:
# A dictionary containing the settings for all databases to be used with Django.
# The DATABASES setting must configure a default database; you can define as many additional databases as needed.
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# This database configuration uses an environment variable in URL form named DJANGO_DATABASE_URL.
# Examples of such configuration URLs are:
# - POSTGRESQL: postgres://USER:PASSWORD@HOST:PORT/DB_NAME (with psycopg driver)
# - MYSQL: mysql://USER:PASSWORD@HOST:PORT/DB_NAME (with mysqlclient driver)
# - SQLITE: sqlite:///FILE_NAME (driver included by default in Python)
DATABASES = {"default": env.db("DJANGO_DATABASE_URL")}

# CONN_MAX_AGE is used in a Django production configuration to set how long database connections are reused,
# which improves performance by reducing the overhead of creating new connections for each request.
DATABASES["default"]["CONN_MAX_AGE"] = env.int(
    "DJANGO_DB_CONN_MAX_AGE", default=60
)

# If the database engine is MySQL, the following configuration settings are
# applied to ensure that the database connection uses the utf8mb4 character set.
if "mysql" in DATABASES["default"]["ENGINE"]:
    pymysql.install_as_MySQLdb()
    DATABASES["default"]["OPTIONS"] = {
        "charset": "utf8mb4",
        "init_command": "SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci', sql_mode='STRICT_TRANS_TABLES'",
    }

# SECURITY
# The SECURE_PROXY_SSL_HEADER variable is used in Django to indicate that the application is behind a reverse proxy
# (such as Nginx or a load balancer) that handles the SSL protocol.
# By setting SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https"), we specify that Django should treat requests
# with the HTTP_X_FORWARDED_PROTO header as secure if they are marked with the value "https".
# This allows Django to properly handle these requests as being made over HTTPS, even if the connection between
# Django and the proxy is over HTTP.
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# The SECURE_SSL_REDIRECT variable configures Django to automatically redirect all HTTP requests to HTTPS.
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)  # type: ignore

# The SESSION_COOKIE_SECURE = True variable ensures that session cookies are only sent over HTTPS connections,
# enhancing security by preventing their transmission over unsecured connections.
# https://docs.djangoproject.com/en/5.1/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# The SESSION_COOKIE_NAME = "__Secure-sessionid" variable allows for setting a custom name for the session cookie,
# and the __Secure- prefix is often used to indicate that this cookie should only be sent over HTTPS connections.
# https://docs.djangoproject.com/en/5.1/ref/settings/#session-cookie-name
SESSION_COOKIE_NAME = "__Secure-sessionid"

# The CSRF_COOKIE_SECURE = True variable ensures that the CSRF cookie (used for protection against CSRF attacks)
# is only transmitted over HTTPS connections, enhancing security against attacks on unsecured connections.
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# The CSRF_COOKIE_NAME = "__Secure-csrftoken" variable customizes the name of the CSRF cookie,
# and the __Secure- prefix is used to indicate that the cookie should only be sent over HTTPS,
# following best security practices for sensitive cookies.
# https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "__Secure-csrftoken"

# The SECURE_HSTS_SECONDS = 60 variable activates the HTTP Strict Transport Security (HSTS) policy for 60 seconds,
# telling browsers to exclusively use HTTPS connections for the site during this time,
# enhancing security by preventing downgrades to HTTP.
# https://docs.djangoproject.com/en/5.1/topics/security/#ssl-https
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-seconds
# TODO: Set this value to 60 seconds first, then to 518400 once you have confirmed that the initial value works.
SECURE_HSTS_SECONDS = 60

# The SECURE_HSTS_INCLUDE_SUBDOMAINS variable indicates whether the HSTS policy (HTTP Strict Transport Security)
# should also apply to all subdomains of the site. Setting this via an environment variable, defaulting to True here,
# ensures that all requests to subdomains are also forced to use HTTPS, enhancing security across the entire domain.
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,  # type: ignore
)

# The SECURE_HSTS_PRELOAD variable, when set to True, allows the domain to be included in the HSTS preload list.
# This means that browsers supporting this feature will refuse any HTTP connection right from the first visit,
# enhancing security by avoiding attacks before even the first unsecured HTTP request.
# https://docs.djangoproject.com/en/5.1/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)  # type: ignore

# The SECURE_CONTENT_TYPE_NOSNIFF variable, enabled here by default through an environment variable,
# adds the HTTP X-Content-Type-Options: nosniff header to responses.
# This header prevents browsers from guessing the content type and handling it differently from what is specified,
# which enhances security by preventing certain attacks, such as those related to misinterpreted file types (MIME type sniffing).
# https://docs.djangoproject.com/en/5.1/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True,  # type: ignore
)


# EMAIL
# Email configuration. By default, emails are displayed in the terminal.
# To set up an email backend, define the DJANGO_EMAIL_URL environment variable with the following values:
# - SMTP with SSL: smtp+ssl://USER:PASSWORD@HOST:PORT
# - SMTP with STARTTLS: smtp+tls://USER:PASSWORD@HOST:PORT
# - Console: consolemail://
# https://docs.djangoproject.com/en/5.1/ref/settings/
EMAIL_CONFIG = env.email(
    "DJANGO_EMAIL_URL",
    default="consolemail://",  # type: ignore
)
globals().update(**EMAIL_CONFIG)

# The DEFAULT_FROM_EMAIL variable defines the default email address used by Django to send emails from the application.
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="mysite <noreply@eu.pythonanywhere.com>",  # type: ignore
)

# The SERVER_EMAIL variable defines the email address used to send error or alert messages originating from the Django server,
# such as 500 error notifications.
# https://docs.djangoproject.com/en/5.1/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# The EMAIL_SUBJECT_PREFIX variable adds a custom prefix to the subject of all emails sent by the Django application.
# https://docs.djangoproject.com/en/5.1/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Laurent] ",  # type: ignore
)

# ADMIN
# The ADMIN_URL variable defines the custom URL for accessing the Django admin interface.
# Configuring it via an environment variable helps obscure or make the admin URL less predictable (instead of the default /admin/ URL),
# enhancing security by reducing the risk of automated attacks targeting the admin interface.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")


# Logging
# https://docs.djangoproject.com/en/5.1/ref/settings/#logging
# See https://docs.djangoproject.com/en/5.1/topics/logging/
# for more details on customizing logging configuration.
# A sample logging configuration. The only concrete logging action this configuration performs
# is sending an email to site admins on every HTTP 500 error when DEBUG=False.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "mail_admins"],
            "propagate": True,
        },
    },
}

# Wagtail settings

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = env("DJANGO_WAGTAILADMIN_BASE_URL")
