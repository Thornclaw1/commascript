# commascript

## Set Up

---

Once you have cloned or downloaded the repo, you'll want to open up the file called cs.sh.

Inside of this file, you will see this line `python ~/dev/personal/commascript/interpreter.py $1 $2`.

Edit this file path so that it matches your path to the `interpreter.py` file, starting in your home directory. Leave the `python` and `$1 $2` as is. And don't forget to include the `~/` at the beginning.

> Tip: you can use the command `pwd` to print your working directory.

Now in your terminal, go to your root folder via `cd ~` and type `nano .bashrc`.
Add this line to the file that opens: `alias cs="/Users/cameronfletcher/dev/personal/commascript/cs.sh"` replacing the file path with your own once again

> Take note that this file path requires you to start with the `Users` directory, unlike the first one.

Then press `^O ^X`, to write it out and close the file.

Now you can make a CommaScript file anywhere and run it with the command `cs file_name.cscr`

---

## Primitive Types

| Type    | Values                   | Examples          |
| ------- | ------------------------ | ----------------- |
| int     | any whole number         | 14, 230           |
| float   | any decimal number       | 52.13, 3.1415     |
| string  | any string of characters | "Hello", 'World!' |
| boolean | True or False            | T, F              |

---

## Writing the Infamous Hello World Program

Start by making a new file. You can call it whatever you want, but make sure add the _.cscr_ file extension.

Now to run the file, you will type `cs name_of_file.cscr`, and you will see it output 'Hello World!' to the console.

Congratulations! You wrote your first CommaScript script.

In this coding language, an empty file will automatically print out 'Hello World!'.

But if you want to do it manually here's the code:

```py
p<"Hello World!">
```

Let's break this down.

The 'p' is the function for printing things to the console, and the angle brackets are what you use to surround the arguments you want to pass in.

So we pass "Hello World!" into the print function, and it prints it out to the screen! Pretty simple, right?

---

## Getting Input from the User

Let's make a more interesting program, let's get input from the user, and print it out with some flavor text.

We will start with getting input.

```py
i<"Enter your name: ">
```

'i' is the function for obtaining input, and once again we are passing in a string. The string we pass in will be used as the prompt given to the user.

This function then returns the string that the user types in.

Now you may be wondering how we obtain this value and store it in a variable to use later. And that is actually handled automatically! When writing a statement like `2 + 2`, `"Hello"`, any function that has a return value, or pretty much anything else, it will be automatically stored in memory.

Now let's get to using the string that the user passed in. Memory is stored in a list of sorts, and to retrieve them, you use the keyword `m` followed by the index of the value you want to retrieve. So to obtain our inputed string, we will use the following syntax `m0`.

Let's print out the string with some added flavor.

```py
i<"Enter your name: ">,
p<"Hello " + m0 + "!">
```

Note that I added a comma after the first line. This is what is used to split statements. In this language, spaces don't matter, and thus the comma is necessary to tell the program that we want two different statements.

Inside the print function, we are using string concatenation to join the three strings together.

Now if you run this program, it will prompt you for your name, and then print out 'Hello _name_!"

---

## Casting

Casting is fairly simple. You can cast between all four primitive types: string, int, float, and boolean.

Using the functions `cs`, `ci`, `cf`, and `cb`, you can cast to the different primitive types. More info on these functions in the Built-in Functions section below.

---

## Conditionals

Here is an example of an if statement:

```py
? 5 = 4:
    p<"5 is equal to 4">
;
```

> Remember that the spaces, including the tab, are unnecessary, but are included for readability

The question mark is used to tell the program to check if the following statement evaluates to true. The colon then starts the if block, and the semi-colon concludes the block.

Statements inside of the block follow the same rules as outside of the block. As such, you must separate statements with a comma if you have more than one.

Let's add an else statement to this code.

```py
? 5 = 4:
    p<"5 is equal to 4">
; e:
    p<"5 is not equal to 4">
;
```

