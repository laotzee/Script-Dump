from random import choice
import os
import threading
import time

POSSIBLE_NUMS = list(range(10, 40))
VARIATION_RANGE = list(range(30, 50))
ERROR_MESSAGE = "Oh no, that's not the correct answer. It is "
CONGRATS_MESSAGE = "Excellent! that's the correct answer :)"
AWKWARD_MESSAGE ="Well, it seems you answer something rather creative"

user_seconds = []

def measure_time(stop_signal, user_time):

    counter = 0
    while not stop_signal:
        time.sleep(1)
        if len(user_time) == 0:
            counter = 0
        counter += 1

    user_time.append(counter)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def pick_nums():

    median = choice(POSSIBLE_NUMS)
    greater_variation = choice(VARIATION_RANGE) / 100
    lesser_variation = choice(VARIATION_RANGE) / 100
    greater_num = median + round(median * greater_variation)
    lesser_num = median - round(median * lesser_variation)

    greater_difference = greater_num - median
    lesser_difference = median - lesser_num

    if greater_difference > lesser_difference:
        correct_answer = greater_num
    elif lesser_num > greater_num:
        correct_answer = lesser_num
    else:
        return pick_nums()

    return {median, greater_num, lesser_num}, correct_answer

def present_to_user(nums):

    boxes = f"""                                                                        
    +---------------------+     +---------------------+     +---------------------+
    |                     |     |                     |     |                     |
    |                     |     |                     |     |                     |
    |         {nums.pop()}          |     |         {nums.pop()}          |     |         {nums.pop()}          |
    |                     |     |                     |     |                     |
    |                     |     |                     |     |                     |
    +---------------------+     +---------------------+     +---------------------+\n"""

    print(boxes)
    answer = int(input("Which number is farthest from the median?\n"))

    return answer

def evaluate_input(answer, correct_answer):

    if answer != correct_answer:
        print(ERROR_MESSAGE + str(correct_answer))
    elif answer == correct_answer:
        print(CONGRATS_MESSAGE)
    else:
        print()

if __name__ == "__main__":

    game_on = True
    while game_on:
        clear_screen()
        test_nums = pick_nums()
        user_answer = present_to_user(test_nums[0])
        evaluate_input(user_answer, test_nums[1])
        if input("") != "": game_on = False