"""
Database ciphers
"""

from .cfg import cfg


# NOTE: ISO 639-1
LOCALES = (
    "en",  # English (UK) / English
    "ru",  # Russian / Русский
    "zh",  # Chinese / 中文
    "es",  # Spanish / Español
    "de",  # German / Deutsch
    "fr",  # French / Français
    "ja",  # Japanese / 日本語
    "pt",  # Portuguese / Português
    "it",  # Italian / Italiano
    "pl",  # Polish / Polski
    "tr",  # Turkish / Türkçe
    "nl",  # Dutch / Nederlands
    "cs",  # Czech / Čeština
    "ko",  # Korean / 한국어
    "vi",  # Vietnamese / Việt ngữ
    "fa",  # Persian / فارسی
    "ar",  # Arabic / العربية
    "el",  # Greek / Ελληνικά
    "hu",  # Hungarian / Magyar
    "sv",  # Swedish / Svenska
    "ro",  # Romanian / Română
    "sk",  # Slovak / Slovenčina
    "id",  # Indonesian / Bahasa Indonesia
    "da",  # Danish / Dansk
    "th",  # Thai / ไทย
    "fi",  # Finnish / Suomi
    "bg",  # Bulgarian / Български език
    "uk",  # Ukrainian / Українська
    "he",  # Hebrew / עברית
    "no",  # Norwegian / Norsk
    # 'nb',  # Norwegian (Bokmål)
    "hr",  # Croatian / Hrvatski jezik
    "sr",  # Serbian / Српски језик
    "lt",  # Lithuanian / Lietuvių kalba
    "sl",  # Slovenian (Slovene) / Slovenščina
    # 'nn',  # Norwegian (Nynorsk)
    "ca",  # Catalan / Català
    "lv",  # Latvian / Latviešu valoda
    "hi",  # Hindi / हिन्दी
    "et",  # Estonian / Eesti keel
    "az",  # Azerbaijani / Azərbaycan dili
    "so",  # Somali / Af Soomaali
    "af",  # Afrikaans / Afrikaans
    # Malaysian Malay / Bahasa Malaysia
    "ms",  # Malay / Bahasa Melayu
    "jv",  # Javanese / Basa Jawa
    "su",  # Sundanese / Basa Sunda
    "bs",  # Bosnian / Bosanski jezik
    "ny",  # Chichewa / Chichewa
    "cy",  # Welsh / Cymraeg
    "eo",  # Esperanto / Esperanto
    "eu",  # Basque / Euskara
    "ga",  # Irish / Gaeilge
    "gl",  # Galician / Galego
    "xh",  # Xhosa / isiXhosa
    "zu",  # Zulu / isiZulu
    "is",  # Icelandic / Íslenska
    "sw",  # Swahili / Kiswahili
    "ht",  # Haitian Creole / Kreyòl Ayisyen
    "ku",  # Kurdish / Kurdî
    "la",  # Latin / Latīna
    "lb",  # Luxembourgish / Lëtzebuergesch
    "mg",  # Malagasy / Malagasy
    "mt",  # Maltese / Malti
    "mi",  # Maori / Māori
    "uz",  # Uzbek / O'zbek tili
    # Sesotho / Sesotho
    "sq",  # Albanian / Shqip
    "tl",  # Tagalog / Tagalog
    "tt",  # Tatar / Tatarça
    "yo",  # Yoruba / Yorùbá
    "be",  # Belarusian / Беларуская мова
    "ky",  # Kyrgyz / Кыр
    "kk",  # Kazakh / Қазақ тілі
    "mk",  # Macedonian / Македонски јазик
    "mn",  # Mongolian / Монгол хэл
    "tg",  # Tajik / Тоҷикӣ
    "ka",  # Georgian / ქართული
    "hy",  # Armenian / Հայերեն
    "yi",  # Yiddish / ייִדיש
    "ug",  # Uyghur / ئۇيغۇرچە
    "ur",  # Urdu / اردو
    "ps",  # Pashto / پښتو
    "ne",  # Nepali / नेपाली
    "mr",  # Marathi / मराठी
    "bn",  # Bengali / বাংলা
    "pa",  # Punjabi / ਪੰਜਾਬੀ
    "gu",  # Gujarati / ગુજરાતી
    "or",  # Oriya / ଓଡ଼ିଆ
    "ta",  # Tamil / தமிழ்
    "te",  # Telugu / తెలుగు
    "kn",  # Kannada / ಕನ್ನಡ
    "ml",  # Malayalam / മലയാളം
    "si",  # Sinhala / සිංහල
    "lo",  # Lao / ພາສາລາວ
    "my",  # Burmese / ဗမာစာ
    "km",  # Khmer / ភាសាខ្មែរ
    # 'aa',  # Afar
    # 'ab',  # Abkhazian
    # 'ae',  # Avestan
    # 'ak',  # Akan
    # 'am',  # Amharic
    # 'an',  # Aragonese
    # 'as',  # Assamese
    # 'av',  # Avaric
    # 'ay',  # Aymara
    # 'ba',  # Bashkir
    # 'bh',  # Bihari languages
    # 'bi',  # Bislama
    # 'bm',  # Bambara
    # 'bo',  # Tibetan
    # 'br',  # Breton
    # 'ce',  # Chechen
    # 'ch',  # Chamorro
    # 'co',  # Corsican
    # 'cr',  # Cree
    # 'cu',  # Church Slavic; Old Slavonic; Church Slavonic;
    # Old Bulgarian; Old Church Slavonic
    # 'cv',  # Chuvash
    # 'dv',  # Divehi; Dhivehi; Maldivian
    # 'dz',  # Dzongkha
    # 'ee',  # Ewe
    # 'ff',  # Fulah
    # 'fj',  # Fijian
    # 'fo',  # Faroese
    # 'fy',  # Western Frisian
    # 'gd',  # Gaelic; Scottish Gaelic
    # 'gn',  # Guarani
    # 'gv',  # Manx
    # 'ha',  # Hausa
    # 'ho',  # Hiri Motu
    # 'hz',  # Herero
    # 'ia',  # Interlingua (International Auxiliary Language Association)
    # 'ie',  # Interlingue; Occidental
    # 'ig',  # Igbo
    # 'ii',  # Sichuan Yi; Nuosu
    # 'ik',  # Inupiaq
    # 'io',  # Ido
    # 'iu',  # Inuktitut
    # 'kg',  # Kongo
    # 'ki',  # Kikuyu; Gikuyu
    # 'kj',  # Kuanyama; Kwanyama
    # 'kl',  # Kalaallisut; Greenlandic
    # 'kr',  # Kanuri
    # 'ks',  # Kashmiri
    # 'kv',  # Komi
    # 'kw',  # Cornish
    # 'lg',  # Ganda
    # 'li',  # Limburgan; Limburger; Limburgish
    # 'ln',  # Lingala
    # 'lu',  # Luba-Katanga
    # 'mh',  # Marshallese
    # 'na',  # Nauru
    # 'nd',  # Ndebele, North; North Ndebele
    # 'ng',  # Ndonga
    # 'nr',  # Ndebele, South; South Ndebele
    # 'nv',  # Navajo; Navaho
    # 'oc',  # Occitan (post 1500)
    # 'oj',  # Ojibwa
    # 'om',  # Oromo
    # 'os',  # Ossetian; Ossetic
    # 'pi',  # Pali
    # 'qu',  # Quechua
    # 'rm',  # Romansh
    # 'rn',  # Rundi
    # 'rw',  # Kinyarwanda
    # 'sa',  # Sanskrit
    # 'sc',  # Sardinian
    # 'sd',  # Sindhi
    # 'se',  # Northern Sami
    # 'sg',  # Sango
    # 'sm',  # Samoan
    # 'sn',  # Shona
    # 'ss',  # Swati
    # 'st',  # Sotho, Southern
    # 'ti',  # Tigrinya
    # 'tk',  # Turkmen
    # 'tn',  # Tswana
    # 'to',  # Tonga (Tonga Islands)
    # 'ts',  # Tsonga
    # 'tw',  # Twi
    # 'ty',  # Tahitian
    # 've',  # Venda
    # 'vo',  # Volapük
    # 'wa',  # Walloon
    # 'wo',  # Wolof
    # 'za',  # Zhuang; Chuang
    # 'us',  # English (US) / English
    # 'zh',  # Traditional Chinese / 繁體中文
)
FLAGS = (
    "🇬🇧",  # English (UK) / English
    "🇷🇺",  # Russian / Русский
    "🇨🇳",  # Chinese / 中文
    "🇪🇸",  # Spanish / Español
    "🇩🇪",  # German / Deutsch
    "🇫🇷",  # French / Français
    "🇯🇵",  # Japanese / 日本語
    "🇵🇹",  # Portuguese / Português
    "🇮🇹",  # Italian / Italiano
    "🇵🇱",  # Polish / Polski
    "🇹🇷",  # Turkish / Türkçe
    "🇳🇱",  # Dutch / Nederlands
    "🇨🇿",  # Czech / Čeština
    "🇰🇷",  # Korean / 한국어
    "🇻🇳",  # Vietnamese / Việt ngữ
    "🇮🇷",  # Persian / فارسی
    "🇦🇪",  # Arabic / العربية # TODO: by country
    "🇬🇷",  # Greek / Ελληνικά
    "🇭🇺",  # Hungarian / Magyar
    "🇸🇪",  # Swedish / Svenska
    "🇷🇴",  # Romanian / Română
    "🇸🇰",  # Slovak / Slovenčina
    "🇮🇩",  # Indonesian / Bahasa Indonesia
    "🇩🇰",  # Danish / Dansk
    "🇹🇭",  # Thai / ไทย
    "🇫🇮",  # Finnish / Suomi
    "🇧🇬",  # Bulgarian / Български език
    "🇺🇦",  # Ukrainian / Українська
    "🇮🇱",  # Hebrew / עברית
    "🇳🇴",  # Norwegian / Norsk
    # '🇳🇴',  # Norwegian (Bokmål)
    "🇭🇷",  # Croatian / Hrvatski jezik
    "🇷🇸",  # Serbian / Српски језик
    "🇱🇹",  # Lithuanian / Lietuvių kalba
    "🇸🇮",  # Slovenian (Slovene) / Slovenščina
    # '🇳🇴',  # Norwegian (Nynorsk)
    "🇦🇩",  # Catalan / Català
    "🇱🇻",  # Latvian / Latviešu valoda
    "🇮🇳",  # Hindi / हिन्दी
    "🇪🇪",  # Estonian / Eesti keel
    "🇦🇿",  # Azerbaijani / Azərbaycan dili
    "🇸🇴",  # Somali / Af Soomaali
    "🇿🇦",  # Afrikaans / Afrikaans # FIXME
    # Malaysian Malay / Bahasa Malaysia
    "🇲🇾",  # Malay / Bahasa Melayu
    "🇮🇩",  # Javanese / Basa Jawa
    "🇮🇩",  # Sundanese / Basa Sunda
    "🇧🇦",  # Bosnian / Bosanski jezik
    "🇲🇼",  # Chichewa / Chichewa
    "🏴󠁧󠁢󠁷󠁬󠁳󠁿",  # Welsh / Cymraeg
    "🏳️",  # Esperanto / Esperanto # FIXME
    "🇪🇸",  # Basque / Euskara
    "🇮🇪",  # Irish / Gaeilge
    "🇪🇸",  # Galician / Galego
    "🇿🇦",  # Xhosa / isiXhosa # FIXME
    "🇿🇦",  # Zulu / isiZulu
    "🇮🇸",  # Icelandic / Íslenska
    "🇹🇿",  # Swahili / Kiswahili
    "🇭🇹",  # Haitian Creole / Kreyòl Ayisyen
    "🇮🇶",  # Kurdish / Kurdî # FIXME
    "🏳️",  # Latin / Latīna # FIXME
    "🇱🇺",  # Luxembourgish / Lëtzebuergesch
    "🇲🇬",  # Malagasy / Malagasy
    "🇲🇹",  # Maltese / Malti
    "🇳🇿",  # Maori / Māori
    "🇺🇿",  # Uzbek / O'zbek tili
    # Sesotho / Sesotho
    "🇦🇱",  # Albanian / Shqip
    "🇵🇭",  # Tagalog / Tagalog
    "🇷🇺",  # Tatar / Tatarça
    "🇳🇬",  # Yoruba / Yorùbá
    "🇧🇾",  # Belarusian / Беларуская мова
    "🇰🇬",  # Kyrgyz / Кыр
    "🇰🇿",  # Kazakh / Қазақ тілі
    "🇲🇰",  # Macedonian / Македонски јазик
    "🇲🇳",  # Mongolian / Монгол хэл
    "🇹🇯",  # Tajik / Тоҷикӣ
    "🇬🇪",  # Georgian / ქართული
    "🇦🇲",  # Armenian / Հայերեն
    "🇮🇱",  # Yiddish / ייִדיש # FIXME
    "🇨🇳",  # Uyghur / ئۇيغۇرچە
    "🇵🇰",  # Urdu / اردو
    "🇦🇫",  # Pashto / پښتو
    "🇳🇵",  # Nepali / नेपाली
    "🇮🇳",  # Marathi / मराठी
    "🇧🇩",  # Bengali / বাংলা
    "🇵🇰",  # Punjabi / ਪੰਜਾਬੀ
    "🇮🇳",  # Gujarati / ગુજરાતી
    "🇮🇳",  # Oriya / ଓଡ଼ିଆ
    "🇮🇳",  # Tamil / தமிழ்
    "🇮🇳",  # Telugu / తెలుగు
    "🇮🇳",  # Kannada / ಕನ್ನಡ
    "🇮🇳",  # Malayalam / മലയാളം
    "🇱🇰",  # Sinhala / සිංහල
    "🇱🇦",  # Lao / ພາສາລາວ
    "🇲🇲",  # Burmese / ဗမာစာ
    "🇰🇭",  # Khmer / ភាសាខ្មែរ
    # '🇺🇸',  # English (US) / English
    # '🇨🇳',  # Traditional Chinese / 繁體中文
)

