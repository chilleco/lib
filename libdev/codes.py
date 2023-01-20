"""
Database ciphers
"""

from .cfg import cfg


# NOTE: ISO 639-1
LOCALES = (
    'en',
    'ru',
    'zh',
    'es',
    'de',
    'fr',
    'ja',
    'pt',
    'it',
    'pl',
    'tr',
    'nl',
    'cs',
    'ko',
    'vi',
)
FLAGS = (
    '🇬🇧',  # 🇺🇸
    '🇷🇺',
    '🇨🇳',
    '🇪🇸',
    '🇩🇪',
    '🇫🇷',
    '🇯🇵',
    '🇵🇹',
    '🇮🇹',
    '🇵🇱',
    '🇹🇷',
    '🇳🇱',
    '🇨🇿',
    '🇰🇷',
    '🇻🇳',
)

NETWORKS = (
    '', # Console
    'web', # Web-interface
    'tg', # Telegram
    'vk', # VKontakte
    'g', # Google
    'fb', # Facebook
    'a', # Apple
    'in', # LinkedIn
    'ig', # Instagram
)

STATUSES = (
    'removed',
    'disabled',
    'active',
)
USER_STATUSES = (
    'removed', # deleted # not specified # Does not exist
    'blocked', # archive # Does not have access to resources
    'guest', # normal
    'authorized', # registered # confirmed # Save personal data & progress
    'editor', # curator # View reviews, add verified posts
    'verified', # Delete reviews, edit posts, add categories
    'moderator', # View & block users, delete posts, edit & delete categories
    'admin', # Change permissions
    'owner', # Can't be blocked
)


default_locale = cfg('locale', 0)


def get_network(code):
    """ Get network code by cipher """

    if code is None:
        return 0

    if code in NETWORKS:
        return NETWORKS.index(code)

    if code in range(len(LOCALES)):
        return code

    return 0

def get_locale(code):
    """ Get language code by cipher """

    if code is None:
        return default_locale

    if code in LOCALES:
        return LOCALES.index(code)

    if code in range(len(LOCALES)):
        return code

    return default_locale

def get_flag(code):
    """ Get flag by language """
    return FLAGS[get_locale(code)]
