import os  # isort:skip

gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))
"""
Django settings for bportal project.

Generated by 'django-admin startproject' using Django 1.11.22.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

# import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')5i6!m4(j5=)m1b3%n^o&wz-0$%j)m7^=*%@v_$(2-q-!2l3xq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition





ROOT_URLCONF = 'bportal.urls'

DATE_INPUT_FORMATS = ['%m/%d/%Y']
DATE_FORMAT = "%m/%d/%Y"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bportal', 'static'),
)
SITE_ID = 1


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'bportal', 'templates'), os.path.join(BASE_DIR, 'templates'),],
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',
                'django.template.context_processors.tz',
                'sekizai.context_processors.sekizai',
                'django.template.context_processors.static',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai'
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ],
        },
    },
]


MIDDLEWARE = [
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware'
]

SESSION_EXPIRY_TIME = 1800

INSTALLED_APPS = [
    'djangocms_admin_style',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'formtools',
    'cms',
    'menus',
    'sekizai',
    'treebeard',
    'djangocms_text_ckeditor',
    'filer',
    'easy_thumbnails',
    'djangocms_column',
    'djangocms_file',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_style',
    'djangocms_snippet',
    'djangocms_googlemap',
    'djangocms_video',
    # local
    'bportal',
    'core.apps.CoreConfig',
    'form_application.apps.FormApplicationConfig',
    'apps_cms_integration.apps.AppsCmsIntegrationConfig',
    'employer.apps.EmployerConfig',
    'healthquestionaire.apps.HealthquestionaireConfig',

    # third party
    'django_s3_storage',
    'storages',
    'django_filters',
    'django_tables2',
    'crudbuilder'
]

LOGIN_REDIRECT_URL = 'login_success'
LOGOUT_REDIRECT_URL = '/accounts/login/?toolbar_off'

LANGUAGES = (
    ## Customize this
    ('en', gettext('en')),
)

CMS_LANGUAGES = {
    ## Customize this
    'default': {
        'hide_untranslated': False,
        'public': True,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'hide_untranslated': False,
            'public': True,
            'redirect_on_fallback': True,
            'code': 'en',
            'name': gettext('en'),
        },
    ],
}

CMS_TEMPLATES = (
    ## Customize this
    ('fullwidth.html', 'Fullwidth'),
    ('sidebar_left.html', 'Sidebar Left'),
    ('sidebar_right.html', 'Sidebar Right')
)

CMS_PERMISSION = True

CMS_PLACEHOLDER_CONF = {}

# DATABASES = {
#     'default': {
#         'CONN_MAX_AGE': 0,
#         'ENGINE': 'django.db.backends.sqlite3',
#         'HOST': 'localhost',
#         'NAME': 'project.db',
#         'PASSWORD': '',
#         'PORT': '',
#         'USER': ''
#     }
# }

WSGI_APPLICATION = 'bportal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': "cms_benefits_dev_db",
        'USER': "cms_benefits_db",
        'PASSWORD': "PERstVLO6",
        'HOST': "cms-benefits-dev-db.crk7fkrxykmu.us-west-2.rds.amazonaws.com",
        'PORT': 5432,
        'CONN_MAX_AGE': 500
    }
}


MIGRATION_MODULES = {
    
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

# YOUR_S3_BUCKET = "zappa-cms-static"

# STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
# AWS_S3_BUCKET_NAME_STATIC = YOUR_S3_BUCKET

# # These next two lines will serve the static files directly 
# # from the s3 bucket
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % YOUR_S3_BUCKET
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# AWS_S3_MEDIA_DIR = '%s.s3.amazonaws.com/media/submitted' % YOUR_S3_BUCKET

# AWS_S3_PDF_TEMPLATE_DIR = '%s.s3.amazonaws.com/media/pdf-templates' % YOUR_S3_BUCKET
# S3_MEDIA_URL = "https://%s/" % AWS_S3_MEDIA_DIR
# S3_TEMPLATE_URL = "https://%s/" % AWS_S3_PDF_TEMPLATE_DIR
# OR...if you create a fancy custom domain for your static files use:
#AWS_S3_PUBLIC_URL_STATIC = "https://static.zappaguide.com/"

AWS_DEFAULT_ACL = 'public-read'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_bportal"),
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn", "static_root")


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn", "media_root")

AWS_ACCESS_KEY_ID = os.environ["DJANGO_AWSACCESSKEYID"]
AWS_SECRET_ACCESS_KEY = os.environ["DJANGO_AWSSECRETACCESSKEY"]
AWS_STORAGE_BUCKET_NAME = 'zappa-cms-static'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static'
AWS_STATIC_LOCATION = 'static_cdn'
AWS_PUBLIC_MEDIA_LOCATION = 'media/submitted'
AWS_PRIVATE_MEDIA_LOCATION = 'private_media_cdn'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

AWS_S3_MEDIA_CDN = "https://%s/media_cdn/" % (AWS_S3_CUSTOM_DOMAIN)

DEFAULT_FILE_STORAGE = 'bportal.storage_backends.PublicMediaStorage'

# PREFIX_URL = '/dev/'
PREFIX_URL = '/'
DOWNLOAD_URL = '/sss-file/'