from qiskit import QuantumProgram
Q_obj = QuantumProgram() #Quantum object created
backend = 'local_qasm_simulator' #Backend is chosen

inputs = []
terms = []
d = []

m = int(input("Enter the number of qubits involved: "))

qr = Q_obj.create_quantum_register("qr", m)
cr = Q_obj.create_classical_register("cr", m)
qc = Q_obj.create_circuit(None, [qr], [cr])

filename = input("Enter name of the file: ")

access_mode = input("Enter file mode")
file_object = open(file_name_input(), access_mode)

for i in range(0, m):
    inputs.append(chr(i + 65))

for i in range(pow(2, m)):
    row[i] = file_object.readline().rstrip()
    row_qubits[i] = row[i].split("-")
    if (row_qubits[i][1] == '1'):
        terms.append(i)

terms += d

final_exp = '' + booleanReduction(terms)
print(final_exp)

expression = ''.join(expression.split())
    list_expression = expression.split('+')
    no_of_terms = len(list_expression)

    not_gate_qubits = []
    for i in range(0, no_of_terms):
        sub_term = list_expression[i]
        list_sub_term = sub_term.split('.')
        no_of_sub_terms = len(list_sub_term)

        for j in range(0, no_of_sub_terms):
            each_bit = list_sub_term[j]
            if (len(each_bit) > 1):
                not_gate_qubits.append(each_bit[0])

        while (no_of_sub_terms <= 3):
            list_sub_term.append(0)
            no_of_sub_terms = no_of_sub_terms + 1

        for j in range(0, len(not_gate_qubits)):
            each_bit = not_gate_qubits[j]
            qc.x(qr[ord(each_bit) - 65])

        for j in range(0, no_of_sub_terms - 1):
            each_bit_1 = list_sub_term[j]
            each_bit_2 = list_sub_term[j + 1]
            qc.cx(qr[ord(each_bit_1) - 65], qr[ord(each_bit_2) - 65])

        list_sub_term.clear()


class Expression:
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

def setTerms(terms, inputs):
    fo = (len(terms), len(inputs))
    for i in range(fo[0]):
        terms.append(Expression(terms[i], fo[1]))
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
                v = Expression(1, 4)
                v.m = []
                v.m += i.m
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
            ret += inputs[i] + '|' + '.'
        elif (x[i] == '1'):
            ret += inputs[i] + '.'
    return ret[:len(ret) - 1]

def expression_output(x):
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

def obtainGroups(x):
    buf = list(x)
    for i in range(len(x)):
        if (x.count(x[i]) == 2) and x[i].val != '':
            x[i].val = ''
            buf.remove(x[i])
    return buf

def manipulation(x):
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

    return ret

def booleanReduction(x):
    x = manipulation(obtainGroups(sizeImpl(setTerms(x, inputs))))
    reduced_exp = '' + expression_output(x)
    return reduced_exp
