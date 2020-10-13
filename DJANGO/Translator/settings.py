from django.utils.translation import ugettext_lazy as _


LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

LANGUAGES = (
        ('ar', _('Arabic')),
        ('en', _('English')),
    )

LANGUAGE_CODE = 'en-us'

USE_I18N = True # might be already True