`e` is the keyword for else, and like the if statement, the colon starts the block and the semi-colon concludes the block.

> You may have noticed that there is no comma between the if statement and the else statment, and that is because chains of if, else-if, and else are considered one statment

Let's spice it up with an else-if thrown into the pot.

```py
? 5 = 4:
    p<"5 is equal to 4">
; e? 5 = 6:
    p<"5 is equal to 6">
; e:
    p<"5 is not equal to 4 or 6">
;
```

All it takes is adding a `?` right after the `e` and now you can check another conditional.

Now you may be wondering what conditional operators you have access to. Here's the list:

| Condition             | op  |
| --------------------- | :-: |
| Equal to              |  =  |
| Not Equal to          | !=  |
| Less Than             | =-  |
| Greater Than          | =+  |
| Less Than or Equal    | =-= |
| Greater Than or Equal | =+= |
| And                   |  &  |
| Or                    | \|  |
| Not                   |  !  |

And while we are at it, here's the mathmatical operators:

| Binary Operators |  op  |
| ---------------- | :--: |
| Plus             |  +   |
| Minus            |  -   |
| Multiply         |  \*  |
| Divide           |  /   |
| Integer Divide   |  //  |
| Modulo           |  %   |
| Exponent         | \*\* |

| Unary Operators | op  |
| --------------- | :-: |
| Positive        |  +  |
| Negative        |  -  |

---

## While Loops

While loops work similarly to if statments, but they run the code inside of the block continuously until the conditional no longer evaluates to true. Here's an example:

```py
5,
?? m0 =+ 0:
    p<m.0>,
    s.0 => m.0 - 1
;
```

> You can find this script, `countdown.cscr`, in the `example_scripts` folder

Now there is quite a lot to digest here, so let's break it down.

On line 1, we start by storing the number 5 in memory.

Line 2 starts with `??`, which is the keyword for while. We then define the conditional, `m0 =+ 0`. This states that the while loop will run as long as the value at the 0th index in memory is greater than 0.

Now line 3 is where it gets more interesting. You'll notice that we have a print function, with the argument of `m.0`. To explain this, you will need to understand how scope works in this language.

Every time you enter into a new block of code, you enter a new scope as well. This means that any variables that get defined inside of blocks, get defined within that blocks scope. So that brings up the question, how do you access memory outside of the current scope? That's where `.`'s come in. For every `.` in between `m` and the index, you go up one scope.

So now you can see that `m.0` inside the loop, is just getting the 0th index in memory from the enclosing scope.

> Both the `m0` from the conditional and the `m.0` from inside the while loop are getting the same variable

The next line is also interesting. `s` is what is used to reassign a variables value. It works similarly to `m`, but instead of getting, it sets. When setting variables you use the same syntax as getting variables to tell the program what scope and what index to look at. Then you follow it up with the 'set to' keyword `=>`, and the value you want to set it to.

So our line of `s.0 => m.0 - 1` is setting the 0th index of memory in the outer scope, to that same value minus 1.

This while loop will run 5 times, each time printing out a number. The output should look like this:

```
5
4
3
2
1
```

---

## Collections

If you've ever coded in another language, these should look familiar.

### Lists

```py
[2,4,5,7,3]
```

### Dictionaries

```py
{'john':4, 'jane':3}
```

The above statments are all the syntax you need to create lists and dictionaries, and using `m`, you can obtain the whole list or dictionary object later in the code.

To obtain a single value out of these collections, you use what is called an indexer. Using square brackets, you can obtain values with indexes or keys. Here are some examples:

```py
[2,4,5,7,3],
m0[2], # 5 #
m0[0]  # 2 #
```

```py
{'john':4, 'jane':3},
m0['john'], # 4 #
m0['jane']  # 3 #
```

To modify these collections, there are three functions you can use: `a`, `rm`, and `rmv`. Add, Remove, and Remove by Value, respectively. I suggest reading the documentation on those functions down below in the section labeled Built-in Functions.

