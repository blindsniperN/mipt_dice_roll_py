from dice_lib import *


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
            global accuracy
            check = rolling_dice(d, s, accuracy)
            if check is not None:
                print(check)
            d.print()


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
    are_there_critical_hits = input()
    if ac != -1:
        global accuracy
        print('Expected damage per attack is ', expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode,
                                                                    are_there_critical_hits, ac, accuracy))
    else:
        max_ac = 25
        arr = [0] * (max_ac + 1)
        for i in range(max_ac + 1):
            global accuracy
            arr[i] = expected_dmg_per_ac(to_hit, to_hit_mode, dmg, dmg_mode, are_there_critical_hits, i, accuracy)
        plt_probability(arr)


if __name__ == '__main__':
    print('If you want help, print help. If you want to stop, print stop')
    print('Type 0 if you want to work with dice right now. If you want to work with characters, type 1')
    if int(input()):
        character_build()
    else:
        cycle_dice()
    print('Thanks for using my program! <3')
