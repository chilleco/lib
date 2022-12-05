"""
Database ciphers
"""

from .cfg import cfg


# NOTE: ISO 639-1
LOCALES = (
    'en',
    'ru',
    'es',
)
FLAGS = (
    '🇬🇧',
    '🇷🇺',
    '🇪🇸',
)

CURRENCIES = {
    'USD': '$',
    'RUB': '₽',
    'EUR': '€',
    'TRY': '₺',
    'UAH': '₴',
    'THB': '฿',
    'AFN': '؋',
    'AOA': 'Kz',
    'AZN': '₼',
    'BIF': 'FBu',
    'BND': 'B$',
    'BWP': 'P',
    'BYN': 'Br',
    'CDF': 'FC',
    'CNY': '￥',
    'CRC': '₡',
    'DJF': 'Fdj',
    'DKK': 'Kr.',
    'ERN': 'Nfk',
    'ETB': 'Br',
    'GNF': 'FG',
    'GTQ': 'Q',
    'HNL': 'L',
    'HRK': 'T',
    'HUF': 'Ft',
    'IQD': 'دينار',
    'ISK': 'Íkr',
    'JOD': 'د.ا',
    'KGS': 'Лв',
    'KMF': 'CF',
    'KWD': 'د.ك',
    'LYD': 'LYD',
    'MDL': 'L',
    'MGA': 'Ar',
    'MOP': 'MOP$',
    'MWK': 'MK',
    'MZN': 'MT',
    'NAD': 'N$',
    'NIO': 'C$',
    'NOK': 'kr',
    'PGK': 'K',
    'RSD': 'din',
    'SCR': 'SRe',
    'TJS': 'SM',
    'TMT': 'T',
    'YER': '﷼',
    'ZMW': 'ZK',
    'ZWD': 'Z$',
    'VND': '₫',
    'NGN': '₦',
    'COP': 'COL$',
    'BRL': 'R$',
    'ARS': 'ARS$',
    'PEN': 'S/.',
    'ZAR': 'R',
    'MXN': 'Mex$',
    'HKD': '$',
    'GBP': '£',
    'KES': 'KSh',
    'AUD': 'A$',
    'CAD': 'C$',
    'VES': 'Bs',
    'INR': '₹',
    'IDR': 'Rp',
    'KZT': '〒',
    'JPY': '¥',
    'PHP': '₱',
    'TWD': '＄',
    'SAR': 'ر.س',
    'BDT': 'Tk.',
    'EGP': 'E£',
    'AED': 'د.إ',
    'BGN': 'лв',
    'MAD': 'د.م.',
    'PLN': 'zł',
    'PKR': '₨',
    'RON': 'lei',
    'CHF': 'Fr.',
    'CZK': 'Kč',
    'SEK': 'kr',
    'UGX': 'Sh',
    'GHS': 'GH¢',
    'LBP': 'ل.ل',
    'AMD': 'դր.',
    'GEL': '₾',
    'UYU': '$U',
    'CLP': '$',
    'XAF': 'Fr',
    'DZD': 'د.ج',
    'PYG': '₲',
    'BOB': 'Bs.',
    'LKR': 'ரூ',
    'PAB': 'B/.',
    'NZD': '$',
    'KHR': '៛',
    'LAK': '₭',
    'MMK': 'K',
    'DOP': 'RD$',
    'QAR': 'ر.ق',
    'BHD': 'ب.د',
    'OMR': 'ر.ع.',
    'TND': 'د.ت',
    'SDG': '£',
    'MNT': '₮',
    'UZS': "so'm",
    'NPR': 'रु',
    'TZS': 'TSh',
    'XOF': 'FCFA',
    'RWF': 'FRw',
}

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
    'editor', # curator # View reviews
    'verified', # Delete reviews
    'moderator', # Block users
    'admin', # Delete posts
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
