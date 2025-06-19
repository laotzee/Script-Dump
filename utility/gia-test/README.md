# GIA Test Tool

This script helps practicing the math part of the GIA test, or General Intelligence Assessment. It presents to the user 3 numbers, and ask to select the furthest one from the median. 

# How to use

Using Python3, run main.py, and the practice begins. Once you guess, the program will give you feedback on the answer and wait for the user to press Enter to continue with the following set of numbers. If anything other than empty is given as input, the program will end. 

# Customize ranges

The practice difficulty can be adjusted by the handles POSSIBLE_NUMS and VARIATION_RANGE. The former dictates the numbers that can be set as median, while the latter indicates the percentage of variation between the upper and lower numbers.

By default, the median is set between 10 and 39, and the variation is set between 30 and 50 percent. 

# How variation range affects practice

If you want to practice longer mental maths, you would keep the variation within a wider range, however, it would be easier to spot numbers that greatly differ, thus making the answer obvious. For this purpose, I find (30,50) range great.

Keeping the range lower makes for an easier mental math operation, you have to work with less quantity, although that easiness to spot significant differences is absent. 
