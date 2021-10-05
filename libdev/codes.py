"""
Database ciphers
"""

# NOTE: ISO 639-1
LOCALES = (
    'en',
    'ru',
    'es',
)

NETWORKS = (
    '', # Console
    'web', # Web-interface
    'tg', # Telegram
    'vk', # VKontakte
    'g', # Google
    'fb', # Facebook
    'a', # Apple
)

USER_STATUSES = (
    'deleted', # not specified # Does not exist
    'blocked', # archive # Does not have access to resources
    'normal', # guest
    'registered', # confirmed # Save personal data & progress
    'editor', # curator # View reviews
    'verified', # Delete reviews
    'moderator', # Block users
    'admin', # Delete posts
    'owner', # Can't be blocked
)


def get_network(code):
    """ Get network code by cipher """

    if code is None:
        return 0

    if code in NETWORKS:
        return NETWORKS.index(code)

    if code in range(len(LOCALES)):
        return code

    return 0

def get_language(code):
    """ Get language code by cipher """

    if code is None:
        return None

    if code in LOCALES:
        return LOCALES.index(code)

    if code in range(len(LOCALES)):
        return code

    return None
