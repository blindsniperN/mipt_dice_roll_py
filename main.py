from dice_lib import *
from numpy import percentile


accuracy = 3


def print_help():
    print('Available commands are:')
    print('add - adds dice, del - deletes dice from our list')
    print('max - returns maximum value of dice')
    print('xpv sum/adv/dis/rrl x/bmb d - returns expected value of outcomes')
    print('r>=/==/<= sum/adv/dis/rrl x/bmb d y - returns possibility of result <=/==/>= than x when rolling dice')
    print('arr sum/adv/dis/rrl x/bmb d - returns the array of possible outcomes')
    print('prb sum/adv/dis/rrl x/bmb d - returns the array of probabilities')
    print('plt sum/adv/dis/rrl x/bmb d - returns plot of possibilities of rolling any given number in given mode')
    print('rll sum/adv/dis/rrl x/bmb d - returns the result of the roll in given mode')
    print('prc sum/adv/dis/rrl x/bmb d y - returns the y percentile')
    print('acc x - change accuracy of non-integer numbers to x')
    print('* for adv and dis it is necessary to have only ONE type of dice in current list of dice')
    print('** bmb works only if there is ONE dice of ONE type in current list of dice. Also there is depth parameter')
#  bmb - взрывные кубы из ведьмака


def cycle_dice():
    d = DiceRoll('')
    while True:
        s = input()
        if s == 'stop':
            break
        elif s == 'help':
            print_help()
        elif s[:3] == 'acc':
            global accuracy
            accuracy = int(s[4:])
        else:
            check = rolling_dice(d, s)
            if check is not None:
                print(check)
            d.print()


def prob_preparation(d, s):  # предобработка кубов для команд r>=, r==, r<=
    y = 0
    arr = []
    if s[4:7] == 'sum':
        arr = d.arr_sum()
        y = int(s[8:])
    elif s[4:7] == 'adv':
        arr = d.adv()
        y = int(s[8:])
    elif s[4:7] == 'dis':
        arr = d.dis()
        y = int(s[8:])
    elif s[4:7] == 'rrl':
        x, y = map(int, s[8:].split())
        arr = d.arr_sum_reroll_less(x)
    elif s[4:7] == 'bmb':
        x, y = map(int, s[8:].split())
        arr = d.bmb(x)
    return [arr, y]


def preparation(d, s):  # предобработка кубов для прочих команд
    arr = []
    if s[4:7] == 'sum':
        arr = d.arr_sum()
    elif s[4:7] == 'adv':
        arr = d.adv()
    elif s[4:7] == 'dis':
        arr = d.dis()
    elif s[4:7] == 'rrl':
        x = int(s[8:])
        arr = d.arr_sum_reroll_less(x)
    elif s[4:7] == 'bmb':
        arr = d.bmb(int(s[8:]))
    return arr


def rolling_dice(d, s):
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
        res = geqslant(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r<=':
        arr, y = prob_preparation(d, s)
        res = leqslant(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'r==':
        arr, y = prob_preparation(d, s)
        res = eq(arr, d.modifier_, y)
        if res is not None:
            return 'Probability is ' + str(round(res, accuracy))

    elif cmd == 'xpv':  # мат ожидание
        res = expected_value(preparation(d, s))
        if res is not None:
            return round(res, accuracy)

    elif cmd == 'prb':
        return turn_to_probability(preparation(d, s), accuracy)

    elif cmd == 'plt':
        plt_probability(turn_to_probability(preparation(d, s), accuracy))

    elif cmd == 'rll':
        return roll(preparation(d, s))

    elif cmd == 'prc':
        arr, y = prob_preparation(d, s)
        if arr is not None:
            return str(y) + '% percentile is: ' + str(percentile(arr, y))


def expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode, crit, ac):
    arr = rolling_dice(to_hit, 'arr ' + to_hit_mode)
    xpv = rolling_dice(dmg, 'xpv ' + dmg_mode)
    prob_sum = 0
    for i in range(len(arr)):
        if (arr[i] == len(arr) - 1) and (crit == 'YES') and (i >= ac):
            prob_sum += arr[i] * (xpv * 2 - dmg.modifier_)
        elif i >= ac:
            prob_sum += arr[i] * xpv
    return round(prob_sum / sum(arr), accuracy)


def character_build():
    print('Enter dice just as in the dice mode, first line - amount, second line - how you want to roll them')
    print('Start by entering the dice to hit of the character: ')
    to_hit = DiceRoll(input())
    to_hit_mode = input()
    print('Enter damage dice per attack: ')
    dmg = DiceRoll(input())
    dmg_mode = input()
    print('Enter the AC of the monster - if you want to plot it, enter -1')
    ac = int(input())
    print('Enter YES if your system includes doubling dmg on a critical hit ')
    crit = input()
    if ac != -1:
        print('Expected damage per attack is ', expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode, crit, ac))
    else:
        max_ac = 25
        arr = [0] * (max_ac + 1)
        for i in range(max_ac + 1):
            arr[i] = expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode, crit, i)
        plt_probability(arr)


if __name__ == '__main__':
    print('If you want help, print help. If you want to stop, print stop')
    print('Type 0 if you want to work with dice right now. If you want to work with characters, type 1')
    if int(input()):
        character_build()
    else:
        cycle_dice()
    print('Thanks for using my program! <3')
