import threading, requests


def download_image(name, link, d):
    d[name] = requests.get(link).content


def main(name=None):
    a = threading.Thread(target=download_image, args=(name))
    a.start()
    return a


# word fixer to adjust the words
def word_fixer(a, f=70):
    b = ""
    for i in a.split("\n"):
        if len(i) < f:
            b += i + '\n'
        else:
            k = ""
            for j in i.split():
                k += j + " "
                if len(k) > f:
                    b += k + '\n'
                    k = ''
            if len(k) <= f:
                b += k + '\n'
    return b


# img downloader for search and home pg
def main1(lst):
    b = []
    for i in lst:
        b.append(i[:2])
    k = dict(b)
    b = []
    for i in k:
        a = threading.Thread(target=download_image, args=(i, k[i], k), daemon=True)
        a.start()
        b.append(a)
    [i.join(timeout=2) for i in b]
    for i in k:
        if type(k[i]) != bytes:
            k[i] = None

    c = []
    for i, j in zip(k, lst):
        a = j + [k[i]]
        c.append(a)

    return c


# epi button arranger
def buttons(value):
    need = []
    c = 0
    r = 0
    for i in range(value):
        need.append([r, c])
        c += 1
        if c == 5:
            c = 0
            r += 1
    return need


def download_imgs(link, n, d):
    d[n] = (requests.get(link).content)


# img downloader for trending
def main12(lst):
    b = []

    d = {}
    c = 1
    imgs = [i[0] for i in lst]

    for i in imgs:
        d[c] = i
        c += 1
    newd = {}
    for i in d:
        a = threading.Thread(target=download_imgs, args=(d[i], i, newd), daemon=True)
        a.start()
        b.append(a)
    [i.join(timeout=2) for i in b]
    k = {}
    for i in newd:
        if type(newd[i]) != bytes:
            k.update({i: None})
        else:
            k.update({i: newd[i]})
    b = sorted(k)
    newone = []
    for i in b:
        newone.append(k[i])
    new_one = []
    for i, j in zip(newone, lst):
        new_one.append([i] + [j[1]] + [word_fixer(j[2], 20)] + j[3:])
    return new_one
