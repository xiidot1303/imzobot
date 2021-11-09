def list_to_text(l):
    t = ''
    for i in l:
        t += str(i.value) + '||'
    return t