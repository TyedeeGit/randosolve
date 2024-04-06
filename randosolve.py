import random as rand
import copy
import math


class Rational:
    def __init__(self, n, d):
        if d < 0:
            n *= -1
            d *= -1
        elif d == 0:
            raise ValueError("Division by 0")
        if math.remainder(n, d) == 0:
            self.numerator = int(n / d)
            self.denominator = 1
        else:
            self.numerator = int(n / math.gcd(n, d))
            self.denominator = int(d / math.gcd(n, d))

    def __abs__(self):
        return Rational(abs(self.numerator), self.denominator)

    def __add__(self, other):
        if type(other) is int:
            return Rational(other * self.denominator + self.numerator, self.denominator)
        else:
            return Rational(self.numerator * other.denominator + other.numerator * self.denominator,
                            self.denominator * other.denominator)

    def __sub__(self, other):
        return self + other * -1

    def __mul__(self, other):
        if type(other) is int:
            return Rational(other * self.numerator, self.denominator)
        else:
            return Rational(self.numerator * other.numerator, self.denominator * other.denominator)

    def __str__(self):
        if self.denominator == 1:
            num = self.numerator
            strnum = str(num)
            return strnum
        else:
            strnum = f'{self.numerator}/{self.denominator}'
            return strnum

    def __eq__(self, other):
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __le__(self, other):
        return self.numerator * other.denominator <= self.denominator * other.numerator

    def __lt__(self, other):
        return self.numerator * other.denominator < self.denominator * other.numerator

    def reciprical(self):
        return Rational(self.denominator, self.numerator)


zero = Rational(0, 1)
one = Rational(1, 1)


def get_integer_as_rational(n):
    return Rational(n, 1)


ten = get_integer_as_rational(10)


def decode_rational(string):
    if '/' not in string:
        return Rational(int(string), 1)
    else:
        n, d = string.split('/')
        return Rational(int(n), int(d))

def len_str_abs(num):
    return len(str(abs(num)))


class Row:
    def __init__(self, rownum, sequence, seqtotal, max_rownum=1):
        self.length = len(sequence)
        self.rownum = rownum
        self.sequence = sequence
        self.seqtotal = seqtotal
        self.max_length = max(len(str(num)) for num in self.sequence)
        self.max_rownum = max_rownum
        self.max_seqtotal_length = len_str_abs(seqtotal)

    def __str__(self):
        modseq = self.sequence
        modstr = ''
        modtotal = self.seqtotal
        modtotalstr = str(modtotal)

        if modtotal >= zero:
            modtotalstr = ' ' + modtotalstr
        for i in range(self.length):
            if 0 < i < self.length:
                modstr += ","
            num = modseq[i]
            strnum = ' ' + str(num) + ' '
            if num >= zero:
                strnum = ' ' + strnum
            modstr += strnum + (self.max_length - len(strnum)) * ' '
        return f"R{self.rownum}{(len_str_abs(self.max_rownum) - len_str_abs(self.rownum)) * ' '}: [{modstr}| {modtotalstr}{(self.max_seqtotal_length - len_str_abs(modtotal)) * ' '}]"

    def __mul__(self, other):
        newseq = [0] * self.length
        for i in range(len(self.sequence)):
            newseq[i] = self.sequence[i] * other
        return Row(self.rownum, newseq, self.seqtotal * other)

    def __add__(self, other):
        newseq = [0] * self.length
        for i in range(len(self.sequence)):
            newseq[i] = self.sequence[i] + other.sequence[i]
        return Row(self.rownum, newseq, self.seqtotal + other.seqtotal)

    def __eq__(self, other):
        return (self.sequence == other.sequence) and (self.seqtotal == other.seqtotal)


class Matrix:
    def __init__(self, rows):
        self.rows = rows
        self.max_length = 0
        self.max_seqtotal_length = 0
        self.update_max_length()

    def __str__(self):
        self.update_max_length()
        string = "\n".join(str(row) for row in self.rows)
        return string + '\n'

    def __eq__(self, other):
        for i in range(len(self.rows)):
            if self.rows[i] != other.rows[i]:
                return False
        return True

    def update_max_length(self):
        self.max_length = 0
        self.max_seqtotal_length = max(len_str_abs(row.seqtotal) for row in self.rows) + 1
        for row in self.rows:
            row.max_rownum = len(self.rows)
            self.max_length = max(self.max_length, max(len_str_abs(num) for num in row.sequence) + 2)
        for row in self.rows:
            row.max_length = self.max_length + 1
            row.max_seqtotal_length = self.max_seqtotal_length

    def swap(self, row1, row2):
        row1row = self.rows[row1 - 1]
        row2row = self.rows[row2 - 1]
        self.rows[row2 - 1].rownum = row1
        self.rows[row1 - 1].rownum = row2
        self.rows.remove(row1row)
        self.rows.insert(row1 - 1, row2row)
        self.rows.remove(row2row)
        self.rows.insert(row2 - 1, row1row)

    def multiply(self, rownum, amount):
        old_self = copy.deepcopy(self)
        self.rows[rownum - 1] *= amount
        return old_self

    def add_multiple(self, rownum1, rownum2, amount):
        old_self = copy.deepcopy(self)
        self.rows[rownum1 - 1] += self.rows[rownum2 - 1] * amount
        return old_self