---

## For Loops

For loops are similar to while loops, but instead of waiting for a condintional to no longer evaluate to true, it loops over an iterable object. The iterable objects it supports are as follows: list, dictionary, string, and even int. Here are some examples:

```py
["This", "is", "some", "important", "info"],
?/m0:
    p<m0>
;
# > This        #
# > is          #
# > some        #
# > important   #
# > info        #
```

```py
?/["This", "is", "some", "important", "info"]:
    p<m0>
;
# > This        #
# > is          #
# > some        #
# > important   #
# > info        #
```

```py
?/{'john':2,'jane':4,'doe':6}:
    p<m0>
;
# > john  #
# > jane  #
# > doe   #
```

```py
?/"Hello":
    p<m0>
;
# > H  #
# > e  #
# > l  #
# > l  #
# > o  #
```

As you may have guessed, `?/` is the keyword for for. It then takes in the iterable, either through a variable, or as a literal. Then the colon opens the block, and the semi-colon closes it. When iterating over the iterable, the value it is currently evaluating gets set in memory as m0, so you can access each element that way.

Now you may remember that I mentioned that you could iterate over integers. And the way this works is it essentially tells the loop how many times to run the enclosed block of code. Here's an example of that:

```py
?/4:
    p<m0>
;
# > 0 #
# > 1 #
# > 2 #
# > 3 #
```

When looping with an integer, it will set m0 to the current loop count minus 1

> You can think of it like doing `for i in range(4)` in python, because that's exactly what it's doing behind the scenes.

Now there's actually one more think that you can iterate over, and it is booleans. The reason for this is because it reads True and False as 1 and 0 respectively. This functions pretty much exactly the same as an if statement without the ability to chain else-if statements. You do, however, get the added bonus of having a 0 automatically stored for you, if you wanted that for some reason. It serves very little purpose as a feature, but maybe somebody will find a use case for it.

---

## Creating Custom Functions

Creating a function is fairly simple. Here's a couple of examples:

```py
2:
    p<m0, m1>
;
```

```py
:
    p<"Hello there!">
;
```

To create a function, you specify the number of parameters followed by a colon to start the function block. And once again a semi-colon is used to conclude the function block.

Now you may notice that on the second example, no number was provided for the number of parameters. That is because if you don't want any parameters to be passed in to the function, rather than typing 0, you can simply just omit the number entirely.

The values passed to the functions will automatically be stored in that functions scope, so obtaining them is no different than before. In the first example, the function takes 2 arguments, and automatically stores them in the 0th and 1st place in the functions scope. So when it gets to `p<m0, m1>`, it's taking both arguments passed in and printing them to the screen.

Let's get to calling these functions. Calling custom functions is the same as calling built-in functions, except instead of using the function names, you are using the functions place in memory, as custom functions are nameless. Here are some examples:

```py
2:
    p<m0, m1>
;,
m0<"Hello", "World!">
# > Hello World! #
```

```py
:
    p<"Hello there!">
;,
m0<>,
# > Hello there! #
m0
# > Hello there! #
```

> Just like how you can omit the number if there are no parameters, you can omit the angle brackets if you aren't passing anything in.

---

## Importing Other CommaScript Files

As we all know, the larger your project becomes, the harder it is to maintain. And while hard to maintain was one of the goals of this project, I thought it only fair to allow for some organization. This also allows for modules to be built and be used in many different projects.

So how do you go about importing files? Well it's fairly simple. Using an `@` sign followed by the relative file path in quotes will import the file.

```py
@'file_path.cscr'
```

> When the program imports another file, it will run that file automatically.

To obtain access to the imported files memory, you use a `$` followed by the index of the module. You can then use `m` and `s` to get variables, call functions, and set variables on the other script.

file1.cscr

```py
2:
    m0 * 2,
    r<m2 + m1>
;,
:
    p<"Hello World!">
;
```

main.cscr

