from qiskit import QuantumProgram
Q_obj = QuantumProgram() #Quantum object created
backend = 'local_qasm_simulator' #Backend is chosen

def no_of_qubits():
    m = int(input("Enter the number of qubits involved: "))
    return m

def qubit_declaration(m):
    qr = Q_obj.create_quantum_register("qr", m)
    cr = Q_obj.create_classical_register("cr", m)
    qc = Q_obj.create_circuit(None, [qr], [cr])

def file_name_input():
    filename = input("Enter name of the file: ")
    return filename

def create_file_object():
    access_mode = input("Enter file mode")
    file_object = open(file_name_input(), access_mode)
# ------------------------------------------------------------------------------------------------
    for i in range(0,m):
        inputs.append(chr(i+65))

    for i in range(pow(2, m)):
        row[i] = file_object.readline().rstrip()
        row_qubits[i] = row[i].split("-")
        if(row_qubits[i][1] == '1'):
            terms.append(i)

    d = []
# inputs = ['A', 'B', 'C', 'D', 'E']  # Put the values that F=1 in the Terms List
# terms = [6, 7, 12, 13, 14, 15, 22, 23, 24, 25, 30, 31]  # the terms equal to 1
# d = []  # Dont care list
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

def setTerms(terms, inputs):
    fo = (len(terms), len(inputs))
    for i in range(fo[0]):
        terms.append(term(terms[i], fo[1]))
    return terms[int(len(terms) / 2):]


def combineTerms(x):
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

    return ret


def boolReduce(x):
    x = primeTable(getGroups(sizeImpl(setTerms(x, inputs))))
    # print('The reduced Boolean equation is \n', result(x))
    reduced_exp = '' + result(x)
    return reduced_exp

# print(' ')
# print('RESULT FOR ', op)
collected_exp = '' + boolReduce(terms)

# print(collected_exp)

qr = Q_obj.create_quantum_register("qr", m)
cr = Q_obj.create_classical_register("cr", m)
qc = Q_obj.create_circuit(None, [qr], [cr])

def quantum_circuit_extractor(expression):
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
            if(len(each_bit)>1):
                not_gate_qubits.append(each_bit[0])

        while(no_of_sub_terms<=3):
            list_sub_term.append(0)
            no_of_sub_terms = no_of_sub_terms + 1

        for j in range(0, len(not_gate_qubits)):
            each_bit = not_gate_qubits[j]
            qc.x(qr[ord(each_bit)-65])

        for j in range(0, no_of_sub_terms-1):
            each_bit_1 = list_sub_term[j]
            each_bit_2 = list_sub_term[j+1]
            qc.cx(qr[ord(each_bit_1)-65], qr[ord(each_bit_2)-65])


        list_sub_term.clear()
    # print(not_gate_qubits)



    # print(no_of_terms)

quantum_circuit_extractor(collected_exp)