def solve_matrix(matrix, print_steps=True):
    detected_hard = False
    old_matrix = copy.deepcopy(matrix)
    new_matrix = matrix
    total_row_count = len(new_matrix.rows)
    # Eliminates numbers below the diagonal. This is the hard part, mainly because complicated fractions accumulate above the diagonal during this step.
    for k in range(total_row_count):
        for i in range(total_row_count):
            if new_matrix.rows[i].sequence[i] == zero:
                new_matrix.swap(i + 1, i)
            diagonal_eliminator = new_matrix.rows[i].sequence[i]

            for j in range(k, i):
                n = new_matrix.rows[i].sequence[j]
                new_matrix.add_multiple(i + 1, j + 1, new_matrix.rows[i].sequence[j] * -1)
                if n != zero and print_steps:
                    print(f'Subtract {str(n * diagonal_eliminator).strip(" ")} * R{j + 1} from R{i + 1}:')
                    print(new_matrix)
            new_matrix.multiply(i + 1, new_matrix.rows[i].sequence[i].reciprical())
    # Normalize matrix. This helps clean up the complicated fractions from the previous step.
    for i in range(total_row_count):
        if new_matrix.rows[i].sequence[i] == zero:
            new_matrix.swap(i + 1, i)
        new_matrix.multiply(i + 1, new_matrix.rows[i].sequence[i].reciprical())
    if print_steps:
        print("Matrix normalized in triangle form:")
        print(new_matrix)
    # Reduce matrix from triangle form. After that the matrix is solved
    for i in range(total_row_count):
        for j in range(total_row_count):
            k = total_row_count - i - 1
            l = total_row_count - j - 1
            if k != l:
                n = new_matrix.rows[l].sequence[k]
                new_matrix.add_multiple(l + 1, k + 1, new_matrix.rows[l].sequence[k] * -1)
                if n != zero and print_steps:
                    print(f'Subtract {str(n).strip(" ")} * R{k + 1} from R{l + 1}:')
                    print(new_matrix)
    if print_steps:
        print("Matrix solved:")
    return new_matrix, old_matrix


def generate_matrix():
    h = 0
    rows = 0
    o = None
    while True:
        try:
            rows = int(input("How many rows to generate(fractions get exponentially huge for anything above 10)? "))
        except ValueError:
            continue
        break
    matrixrows = [zero] * rows
    solved_rows = []
    for i in range(rows):
        solved_row = [zero] * (rows - 1)
        solved_row.insert(i, one)
        solved_rows.append(Row(i + 1, solved_row, one))
    solved_matrix = Matrix(solved_rows)
    good_matrix = False
    while not good_matrix and h <= 10:
        for j in range(rows):
            seq = [0] * rows
            n = zero
            for i in range(rows):
                n = get_integer_as_rational(rand.randint(-3, 4))
                if n == zero:
                    n = one
                seq[i] = n
            total = get_integer_as_rational(rand.randint(-1, 3)) * get_integer_as_rational(
                rand.randint(1, 4)).reciprical()
            matrixrows[j] = Row(j + 1, seq, total)
        try:
            solved_matrix, o = solve_matrix(Matrix(matrixrows), print_steps=False)
            good_matrix = True
            for row in solved_matrix.rows:
                if row.seqtotal.denominator >= 100000:
                    # good_matrix = False
                    print("Warning: huge fractions in solution")
                    break
        except ValueError:
            print("Generated unsolvable matrix, retrying...")
            h += 1
            continue
    if h > 10:
        print("Could not find solvable matrix in less than 10 tries. Good luck!")
        o = Matrix(matrixrows)
    else:
        print("Found good matrix. Yay!")
    # This code at the end helps get rid of complicated or impossible matrices.
    return o, solved_matrix

def handle_new_game(autosolved, solved):
    if solved:
        if not autosolved:
            print("Good job! You solved the matrix!")
        else:
            print("Try completing all of the steps yourself next time.")
    while True:
        make_new_matrix = input("New game(Y/N)? ")
        if make_new_matrix.lower() == 'y':
            return generate_matrix()
        elif make_new_matrix.lower() == 'n':
            return None, None
        else:
            print(f"Could not understand '{make_new_matrix}'")

def main():
    # m is the random matrix, sm is the solved matrix to compare to.
    m, sm = generate_matrix()
    history = [m]
    print(f'Your matrix is: \n{m}')
    while True:
        cmd = input('> ')
        args = cmd.split(' ')
        # noinspection PyRedeclaration
        autosolved = False
        try:
            if args[0] == 'multiply':
                history.append(m.multiply(int(args[1]), decode_rational(args[2])))
                print(m)
            elif args[0] == 'add':
                history.append(m.add_multiple(int(args[1]), int(args[2]), decode_rational(args[3])))
                print(m)
            elif args[0] == 'undo':
                m = history.pop()
                print(m)
            elif args[0] == 'swap':
                history.append(m.swap(int(args[1]), int(args[2])))
                print(m)
            elif args[0] == 'quit':
                break
            elif args[0] == 'normalize':
                rownumber = int(args[1])
                history.append(m.multiply(rownumber, m.rows[rownumber - 1].sequence[rownumber - 1].reciprical()))
                print(m)
            elif args[0] == 'get_factor':
                print(decode_rational(args[2]) * decode_rational(args[1]).reciprical())
            elif args[0] == 'solve':
                m, old_m = solve_matrix(m)
                autosolved = True
                history.append(old_m)
                print(m)
            elif args[0] == 'new':
                nm, nsm = handle_new_game(autosolved, False)
                if nm:
                    m, sm = nm, nsm
                    history = [m]
            else:
                print(f'Could not understand "{args[0]}".')
        except Exception as e:
            raise e

        if m == sm:
            m, sm = handle_new_game(autosolved, True)
            if not m:
                return
            history = [m]
            print(f'Your matrix is: \n{m}')

if __name__ == '__main__':
    main()
