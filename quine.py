# ------------------------------------------------------------------------------------------------


inputs = ['A']  # Put the values that F=1 in the Terms List
terms = [1]  # the terms equal to 1
d = []  # Dont care list
op = 'F'  # the output name


# ------------------------------------------------------------------------------------------------


class term:
    def __init__(self, x, l):
        self.prime = True
        self.m = [x]
        self.val = bin(x)[2:]
        while (len(self.val) < l):
            self.val = '0' + self.val
        self.ones = self.val.count('1')

    def hd(self, x):
        hd, pos = 0, 0
        for i in range(len(x.val)):
            if (self.val[i] != x.val[i]):
                hd += 1
                pos = i
            if (hd > 1):
                return -1
        if (hd == 1 and (x.val.find('-') == self.val.find('-'))):
            return pos
        else:
            return -1

    def msIn(self, x):
        ret = []
        for i in self.m:
            if (i in x):
                ret += [i]
        return ret, len(ret)

    def __str__(self):
        return self.val

    def __eq__(self, x):
        return self.val == x.val

    def __lt__(self, x):
        return self.m < x.m


# ===============================================================================
def setTerms(terms, inputs):
    fo = (len(terms), len(inputs))
    for i in range(fo[0]):
        terms.append(term(terms[i], fo[1]))
    return terms[int(len(terms) / 2):]


def combineTerms(x):  # O(n^2 +n) :(
    ret = []
    for i in x:
        for j in x:
            buf = i.hd(j)
            if ((buf != -1) and (j.ones - i.ones == 1)):
                i.prime = False
                j.prime = False
                fo = list(i.val)
                v = term(1, 4)
                v.m = []
                # for k in i.m: v.m.append(k)
                v.m += i.m
                # for k in j.m: v.m.append(k)
                v.m += j.m
                fo[buf] = '-'
                v.val = ''.join(fo)
                v.ones = v.val.count('1')
                ret.append(v)
    for i in x:
        if i.prime == True:
            ret.append(i)
    return ret


def lettersFromBinary(x):
    ret = ''
    for i in range(len(x)):
        if (x[i] == '0'):
            # ret+='~'+inputs[i]+'.'
            ret += inputs[i] + '`' + '.'
        elif (x[i] == '1'):
            ret += inputs[i] + '.'
    return ret[:len(ret) - 1]


def result(x):
    buf = ''
    for i in x:
        fo = lettersFromBinary(i.val)
        if (fo != ''):
            buf += fo + ' + '
    return buf[:len(buf) - 3]


def sizeImpl(x):
    while (True):
        buf = combineTerms(x)
        if (x == buf):
            break
        x = buf
    return x


def getGroups(x):
    buf = list(x)
    for i in range(len(x)):
        if (x.count(x[i]) == 2) and x[i].val != '':
            x[i].val = ''
            buf.remove(x[i])
    return buf


def primeTable(x):
    ms = {}
    ret = []
    for i in x:
        for k in i.m:
            try:
                ms[k].append(i)
            except:
                ms[k] = [i]

    for i in ms:
        if (len(ms[i]) == 1 and i not in d):
            for j in ms[i]:
                if (j not in ret):
                    ret.append(j)
    for i in ret:
        for j in i.m: ms.pop(j, None)
    for i in d:
        ms.pop(i, None)

    while (len(ms) != 0):
        currentLength, currentGroups, prime = 0, 0, 0
        for i in ms:
            for j in ms[i]:
                nextGroups, nextLength = j.msIn(ms.keys())
                if (nextLength > currentLength):
                    currentLength = nextLength
                    currentGroups = nextGroups
                    prime = j
        ret.append(prime)
        for i in currentGroups:
            ms.pop(i, None)

    # print ms

    return ret


def boolReduce(x):
    x = primeTable(getGroups(sizeImpl(setTerms(x, inputs))))
    print('The reduced Boolean equation is \n', result(x))


# classes and helper functions
# =============================================================================
terms += d
print(' ')
print('RESULT FOR ', op)
boolReduce(terms)