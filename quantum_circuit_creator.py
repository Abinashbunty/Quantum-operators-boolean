inputs = []
terms = []
d = []
row = []

m = 3 # Number of Qubits in the Input file containing the Truth Table
extra = m # To store a copy of m for future reference

from qiskit import QuantumProgram, CompositeGate

Q_obj = QuantumProgram() #Quantum object created
backend = 'local_qasm_simulator' #Backend is chosen

# filename = input("Enter name of the file: ")
filename = 'inputs.txt' #   File containing the desired Truth Table
# access_mode = input("Enter file mode")
file_object = open(filename, 'r')

"""
Let's name the various qubits as A, B, C and so on.
"""
for i in range(0, m):
    inputs.append(chr(i + 65))

"""
Separate the Input Qubits from its output value.
If the output is HIGH, append it to the list of minterms.
This will later help in reducing the Boolean expression.
"""
for i in range(pow(2, m)):
    row = file_object.readline().rstrip()
    row_qubits = row.split("-")
    if (row_qubits[1] == '1'):
        terms.append(i)

terms += d # appending all terms to work on a "copy" of the terms

"""
Designing a class to reduce the minterms. 
By checking the HIGH output minterms, we can solve
the expression and minimise it using Quine–McCluskey algorithm. 
Quine–McCluskey algorithm is used so that it can handle large number 
of bits, unlike Karnaugh maps which can be used only up to 4 qubits.
"""
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


final_exp = '' + booleanReduction(terms)
print(final_exp)

expression = ''.join(final_exp.split()) # To remove any space both inside the expression as well as at the ends.

"""
The obtained string expression has to be operated upon to
get the number of terms. For that, the number of '+' signs in the expression will help.
To find the additional number of qubits required to operate upon,
we have to find the number of individual qubits within the terms in the entire sequence. 

Reason:
In QISKit, there is no OR gate. To implement OR gate, we have use Toffoli gate
which acts as AND gate and form OR gates. For example: 

A OR B = NOT(NOT(A) AND NOT(B))

Toffoli gates are the quantum equivalent for AND gates. For every OR operation of
2 terms, we use a Tofolli gate and produce new qubits. Hence, the total number of 
qubits to be initialised are the number of +'s and .'s in the simplified 
boolean expression.
"""
no_of_plus = expression.count('+')
no_of_dots = expression.count('.')
no_of_extra_qubits = no_of_plus + no_of_dots

"""
Creation of Classical and Quantum registers.
Also, creation of the quantum circuit layout usinng those registers.
"""
qr = Q_obj.create_quantum_register("qr", m+no_of_extra_qubits)
cr = Q_obj.create_classical_register("cr", m+no_of_extra_qubits)
qc = Q_obj.create_circuit("Circuit", [qr], [cr])

list_expression = expression.split('+')

and_all_terms_list = []

for sub_expression in list_expression:
    not_gate_list = []  # To store qubits having "Bar" or the NOT operator on them.
    normal_gate_list = []
    list_sub_expression = sub_expression.split('.')

    """
    Let's separate the negated terms from the normal terms. 
    Put the bits having bar operator on them in different list
    """
    for i in range(0, len(list_sub_expression)):
        if(len(list_sub_expression[i])>1):
            not_gate_list.append(list_sub_expression[i][0])
        else:
            normal_gate_list.append(list_sub_expression[i])

    for ch in not_gate_list:
        qc.x(qr[ord(ch)-65])    # Application of NOT gates to the bits having the Bar over them

    merged_list = not_gate_list + normal_gate_list

    for i in range(0, len(merged_list)-1):
        ch1 = merged_list[i]
        ch2 = merged_list[i+1]
        """
        Application of Tofolli gate to the bits so that we can
        perform AND operation on the bits. This is stored into a new qubit.
        Hence, extra = extra + 1
        """
        qc.ccx(qr[ord(ch1)-65], qr[ord(ch2)-65], qr[extra]) # The result is computed and stored in another qubit.
        extra = extra + 1

    for ch in not_gate_list:
        qc.x(qr[ord(ch) - 65])

    extra = extra - 1
    qc.x(qr[extra])
    and_all_terms_list.append(extra)
    # To store the bits where the new qubits are stored after
    #  application of Toffoli gates
    extra = extra + 1

for i in range(0, len(and_all_terms_list)-1):
    qubit1 = and_all_terms_list[i]
    qubit2 = and_all_terms_list[i+1]

    """
    Now, all the terms have to be further implemented with AND gate to get to
    the penultimate stage. Hence, we have to apply Toffoli gates which are used
    as AND gates.
    """
    qc.ccx(qr[qubit1], qr[qubit2], qr[extra])
    extra = extra + 1

"""
Final application of NOT gate to get the result because we are trying to achieve this:

A ¦¦ B = NOT(NOT(A) AND (B))

Hence, we are applying the NOT gate to final qubit which holds the solution of the entire circuit.
"""
extra = extra - 1
qc.x(qr[extra])

"""
To generate the QASM Code fot the Quantum Circuit so that the working 
and chronology of the operations is understood. It describes a sequential 
order of execution of circuits along with operation of gates on the various
qubits. 
"""


QASM_source = Q_obj.get_qasm("Circuit")
print(QASM_source)