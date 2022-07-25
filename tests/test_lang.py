from libdev.lang import get_form, transliterate, to_letters


def test_form():
    assert get_form(1, ('день', 'дня', 'дней')) == 'день'
    assert get_form(0, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(10, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(11, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(12, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(15, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(21, ('день', 'дня', 'дней')) == 'день'
    assert get_form(22, ('день', 'дня', 'дней')) == 'дня'
    assert get_form(25, ('день', 'дня', 'дней')) == 'дней'
    assert get_form(12, ('час', 'часа', 'часов')) == 'часов'
    assert get_form(23, ('час', 'часа', 'часов')) == 'часа'
    assert get_form(101, ('час', 'часа', 'часов')) == 'час'
    assert get_form(-1, ('минута', 'минуты', 'минут')) == 'минута'
    assert get_form(-21, ('минута', 'минуты', 'минут')) == 'минута'
    assert get_form(-22, ('минута', 'минуты', 'минут')) == 'минуты'
    assert get_form(-1012, ('минута', 'минуты', 'минут')) == 'минут'
    assert get_form(-25, ('минута', 'минуты', 'минут')) == 'минут'
    assert get_form(-12, ('минута', 'минуты', 'минут')) == 'минут'

def test_transliterate():
    assert transliterate('Щелкунчик') == 'shchelkunchik'
    assert transliterate(' \tьяНКъы\n') == 'yanky'
    assert transliterate('одежда') == 'odezhda'
    assert transliterate('Пуховики/ Спортивные куртки', separator='-') \
        == 'pukhoviki-sportivnye-kurtki'
    assert transliterate('polos') == 'polos'

def test_to_letters():
    assert to_letters(None) == ''
    assert to_letters('') == ''
    assert to_letters('None') == 'none'
    assert to_letters(' 12\tLa\' tuell  e   \t ') == '12latuelle'
    assert to_letters(' -= ☜☢ Т е к с т \n 0 0 ~ღ ° ˜♥️♉️') == 'текст00'
    assert to_letters('₸ᾟ€‗Ҕ€₵₸ Дêβōчķẳ © хẵῥαķŧéῥổм ҈') == 'дчхм'
    assert to_letters('  [\'Clothing\', \'Shirts & Tops\', \'T Shirts\']\t', separator='-') == 'clothing-shirts-tops-t-shirts'
    assert to_letters('["Clothing", "Shirts & Tops", "T Shirt\'s"]', separator=' ') == 'clothing shirts tops t shirt s'
