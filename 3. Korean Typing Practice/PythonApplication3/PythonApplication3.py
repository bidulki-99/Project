_CHO_ = 'ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ'
_JUNG_ = 'ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ'
_JONG_ = 'ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ' # index를 1부터 시작해야 함

# 겹자음 : 'ㄳ', 'ㄵ', 'ㄶ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ'
# 겹모음 : 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ'

_JAMO2ENGKEY_ = {
 'ㄱ': 'r',
 'ㄲ': 'R',
 'ㄴ': 's',
 'ㄷ': 'e',
 'ㄸ': 'E',
 'ㄹ': 'f',
 'ㅁ': 'a',
 'ㅂ': 'q',
 'ㅃ': 'Q',
 'ㅅ': 't',
 'ㅆ': 'T',
 'ㅇ': 'd',
 'ㅈ': 'w',
 'ㅉ': 'W',
 'ㅊ': 'c',
 'ㅋ': 'z',
 'ㅌ': 'x',
 'ㅍ': 'v',
 'ㅎ': 'g',
 'ㅏ': 'k',
 'ㅐ': 'o',
 'ㅑ': 'i',
 'ㅒ': 'O',
 'ㅓ': 'j',
 'ㅔ': 'p',
 'ㅕ': 'u',
 'ㅖ': 'P',
 'ㅗ': 'h',
 'ㅘ': 'hk',
 'ㅙ': 'ho',
 'ㅚ': 'hl',
 'ㅛ': 'y',
 'ㅜ': 'n',
 'ㅝ': 'nj',
 'ㅞ': 'np',
 'ㅟ': 'nl',
 'ㅠ': 'b',
 'ㅡ': 'm',
 'ㅢ': 'ml',
 'ㅣ': 'l',
 'ㄳ': 'rt',
 'ㄵ': 'sw',
 'ㄶ': 'sg',
 'ㄺ': 'fr',
 'ㄻ': 'fa',
 'ㄼ': 'fq',
 'ㄽ': 'ft',
 'ㄾ': 'fx',
 'ㄿ': 'fv',
 'ㅀ': 'fg',
 'ㅄ': 'qt'
}

def is_hangeul_syllable(ch):
    '''한글 음절인지 검사
    '''
    if not isinstance(ch, str):
        return False
    elif len(ch) > 1:
        ch = ch[0]
    
    return 0xAC00 <= ord(ch) <= 0xD7A3

def compose(cho, jung, jong):
    '''초성, 중성, 종성을 한글 음절로 조합
    cho : 초성
    jung : 중성
    jong : 종성
    return value: 음절
    '''
    if not (0 <= cho <= 18 and 0 <= jung <= 20 and 0 <= jong <= 27):
        return None
    code = (((cho * 21) + jung) * 28) + jong + 0xAC00

    return chr(code)