NETWORKS = (
    "",  # Console
    "web",  # Web-interface
    "tg",  # Telegram
    "vk",  # VKontakte
    "g",  # Google
    "fb",  # Facebook
    "a",  # Apple
    "in",  # LinkedIn
    "ig",  # Instagram
)

STATUSES = (
    "removed",
    "disabled",
    "active",
)
USER_STATUSES = (
    "removed",  # deleted # not specified # Does not exist
    "blocked",  # archive # Does not have access to resources
    "guest",  # normal
    "authorized",  # registered # confirmed # Save personal data & progress
    "editor",  # curator # View reviews, add verified posts
    "verified",  # Delete reviews, edit posts, add categories
    "moderator",  # View & block users, delete posts, edit & delete categories
    "admin",  # Change permissions
    "owner",  # Can't be blocked
)
DEFAULT_LOCALE = LOCALES.index(cfg("locale", "en"))


def get_network(code):
    """Get network code by cipher"""

    if code is None:
        return 0

    if code in NETWORKS:
        return NETWORKS.index(code)

    if code in range(len(LOCALES)):
        return code

    return 0


def get_locale(code):
    """Get language code by cipher"""

    if code is None:
        return DEFAULT_LOCALE

    if code in LOCALES:
        return LOCALES.index(code)

    if code in range(len(LOCALES)):
        return code

    return DEFAULT_LOCALE


def get_flag(code):
    """Get flag by language"""
    return FLAGS[get_locale(code)]
