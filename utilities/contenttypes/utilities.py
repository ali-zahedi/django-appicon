from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

_CONTENT_TYPE_DICTIONARY = {}
_CONTENT_TYPE_ID = []
_CONTENT_TYPE_WHITE_LIST_DICTIONARY = {}
_CONTENT_TYPE_WHITE_LIST_ID = []


def get_content_type():
    """
    Return the User model that is active in this project.
    """
    CONTENT_TYPE_MODEL = 'contenttypes.ContentType'
    try:
        return django_apps.get_model(CONTENT_TYPE_MODEL, require_ready=False)
    except LookupError:
        raise ImproperlyConfigured(
            "ContentType refers to model '%s' that has not been installed" % CONTENT_TYPE_MODEL
        )


ContentType = get_content_type()


def _fetch_white_list_data():
    try:
        global _CONTENT_TYPE_WHITE_LIST_ID, _CONTENT_TYPE_WHITE_LIST_DICTIONARY
        if not _CONTENT_TYPE_WHITE_LIST_DICTIONARY:
            items = [
                # Whitelist
                ContentType.objects.get(app_label='files', model='filemodel'),
                ContentType.objects.get(app_label='links', model='link'),
                ContentType.objects.get(app_label='shops', model='package'),
                ContentType.objects.get(app_label='courses', model='course'),
                ContentType.objects.get(app_label='courses', model='section'),
                ContentType.objects.get(app_label='courses', model='activity'),
                ContentType.objects.get(app_label='blog', model='post'),
                ContentType.objects.get(app_label='segments', model='page'),
                ContentType.objects.get(app_label='slides', model='slide'),
                ContentType.objects.get(app_label='language_dictionaries', model='dictionary'),
            ]
            _CONTENT_TYPE_WHITE_LIST_DICTIONARY = {item.model_class().__name__: item.pk for item in items}
            _CONTENT_TYPE_WHITE_LIST_ID = list(_CONTENT_TYPE_WHITE_LIST_DICTIONARY.values())
    except:
        pass


def _fetch_data():
    _fetch_white_list_data()
    try:
        def ignore_it(app):
            blacklist = [
                'admin', 'auth', 'django', 'contenttypes', 'sessions', 'otp', 'device',
                'push', 'content', 'azbankgateways', 'bank',
            ]
            for item in blacklist:
                if app.app_label.find(item) >= 0:
                    return True
                if app.model.find(item) >= 0:
                    return True
            return False

        global _CONTENT_TYPE_DICTIONARY, _CONTENT_TYPE_ID
        if not _CONTENT_TYPE_DICTIONARY:
            for item in ContentType.objects.all():
                if ignore_it(item) or not item.model_class():
                    continue
                _CONTENT_TYPE_DICTIONARY[item.model_class().__name__] = item.pk
            _CONTENT_TYPE_DICTIONARY.update(_CONTENT_TYPE_WHITE_LIST_DICTIONARY)
            _CONTENT_TYPE_ID = list(_CONTENT_TYPE_DICTIONARY.values())
    except:
        pass


def get_content_type_white_list_id():
    _fetch_white_list_data()
    global _CONTENT_TYPE_WHITE_LIST_ID
    return _CONTENT_TYPE_WHITE_LIST_ID


def get_content_type_dictionary():
    _fetch_data()
    global _CONTENT_TYPE_DICTIONARY
    return _CONTENT_TYPE_DICTIONARY


def get_content_type_from_model(cls):
    return ContentType.objects.get_for_model(cls)
