import compression


def test1():
    alg = compression.Algorythm()
    string_to_check = 'abcdefghijklmnopqrstuvwxyz' \
                      'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                      'абвгдеёжзийклмнопрстуфхцчшщьыъэюя' \
                      'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ' \
                      '0123456789'
    encoded_string = '00000000000001000001000000110000100000010100001100000111000100000010010001010000101100011000001101000111000011110010000001000100100100010011001010000101010010110001011100110000011001001101000110110011100001110100111100011111010000001000010100010010001101001000100101010011001001110101000010100101010100101011010110001011010101110010111101100000110001011001001100110110100011010101101100110111011100001110010111010011101101111000111101011111001111111000000100000110000101000011100010010001011000110100011110010001001001100101010010111001100100110110011101001111101000010100011010010101001110101001010101101011010101111011000101100110110101011011101110010111011011110101111111000001100001110001011000111100100110010111001101100111110100011010011101010110101111011001101101110111011011111110000111000111100101110011111010011101011110110111011111110001111001111101011110111111100111110111111101111111'
    result = alg.compress_str(string_to_check, False)
    table_of_codes = alg.table_of_codes

    assert result == encoded_string
