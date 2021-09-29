def delete_substring(s, start, length):
    string1 = s[:start]
    string2 = s[start + length:len(s)]
    return (string1 + string2)

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError("Input is neither 'True' nor 'False': " + s)

