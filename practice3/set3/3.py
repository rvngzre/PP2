digits = {
    "ZER": "0", "ONE": "1", "TWO": "2", "THR": "3", "FOU": "4",
    "FIV": "5", "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
}
rev = {v: k for k, v in digits.items()}


def word_to_num(s):
    num = ""
    for i in range(0, len(s), 3):
        num += digits[s[i:i+3]]
    return int(num)


def num_to_word(n):
    return "".join(rev[d] for d in str(n))


s = input()

if '+' in s:
    a, b = s.split('+')
    r = word_to_num(a) + word_to_num(b)
elif '-' in s:
    a, b = s.split('-')
    r = word_to_num(a) - word_to_num(b)
else:
    a, b = s.split('*')
    r = word_to_num(a) * word_to_num(b)

print(num_to_word(r))