def decompose(syll):
    '''한글 음절을 초성, 중성, 종성으로 분해
    syll : 한글 음절
    return value : tuple of integers (초성, 중성, 종성)
    '''
    if not is_hangeul_syllable(syll):
        return (None, None, None)
    
    uindex = ord(syll) - 0xAC00
    
    jong = uindex % 28
    jung = ((uindex - jong) // 28) % 21
    cho = ((uindex - jong) // 28) // 21

    return (cho, jung, jong)

def str2jamo(str):
    '''문자열을 자모 문자열로 변환
    '''
    jamo = []
    for ch in str:
        if is_hangeul_syllable(ch):
            cho, jung, jong = decompose(ch)
            jamo.append( _CHO_[cho])
            jamo.append( _JUNG_[jung])
            if jong != 0:
                jamo.append( _JONG_[jong-1])
        else:
            jamo.append(ch)
    return ''.join(jamo)

def jamo2engkey(str):

    engkey = []
    for ch in str:
        if ch not in _JAMO2ENGKEY_:
            engkey.append(ch)
        else:
            engkey.append(_JAMO2ENGKEY_[ch])
    return ''.join(engkey)

def engkey2jamo(str):

    _REVERSE_JAMO2ENGKEY_ = {}
    jamo = []
    for key, value in _JAMO2ENGKEY_.items():
        _REVERSE_JAMO2ENGKEY_[value] = key

    for ch in str:
        if ch not in _REVERSE_JAMO2ENGKEY_:
            jamo.append(ch)
        else:
            jamo.append(_REVERSE_JAMO2ENGKEY_[ch])
    return ''.join(jamo)

def jamo2syllable(str):

    _REVERSE_JAMO2ENGKEY_ = {}
    for key, value in _JAMO2ENGKEY_.items():
        _REVERSE_JAMO2ENGKEY_[value] = key

    syllable = []
    cur = []
    rem = []
    for ch in str:

        if ch not in _JAMO2ENGKEY_:
            if not cur:
                syllable.append(ch)
            else:
                rem = remain_cur(cur)
                for i in rem:
                    syllable.append(i)
                cur = []
                syllable.append(ch)

        else:
            cur.append(ch)

            if len(cur) == 1:
                continue


            elif len(cur) == 2:

                if cur[0] in _CHO_ and cur[1] in _CHO_:
                    engkey = jamo2engkey(cur[0] + cur[1])

                    if engkey in _REVERSE_JAMO2ENGKEY_:
                        continue

                    else:
                        syllable.append(cur[0])
                        del cur[0]

                elif cur[0] in _CHO_ and cur[1] in _JUNG_:
                    continue

                elif cur[0] in _JUNG_ and cur[1] in _CHO_:
                    syllable.append(cur[0])
                    del cur[0]

                elif cur[0] in _JUNG_ and cur[1] in _JUNG_:
                    engkey = jamo2engkey(cur[0] + cur[1])

                    if engkey in _REVERSE_JAMO2ENGKEY_:
                        jung = _REVERSE_JAMO2ENGKEY_[engkey]
                        syllable.append(jung)
                        del cur[0:2]

                    else:
                        syllable.append(cur[0])
                        del cur[0]


            elif len(cur) == 3:

                if cur[0] in _CHO_ and cur[1] in _CHO_:

                    if cur[2] in _CHO_:
                        engkey = jamo2engkey(cur[0] + cur[1])
                        jong = _REVERSE_JAMO2ENGKEY_[engkey]
                        syllable.append(jong)
                        del cur[0:2]

                    elif cur[2] in _JUNG_:
                        syllable.append(cur[0])
                        del cur[0]

                elif cur[0] in _CHO_ and cur[1] in _JUNG_:

                    if cur[2] in _CHO_:
                        continue

                    elif cur[2] in _JUNG_:
                        engkey = jamo2engkey(cur[1] + cur[2])

                        if engkey in _REVERSE_JAMO2ENGKEY_:
                            continue

                        else:
                            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                            syllable.append(han)
                            del cur[0:2]


            elif len(cur) == 4:

                if cur[2] in _CHO_ and cur[3] in _JUNG_:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                    syllable.append(han)
                    del cur[0:2]

                elif cur[2] in _CHO_ and cur[3] in _CHO_:
                    engkey = jamo2engkey(cur[2] + cur[3])

                    if engkey in _REVERSE_JAMO2ENGKEY_:
                        continue

                    else:

                        if cur[2] in _JONG_:
                            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(cur[2]) + 1)
                            syllable.append(han)
                            del cur[0:3]

                        else:
                            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                            syllable.append(han)
                            syllable.append(cur[2])
                            del cur[0:3]

                elif cur[2] in _JUNG_ and cur[3] in _CHO_:
                    continue

                elif cur[2] in _JUNG_ and cur[3] in _JUNG_:
                    engkey = jamo2engkey(cur[1] + cur[2])

                    if engkey in _REVERSE_JAMO2ENGKEY_:
                        jung = _REVERSE_JAMO2ENGKEY_[engkey]
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                        syllable.append(han)
                        del cur[0:3]

                    else:
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                        syllable.append(han)
                        del cur[0:2]


            elif len(cur) == 5:

                if cur[2] in _CHO_ and cur[3] in _CHO_ and cur[4] in _CHO_:
                    engkey = jamo2engkey(cur[2] + cur[3])
                    jong = _REVERSE_JAMO2ENGKEY_[engkey]
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(jong) + 1)
                    syllable.append(han)
                    del cur[0:4]

                elif cur[2] in _CHO_ and cur[3] in _CHO_ and cur[4] in _JUNG_:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(cur[2]) + 1)
                    syllable.append(han)
                    del cur[0:3]

                elif cur[2] in _JUNG_ and cur[3] in _CHO_ and cur[4] in _CHO_:
                    continue

                elif cur[2] in _JUNG_ and cur[3] in _CHO_ and cur[4] in _JUNG_:
                    continue


            elif len(cur) == 6:

                engkey1 = jamo2engkey(cur[1] + cur[2])
                jung = _REVERSE_JAMO2ENGKEY_[engkey1]

                if cur[4] in _CHO_ and cur[5] in _CHO_:
                    engkey2 = jamo2engkey(cur[3] + cur[4])

                    if engkey2 in _REVERSE_JAMO2ENGKEY_:
                        jong = _REVERSE_JAMO2ENGKEY_[engkey2]
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(jong) + 1)
                        syllable.append(han)
                        del cur[0:5]

                    else:
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(cur[3]) + 1)
                        syllable.append(han)
                        syllable.append(cur[4])
                        del cur[0:5]

                elif cur[4] in _CHO_ and cur[5] in _JUNG_:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(cur[3]) + 1)
                    syllable.append(han)
                    del cur[0:4]

                elif cur[4] in _JUNG_ and cur[5] in _CHO_:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                    syllable.append(han)
                    del cur[0:3]

                elif cur[4] in _JUNG_ and cur[5] in _JUNG_:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                    engkey2 = jamo2engkey(cur[4] + cur[5])

                    if engkey2 in _REVERSE_JAMO2ENGKEY_:
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                        syllable.append(han)
                        del cur[0:3]

                    else:
                        han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                        syllable.append(han)
                        han = compose(_CHO_.index(cur[3]), _JUNG_.index(cur[4]), 0)
                        syllable.append(han)
                        syllable.append(cur[5])
                        del cur[0:6]

    rem = remain_cur(cur)
    for i in rem:
        syllable.append(i)

    return ''.join(syllable)

