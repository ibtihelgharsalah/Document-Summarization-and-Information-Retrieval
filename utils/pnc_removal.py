# replace any character that is not a word character (\w) or whitespace (\s) with an empty string
def pnc_removal(tokens):
    pnc_removed = [token for token in tokens if token.isalpha()]
    # pnc_removed = text.replace('[^\w\s]|[\d]','')
    return pnc_removed