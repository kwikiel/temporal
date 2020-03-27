import requests

def flat_dict(url):
    fd = {}
    r = requests.get(url)
    foo = r.json()
    baz = flatten_json(foo) # Refactor
    for x, y in baz.items():
        try:
            if(float(y)!=0.0):
                fd[x] = float(y) 
        except:
            pass
    return fd

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