def remain_cur(cur):

    _REVERSE_JAMO2ENGKEY_ = {}
    for key, value in _JAMO2ENGKEY_.items():
        _REVERSE_JAMO2ENGKEY_[value] = key

    syllable = []

    if len(cur) == 1:
        syllable.append(cur[0])
         

    elif len(cur) == 2:

        if cur[0] in _CHO_ and cur[1] in _JUNG_:
            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
            syllable.append(han)

        elif cur[0] in _CHO_ and cur[1] in _CHO_:
            engkey = jamo2engkey(cur[0] + cur[1])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                syllable.append(_REVERSE_JAMO2ENGKEY_[engkey])

            else:
                syllable.append(cur[0])
                syllable.append(cur[1])

        elif cur[0] in _JUNG_ and cur[1] in _CHO_:
            syllable.append(_CHO_.index(cur[0]))
            syllable.append(_CHO_.index(cur[1]))

        elif cur[0] in _JUNG_ and cur[1] in _JUNG_:
            engkey = jamo2engkey(cur[0] + cur[1])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                syllable.append(_REVERSE_JAMO2ENGKEY_[engkey])

            else:
                syllable.append(cur[0])
                syllable.append(cur[1])


    elif len(cur) == 3:

        if cur[2] in _CHO_:
            if cur[2] in _JONG_:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(cur[2]) + 1)
                syllable.append(han)

            else:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                syllable.append(han)
                syllable.append(cur[2])

        elif cur[2] in _JUNG_:
            engkey = jamo2engkey(cur[1] + cur[2])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                jung = _REVERSE_JAMO2ENGKEY_[engkey]
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                syllable.append(han)

            else:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                syllable.append(han)
                syllable.append(cur[2])



    elif len(cur) == 4:

        if cur[2] in _CHO_ and cur[3] in _CHO_:
            engkey = jamo2engkey(cur[2] + cur[3])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                jong = _REVERSE_JAMO2ENGKEY_[engkey]
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(jong) + 1)
                syllable.append(han)

            else:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(cur[2]) + 1)
                syllable.append(han)
                syllable.append(cur[3])

        elif cur[2] in _CHO_ and cur[3] in _JUNG_:
            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
            syllable.append(han)
            han = compose(_CHO_.index(cur[2]), _JUNG_.index(cur[3]), 0)
            syllable.append(han)

        elif cur[2] in _JUNG_ and cur[3] in _CHO_:
            engkey = jamo2engkey(cur[1] + cur[2])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                jung = _REVERSE_JAMO2ENGKEY_[engkey]
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(cur[3]) + 1)
                syllable.append(han)

            else:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                syllable.append(han)
                syllable.append(cur[2])
                syllable.append(cur[3])


        elif cur[2] in _JUNG_ and cur[3] in _JUNG_:
            engkey = jamo2engkey(cur[1] + cur[2])

            if engkey in _REVERSE_JAMO2ENGKEY_:
                jung = _REVERSE_JAMO2ENGKEY_[engkey]
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
                syllable.append(han)
                syllable.append(cur[3])

            else:
                engkey = jamo2engkey(cur[2] + cur[3])

                if engkey in _REVERSE_JAMO2ENGKEY_:
                    jung = _REVERSE_JAMO2ENGKEY_[engkey]
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                    syllable.append(han)
                    syllable.append(jung)

                else:
                    han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), 0)
                    syllable.append(cur[2])
                    syllable.append(cur[3])



    elif len(cur) == 5:

        if cur[2] in _CHO_ and cur[3] in _CHO_ and cur[4] in _JUNG_:
            han = compose(_CHO_.index(cur[0]), _JUNG_.index(cur[1]), _JONG_.index(cur[2]) + 1)
            syllable.append(han)
            han = compose(_CHO_.index(cur[3]), _JUNG_.index(cur[4]), 0)
            syllable.append(han)


        elif cur[2] in _JUNG_ and cur[3] in _CHO_ and cur[4] in _CHO_:
            engkey1 = jamo2engkey(cur[1] + cur[2])
            jung = _REVERSE_JAMO2ENGKEY_[engkey1]
            engkey2 = jamo2engkey(cur[3] + cur[4])

            if engkey2 in _REVERSE_JAMO2ENGKEY_:
                jong = _REVERSE_JAMO2ENGKEY_[engkey2]
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(jong) + 1)
                syllable.append(han)

            else:
                han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), _JONG_.index(cur[3]) + 1)
                syllable.append(han)
                syllable.append(cur[4])

        elif cur[2] in _JUNG_ and cur[3] in _CHO_ and cur[4] in _JUNG_:
            engkey = jamo2engkey(cur[1] + cur[2])
            jung = _REVERSE_JAMO2ENGKEY_[engkey]
            han = compose(_CHO_.index(cur[0]), _JUNG_.index(jung), 0)
            syllable.append(han)
            han = compose(_CHO_.index(cur[3]), _JUNG_.index(cur[4]), 0)
            syllable.append(han)


    return ''.join(syllable)