```py
@'file1.cscr',
$0m0<4, 1>, # 9 #
$0m1 # > Hello World! #
```

> Note: imports don't get stored in memory, so in the above file, `main.cscr`, only one variable gets stored, which is `9`.

---

## Built-in Functions

### Function Syntax

```py
function_name<arg, ...>
```

---

### P

Prints out to the screen

If passed more than one argument, it will separate them with a space

#### Examples

```py
p<"Hello World!">
# > Hello World! #

p<"Hello", "World!">
# > Hello World! #
```

---

### I

Takes input from the user

#### Example

```py
i<"Enter a number: ">
```

---

### RND

Generates a random integer between the two passed arguments

#### Example

```py
rnd<4,8> # 6 #
```

---

### CS

Casts the passed value to a string and returns the result

#### Example

```py
cs<540> # "540" #
```

---

### CI

Casts the passed value to an int and returns the result

#### Example

```py
ci<"138"> # 138 #
```

---

### CF

Casts the passed value to a float and returns the result

#### Example

```py
cf<"42.14"> # 42.14 #
```

---

### CB

Casts the passed value to a bool and returns the result

#### Examples

```py
cb<"string">, # True #
cb<234>, # True #
cb<0> # False #
```

---

### R

Exits the function and gives it the return value of the passed value

#### Example

```py
2:
    r<m0 + m1>
;,
m0<4, 5> # 9 #
```

---

### A

Appends, inserts, or modifies an item in a list or dictionary

#### Parameters

<dl>
    <dt>
    list, element
    </dt>
    <dd>
    adds the element to the list
    </dd>
    <dt>
    list, index, element
    </dt>
    <dd>
    inserts the element at the index in the list
    </dd>
    <dt>
    dictionary, key, value
    </dt>
    <dd>
    adds or modifes the key to the value in the dictionary
    </dd>
</dl>

#### Examples

```py
[1,2,3],
a<m0,4>, # [1,2,3,4] #
a<m0,2,5> # [1,2,5,3,4] #
```

```py
{'john':2,'jane':4},
a<m0,'doe',6>, # {'john':2,'jane':4,'doe':6} #
a<m0,'john',10> # {'john':10,'jane':4,'doe':6} #
```

---

### RM

Removes an index/key from a list or dictionary

#### Examples

```py
['john','jane','doe'],
rm<m0,1> # ['john','doe'] #
```

```py
{'john':2,'jane':4,'doe':6},
rm<m0,'jane'> # {'john':2,'doe':6} #
```

---

### RMV

Removes an element/value from a list or dictionary

#### Examples

```py
['john','jane','doe'],
rmv<m0,'jane'> # ['john','doe'] #
```

```py
{'john':2,'jane':4,'doe':6},
rmv<m0,4> # {'john':2,'doe':6} #
```

---

### L

Returns the length of a list, dictionary, string, or number

#### Examples

```py
['john','jane','doe'],
l<m0> # 3 #
```

```py
{'john':2,'jane':4,'doe':6},
l<m0> # 3 #
```

```py
"Hello World!",
l<m0> # 12 #
```

```py
1252,
l<m0> # 4 #
```

```py
53.12,
l<m0> # 5 #
```

---

## Using Python's built-in functions

Using `^`, you can call all of [python's built-in functions](https://docs.python.org/3/library/functions.html)

> When calling Python's built-in functions, unless they are nested within another statement, they will always store the return value in memory, regardless of whether the function actually returns a value or not. For example, calling Python's print will store None in memory, while calling CommaScript's print will not.

### Python Function Syntax

```py
^function_name<arg, ...>
```

#### Examples

```py
^print<"Hello World!">
# > Hello World! #
```

```py
^input<"Enter your name: ">
```

```py
^all<[T, T, T]>, # True #
^all<[T, F, T]> # False #
```

```py
^sorted<[4,2,5,3,234,65,2]> # [2, 2, 3, 4, 5, 65, 234] #
```
