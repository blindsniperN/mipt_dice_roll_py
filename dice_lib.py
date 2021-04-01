import matplotlib.pyplot as plt


def expected_value(x):  # подсчёт мат ожидания
    summa = 0
    for i in range(len(x)):
        summa += i * x[i]
    return summa / sum(x)


def plt_probability(x, y):  # построение графика
    sm = sum(y)
    y_plt = [number / sm for number in y]
    plt.bar(x, y_plt)
    plt.show()


class DiceRoll:
    def __init__(self, s):
        self.diceN_ = {}
        self.modifier_ = 0  # модификатор броска
        self.add(s)

    def add(self, s):
        if s != '':
            s += ' + '
            while s != '':
                if (s[:s.find(' ')]).find('d') != -1:
                    amount = int(s[:s.find('d')])
                    s = s[s.find('d') + 1:]
                    cap = int(s[:s.find(' ')])
                    if cap in self.diceN_:
                        self.diceN_[cap] += amount
                    else:
                        self.diceN_[cap] = amount
                elif s != ' ':
                    self.modifier_ += int(s[:s.find(' ')])
                s = s[s.find('+') + 2:]

    def minus(self, s):
        s += ' + '
        while s != '':
            if s[:s.find(' ')].find('d') != -1:
                amount = int(s[:s.find('d')])
                s = s[s.find('d') + 1:]
                cap = int(s[:s.find(' ')])
                s = s[s.find('+') + 2:]
                if cap in self.diceN_:
                    if self.diceN_[cap] <= amount:
                        self.diceN_[cap] = 0
                    else:
                        self.diceN_[cap] -= amount
            elif s != ' ':
                self.modifier_ -= int(s[:s.find(' ')])
            s = s[s.find('+') + 2:]

    def print(self):
        s = ''
        for el in sorted(self.diceN_.items()):
            if el[1] != 0:
                s += str(el[1]) + 'd' + str(el[0]) + ' + '
        if self.modifier_ != 0:
            s += str(self.modifier_)
        else:
            s = s[:len(s)-2]
        if s != '':
            print('Current dice:', s)
        else:
            print('0 cubes added')

    def return_dict(self):
        return self.diceN_

    def average_dice(self):
        sum_d = 0
        for el in self.diceN_.items():
            sum_d += el[1] * (el[0] + 1) / 2
        return int(sum_d) + self.modifier_

    def max_res(self):
        sum_d = 0
        for el in self.diceN_.items():
            sum_d += el[1]*el[0]
        return sum_d + self.modifier_

    def arr_sum(self):  # подсчёт массива всех возможных величин
        x = [0] * (self.max_res() + 1)
        x[self.modifier_] = 1
        for el in self.diceN_.items():
            for i in range(el[1]):
                cpy = [0] * (self.max_res() + 1)
                for j in range(len(x) - el[0]):
                    for k in range(1, el[0] + 1):
                        cpy[j + k] += x[j]
                x = cpy
        return x

    def geqslant(self, x):
        if x < self.modifier_:
            return 1
        elif x > self.max_res():
            return 0
        else:
            arr = self.arr_sum()
            return sum(arr[x:]) / sum(arr)

    def leqslant(self, x):
        if x < self.modifier_:
            return 0
        elif x >= self.max_res():
            return 1
        else:
            arr = self.arr_sum()
            return sum(arr[:x+1]) / sum(arr)

    def eq(self, x):
        if x < self.modifier_ or x > self.max_res():
            return 0
        else:
            arr = self.arr_sum()
            return arr[x] / sum(arr)

    def adv(self):
        for el in self.diceN_.items():
            x = [0] * (el[0] + self.modifier_ + 1)
            x[self.modifier_] = 1
            for i in range(el[1]):
                cpy = [0] * (el[0] + self.modifier_ + 1)
                for j in range(el[0] + self.modifier_ + 1):
                    for k in range(self.modifier_ + 1, el[0] + self.modifier_ + 1):
                        cpy[max(j, k)] += x[j]
                x = cpy
        return x

    def dis(self):
        for el in self.diceN_.items():
            x = [0] * (el[0] + self.modifier_ + 1)
            x[el[0] + self.modifier_] = 1
            for i in range(el[1]):
                cpy = [0] * (el[0] + self.modifier_ + 1)
                for j in range(el[0] + self.modifier_ + 1):
                    for k in range(self.modifier_ + 1, el[0] + self.modifier_ + 1):
                        cpy[min(j, k)] += x[j]
                x = cpy
        return x

    def plt_max(self, modif):
        sz = 0
        for el in self.diceN_.items():
            sz = el[0]
        x = range(sz + self.modifier_ + 1)
        if modif == 1:
            y = self.adv()
        else:
            y = self.dis()
        plt_probability(x, y)

    def arr_sum_reroll_less(self, least_reroll): # подсчёт массива всех возможных величин
        x = [0] * (self.max_res() + 1)
        x[self.modifier_] = 1
        for el in self.diceN_.items():
            for i in range(el[1]):
                cpy = [0] * (self.max_res() + 1)
                for j in range(len(x) - el[0]):
                    for k in range(1, el[0] + 1):
                        if k > least_reroll:
                            cpy[j + k] += x[j] * el[0]
                        else:
                            for reroll in range(1, el[0] + 1):
                                cpy[j + reroll] += x[j]
                x = cpy
        return x