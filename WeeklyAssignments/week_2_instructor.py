#1. Take the sentence: All work and no play makes Jack a dull boy. 
#Store each word in a separate variable, then print out the sentence on one line using print.
print("Beginning of #1")
word1 = "All"
word2 = "work"
word3 = "and" 
word4 = "no"
word5 = "play"
word6 = "makes"
word7 = "Jack"
word8 = "a"
word9 = "dull"
word10 = "boy"
period ="."
space = " "

print(word1 + space + word2 + space + word3 + space + 
      word4 + space + word5 + space + word5 + space + 
      word7 + space + word8 + space + word9 + space + 
      word10 + period)
print("End of #1")

#2. Add parenthesis to the expression `6 * 1 - 2` to change its value from `4` to `-6`.
print("Beginning of #2")

print ("6 * 1 - 2")
print (6 * 1 - 2)

print ("6 * (1 - 2)") # will do what is in parenthesis first
print (6 * (1 - 2))

print("End of #2")

#3. Place a comment before a line of code that you previously worked, and record what happens when you rerun the program.
print("Beginning of #3")
print("If I put a comment before line 30 it will not print the math problem in the interpreter and I will not get the answer -6")
print("End of #3")

#4.Start the Python interpreter and enter `bruce + 4` at the prompt. This will give you an error:
#```python
#NameError: name 'bruce' is not defined
#```
#Assign a value to bruce so that `bruce + 4` evaluates to `10`.
print("Beginning of #4")

print("bruce = 6")
bruce = 6
print("bruce + 4")
print(bruce + 4)

print("End of #4")

#5. The formula for computing the final amount if one is earning compound interest is given on Wikipedia as
#![Compounded Interest Formula](assets/compound_interest_formula.png)
#Write a Python program that assigns the principal amount of $10000 to variable `P`, assign to n the value `12`, and assign to `r` the interest rate of 8%. Then have the program prompt the user for the number of years `t` that the money will be compounded for. 
#Calculate and print the final amount after `t` years.
print("Beginning of #5")

# Get principal amount
P = 10000

#Get the compounding frequency per year
n = 12 #monthly

# Get interest rate
r = .08 #8%

# Get time in years
t = int(input("How many years to calculate?"))

P1 = P * (1 + (r/n)) ** (n*t)

print("Amount with interest after {} years: ${:.2f}".format(t, P1))

print("End of #5")

# 6. Evaluate the following numerical expressions in your head, then use the Python interpreter to check your results:

# ```python
# >>> 5 % 2
# >>> 9 % 5
# >>> 15 % 12
# >>> 12 % 15
# >>> 6 % 6
# >>> 0 % 7
# >>> 7 % 0
# ```

# What happened with the last example? 
# #Why? 
# If you were able to correctly anticipate the computer’s response in all but the last one, it is time to move on. 
# If not, take time now to make up examples of your own. 
# Explore the modulus operator until you are confident you understand how it works.

print("Beginning of #6")

print("5 % 2 returns {}".format(5 % 2))
print("9 % 5 returns {}".format(9 % 5))
print("15 % 12 returns {}".format(15 % 12))
print("12 % 15 returns {}".format(12 % 15))
print("6 % 6 returns {}".format(6 % 6))
print("0 % 7 returns {}".format(0 % 7))
print("7 %% 0 returns ZeroDivisionError: integer division or modulo by zero")

print("End of #6")


#7. You look at the clock and it is exactly 2pm. 
# You set an alarm to go off in 51 hours. 
# At what time does the alarm go off? 
# _(Hint: you could count on your fingers, but this is not what we’re after. 
# If you are tempted to count on your fingers, change the 51 to 5100.)_

print("Beginning of #7")
now = 14
alarm = now + 51

answer = alarm % 24

print("The alarm will go of at {}:00 hours".format(answer)) #Using military time to keep this simple

print("End of #7")

#8. Write a Python program to solve the general version of the above problem. 
# Ask the user for the time now (in hours), and ask for the number of hours to wait. 
# Your program should output what the time will be on the clock when the alarm goes off.

print("Beginning of #8")

now = int(input("What hour of the day is it now?  Ex: 2 PM would be 14 (the 14th hour)"))
alarm = now + int(input("How many hours from now should we set the alarm for?"))
answer = alarm % 24

print("The alarm will go of at {}:00 hours".format(answer)) #Using military time to keep this simple


print("End of #8")

#9. What is the Python interpreter's response to the following?
# ```python
# >>> list(range(10, 0, -2))
# ```
#   The three arguments to the *range* function are *start*, *stop*, and *step*, respectively. 
#   In this example, `start` is greater than `stop`.
#    What happens if `start < stop` and `step < 0`? 
#   Write a rule for the relationships among `start`, `stop`, and `step`.

print("Beginning of #9")
answer = list(range(10, 0, -2))
print("The python interpreter read list(range(10, 0, -2)) as: {}".format(answer))

answer = list(range(-10, 0, -2))
print("The python interpreter read list(range(-10, 0, -2)) as: {}".format(answer))
print("A rule should be applied so that if step is less than zero that the start value must be greater than the stop value.")
print("Likewise a rule should be applied so that if step is greater than zero that the start value must be less than the stop value.")
print("The step value should not be zero.")

print("End of #9")

#10.  Draw a state snapshot for `a` and `b` before and after the third line of the following Python code is executed:

# ```python
# a = [1, 2, 3]
# b = a[:]
# b[0] = 5
# ```
print("Beginning of #10")

a = [1, 2, 3]
print("a = [1, 2, 3]")

b = a[:]
print("b = a[:]")

print("The current value of a is: {} and b is: {}".format(a,b))

b[0] = 5
print("b[0] = 5") # We assigned the value 5 to the first element in the list

print("The updated value of a is: {} and b is: {}".format(a,b))

print("End of #10")


#11.  What will be the output of the following program?

# ```python
# this = ["I", "am", "not", "a", "crook"]
# that = ["I", "am", "not", "a", "crook"]
# print("Test 1: {0}".format(this is that))
# that = this
# print("Test 2: {0}".format(this is that))
# ```
#Provide a *detailed* explanation of the results.

print("Beginning of #11")

this = ["I", "am", "not", "a", "crook"]
that = ["I", "am", "not", "a", "crook"]
print("Test 1: {0}".format(this is that))
that = this
print("Test 2: {0}".format(this is that))

print("The first test compared to see if the two lists were the same thing. They are not.")
print("The second test returned true because in between the two tests we made this equal to that, or in other words we made them the same thing.")

print("End of #11")