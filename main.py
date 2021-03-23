import string


class DiceRoll:
    def __init__(self, s):
        self.diceN_ = {}
        self.add(s)

    def add(self, s):
        if s != '':
            s += ' + '
            while s != '':
                amount = int(s[:s.find('d')])
                s = s[s.find('d') + 1:]
                cap = int(s[:s.find(' ')])
                s = s[s.find('+') + 2:]
                if cap in self.diceN_:
                    self.diceN_[cap] += amount
                else:
                    self.diceN_[cap] = amount

    def minus(self, s):
        s += ' + '
        while s != '':
            amount = int(s[:s.find('d')])
            s = s[s.find('d') + 1:]
            cap = int(s[:s.find(' ')])
            s = s[s.find('+') + 2:]
            if cap in self.diceN_:
                if self.diceN_[cap] <= amount:
                    self.diceN_[cap] = 0
                else:
                    self.diceN_[cap] -= amount

    def print(self):
        s = ''
        for el in sorted(self.diceN_.items()):
            if el[1] != 0:
                s += str(el[1]) + 'd' + str(el[0]) + ' + '
        s = s[:len(s)-2]
        if s != '':
            print(s)
        else:
            print('0 cubes added')

    def return_dict(self):
        return self.diceN_

    def average_dice(self):
        sum_d = 0
        for el in self.diceN_.items():
            sum_d += el[1] * (el[0] + 1) / 2
        return int(sum_d)


d = DiceRoll('')
s = ''
print('Commands are: add, del, stop')
while s != 'stop':
    s = input()
    if s == 'stop':
        break
    if s[:3] == 'add':
        d.add(s[3:])
    if s[:3] == 'del':
        d.minus(s[3:])
    d.print()
    print('Average sum on dice:', d.average_dice())
