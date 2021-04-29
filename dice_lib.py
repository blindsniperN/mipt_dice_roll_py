import matplotlib.pyplot as plt
from random import randint
from numpy import percentile


def expected_value(x):  # подсчёт мат ожидания
    if x is not None:
        summa = 0
        for i in range(len(x)):
            summa += i * x[i]
        return summa / sum(x)


def turn_list_to_probability(y, acc):
    if y is not None:
        sm = sum(y)
        x = [round(number / sm, acc) for number in y]
        return x


def plt_probability(y):  # построение графика
    if y is not None:
        plt.bar(range(len(y)), y)
        plt.show()


# на вход последующим трём функциям подаётся массив исходов, а на выходе - одно значение - возможность выкинуть
def probability_to_roll_greater_or_equal(arr, value, x):
    if arr is not None:
        if x < value:
            return 1
        elif x > len(arr) - 1:
            return 0
        else:
            return sum(arr[x:]) / sum(arr)


def probability_to_roll_less_or_equal(arr, value, x):
    if arr is not None:
        if x < value:
            return 0
        elif x >= len(arr) - 1:
            return 1
        else:
            return sum(arr[:x+1]) / sum(arr)


def probability_to_roll_equal(arr, value, x):
    if arr is not None:
        if x < value or x > len(arr) - 1:
            return 0
        else:
            return arr[x] / sum(arr)


def roll(arr):  # механика броска такая же, как в проекте по тп
    if arr is not None:
        x = randint(1, sum(arr))
        i = 0
        while x > 0:
            x -= arr[i]
            i += 1
        return i - 1


class DiceRoll:
    def __init__(self, s):  # инициализируется через словарь
        self.diceN_ = {}
        self.modifier_ = 0  # модификатор броска
        self.add(s)

    # str_inp - ввод кубов в short notation записи: 1d6, 2d20 + 5. add - добавляет эти кубы в запись, minus - удаляет
    def add(self, str_inp):
        if str_inp != '':
            str_inp += ' + '
            while str_inp != '':
                if (str_inp[:str_inp.find(' ')]).find('d') != -1:
                    amount = int(str_inp[:str_inp.find('d')])
                    str_inp = str_inp[str_inp.find('d') + 1:]
                    cap = int(str_inp[:str_inp.find(' ')])
                    if cap in self.diceN_:
                        self.diceN_[cap] += amount
                    else:
                        self.diceN_[cap] = amount
                elif str_inp != ' ':
                    self.modifier_ += int(str_inp[:str_inp.find(' ')])
                str_inp = str_inp[str_inp.find('+') + 2:]

    def minus(self, str_inp):
        str_inp += ' + '
        while str_inp != '':
            if str_inp[:str_inp.find(' ')].find('d') != -1:
                amount = int(str_inp[:str_inp.find('d')])
                str_inp = str_inp[str_inp.find('d') + 1:]
                cap = int(str_inp[:str_inp.find(' ')])
                str_inp = str_inp[str_inp.find('+') + 2:]
                if cap in self.diceN_:
                    if self.diceN_[cap] <= amount:
                        self.diceN_[cap] = 0
                    else:
                        self.diceN_[cap] -= amount
            elif str_inp != ' ':
                self.modifier_ -= int(str_inp[:str_inp.find(' ')])
            str_inp = str_inp[str_inp.find('+') + 2:]

    # вывод всех текущих кубов в классе
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
            print('0 dice added')

    # возвращает текущие кубы в классе диктом
    def return_dict(self):
        return self.diceN_

    # возвращает максимальное значение, которое может выпасть на кубах
    def max_res(self):
        sum_d = 0
        for el in self.diceN_.items():
            sum_d += el[1]*el[0]
        return sum_d + self.modifier_

    def list_sum(self):  # подсчёт массива всех возможных величин при обычном броске куба
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

    # лист количества возможных исходов (значений на кубах) при броске с преимуществом: выбирается максимум из того, что
    # выпало на кубах
    def lst_outcomes_roll_with_advantage(self):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
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

    # лист количества возможных исходов (значений на кубах) при броске с помехой: выбирается минимум из того, что
    # выпало на кубах
    def lst_outcomes_roll_with_disadvantage(self):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
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

    # лист количества возможных исходов (значений на кубах) при перебрасывании кубов, если на них выпало <= value
    def lst_outcomes_roll_again_less_or_equal(self, value):  # подсчёт массива всех возможных величин
        x = [0] * (self.max_res() + 1)
        x[self.modifier_] = 1
        for el in self.diceN_.items():
            for i in range(el[1]):
                cpy = [0] * (self.max_res() + 1)
                for j in range(len(x) - el[0]):
                    for k in range(1, el[0] + 1):
                        if k > value:
                            cpy[j + k] += x[j] * el[0]
                        else:
                            for dice_result in range(1, el[0] + 1):
                                cpy[j + dice_result] += x[j]
                x = cpy
        return x

    def witcher_explosive_dice_probabilities(self, depth):
        if len(self.diceN_) != 1:
            print('Cannot calculate that')
            return None
        else:
            for el in self.diceN_.items():
                if el[1] != 1:
                    print('Cannot calculate that')
                    return None
                else:
                    arr = [0] * (self.modifier_ + depth * el[0] + 1)
                    for i in range(depth):
                        for j in range(1, el[0]):
                            arr[self.modifier_ + i * el[0] + j] = el[0] ** (depth - i - 1)
                    arr[len(arr) - 1] = 1
                    return arr