quotes = []
with open('quotes.txt', encoding = 'UTF-8') as fin:
    for line in fin.readlines():
        line = line.rstrip()
        quotes.append([line, len(line)])

import time, random

print('타자 연습이 3초 후에 시작됩니다.')
time.sleep(1)
print('타자 연습이 2초 후에 시작됩니다.')
time.sleep(1)
print('타자 연습이 1초 후에 시작됩니다.')
time.sleep(1)

accuracy = 0
count = 1
highest_speed = 0
while True:
    typing = quotes[random.randint(0, len(quotes) - 1)]
    print('%d: %s' % (count, typing[0]))
    print('%d: ' % count, end = '')
    time1 = time.time()
    s = input().rstrip()
    time2 = time.time()

    jamo_str = str2jamo(typing[0])
    key_str = jamo2engkey(jamo_str)
    typing[0] = engkey2jamo(key_str)
    typing[1] = len(typing[0])

    jamo_str = str2jamo(s)
    key_str = jamo2engkey(jamo_str)
    s = engkey2jamo(key_str)

    syllable_quote = jamo2syllable(typing[0])
    len_quote = len(syllable_quote)
    syllable_typing = jamo2syllable(s)

    while len(syllable_typing) < len_quote:
        syllable_typing += ' '

    identical = 0
    for i in range(len_quote):
        if syllable_quote[i] == syllable_typing[i]:
            identical += 1

    current_accuracy = identical / len_quote * 100
    speed = current_accuracy / 100 * typing[1] * 60 / (time2 - time1)
    print('현재 타수: 분당 %.2f타' % speed)
    highest_speed = max(speed, highest_speed)
    print('최고 타수: 분당 %.2f타' % highest_speed)
    print('현재 정확도: %.2f%%' % current_accuracy)

    accuracy *= count - 1
    accuracy += current_accuracy
    accuracy /= count
    print('전체 정확도: %.2f%%' % accuracy)
    print()

    count += 1