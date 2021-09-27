def delete_substring(s, start, length):
    string1 = s[:start]
    string2 = s[start + length:len(s)]
    return (string1 + string2)