def prob_preparation(d, s):  # предобработка кубов для команд r>=, r==, r<=
    y = 0
    arr = []
    if s[4:7] == 'sum':
        arr = d.list_sum()
        y = int(s[8:])
    elif s[4:7] == 'adv':
        arr = d.lst_outcomes_roll_with_advantage()
        y = int(s[8:])
    elif s[4:7] == 'dis':
        arr = d.lst_outcomes_roll_with_disadvantage()
        y = int(s[8:])
    elif s[4:7] == 'rrl':
        x, y = map(int, s[8:].split())
        arr = d.lst_outcomes_roll_again_less_or_equal(x)
    elif s[4:7] == 'bmb':
        x, y = map(int, s[8:].split())
        arr = d.witcher_explosive_dice_probabilities(x)
    return [arr, y]


def preparation(d, s):  # предобработка кубов для прочих команд
    arr = []
    if s[4:7] == 'sum':
        arr = d.list_sum()
    elif s[4:7] == 'adv':
        arr = d.lst_outcomes_roll_with_advantage()
    elif s[4:7] == 'dis':
        arr = d.lst_outcomes_roll_with_disadvantage()
    elif s[4:7] == 'rrl':
        x = int(s[8:])
        arr = d.lst_outcomes_roll_again_less_or_equal(x)
    elif s[4:7] == 'bmb':
        arr = d.witcher_explosive_dice_probabilities(int(s[8:]))
    return arr


def rolling_dice(d, s, accuracy):
    cmd = s[:3]
    if cmd == 'add':  # добавить кубы
        d.add(s[4:])

    elif cmd == 'del':  # удалить кубы
        d.minus(s[4:])

    elif cmd == 'max':
        return 'Max sum on dice: ' + str(d.max_res())

    elif cmd == 'arr':  # массив кубов
        return preparation(d, s)

    elif cmd == 'r>=':
        arr, y = prob_preparation(d, s)
        res = probability_to_roll_greater_or_equal(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r<=':
        arr, y = prob_preparation(d, s)
        res = probability_to_roll_less_or_equal(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r==':
        arr, y = prob_preparation(d, s)
        res = probability_to_roll_equal(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'xpv':  # мат ожидание
        res = expected_value(preparation(d, s))
        if res is not None:
            return round(res, accuracy)

    elif cmd == 'prb':
        return turn_list_to_probability(preparation(d, s), accuracy)

    elif cmd == 'plt':
        plt_probability(turn_list_to_probability(preparation(d, s), accuracy))

    elif cmd == 'rll':
        return roll(preparation(d, s))

    elif cmd == 'prc':
        arr, y = prob_preparation(d, s)
        if arr is not None:
            return str(y) + '% percentile is: ' + str(percentile(arr, y))


# лист мат ожиданий урона в заивисимости от значения ac
# critical hit - критическое попадание, попадание, при котором результат на кубах удваивается
def expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode, are_there_critical_hits, ac, accuracy):
    arr = rolling_dice(to_hit, 'arr ' + to_hit_mode, accuracy)
    xpv = rolling_dice(dmg, 'xpv ' + dmg_mode, accuracy)
    prob_sum = 0
    for i in range(len(arr)):
        if (arr[i] == len(arr) - 1) and (are_there_critical_hits == 'YES') and (i >= ac):
            prob_sum += arr[i] * (xpv * 2 - dmg.modifier_)
        elif i >= ac:
            prob_sum += arr[i] * xpv
    return round(prob_sum / sum(arr), accuracy)
