from dice_lib import *


def help():
    print('Available commands are:')
    print('add - adds dice, del - deletes dice from our list')
    print('sum - returns expected value of sum of dice, max - returns maximum value')
    print('ars - returns the array of possible outcomes when counting the sum of dice')
    print('* adv - returns expected value of throwing dice with advantage, dis - with disadvantage')
    print('rrl x - returns array of outcomes when counting the sum of dice and rerolling results less or equal than x')
    print('xpr x - returns expected value of sum of dice when rerolling results less or equal than x')
    print('* plt sum/adv/dis/rrl x - returns plot of possibilities of rolling any given number in given mode')
    print('r >=/==/<= x - returns possibility of getting result <=/==/>= than x when rolling basic dice')
    print('* for adv and dis it is necessary to have only ONE type of dice in current list of dice')


def rolling_dice():
    d = DiceRoll('')
    s = ''

    while s != 'stop':
        s = input()
        cmd = s[:3]

        if s == 'help':
            help()
            continue

        if s == 'stop':
            break

        if cmd == 'add':
            d.add(s[4:])

        if cmd == 'del':
            d.minus(s[4:])

        if cmd == 'sum':
            print('Average sum on dice:', d.average_dice())

        if cmd == 'max':
            print('Max sum on dice:', d.max_res())

        if cmd == 'ars':
            print(d.arr_sum())

        if cmd == 'r>=':
            print('Probability is', d.geqslant(int(s[4:])))

        if cmd == 'r<=':
            print('Probability is', d.leqslant(int(s[4:])))

        if cmd == 'r==':
            print('Probability is', d.eq(int(s[4:])))

        if cmd == 'adv':
            if len(d.diceN_) != 1:
                print('Cannot calculate that')
            else:
                print('Expected value is', expected_value(d.adv()))

        if cmd == 'dis':
            if len(d.diceN_) != 1:
                print('Cannot calculate that')
            else:
                print('Expected value is', expected_value(d.dis()))

        if cmd == 'rrl':
            print(d.arr_sum_reroll_less(int(s[4:])))

        if cmd == 'xpr':
            print(expected_value(d.arr_sum_reroll_less(int(s[4:]))))

        if cmd == 'plt':
            if s[4:7] == 'sum':
                plt_probability(range(d.max_res() + 1), d.arr_sum())
            elif s[4:7] == 'adv':
                if len(d.diceN_) != 1:
                    print('Cannot calculate that')
                else:
                    d.plt_max(1)
            elif s[4:7] == 'dis':
                if len(d.diceN_) != 1:
                    print('Cannot calculate that')
                else:
                    d.plt_max(-1)
            elif s[4:7] == 'rrl':
                plt_probability(range(d.max_res() + 1), d.arr_sum_reroll_less(int(s[8:])))
        d.print()


if __name__ == '__main__':
    print('If you want help, print help. If you want to stop, print stop')
    rolling_dice()
    print('Thanks for using our program! <3')
