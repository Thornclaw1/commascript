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

## Built-in Functions

### Function Syntax

```
function_name<arg, ...>
```

---

### P

Prints out to the screen

If passed more than one argument, it will separate them with a space

#### Examples

```py
p<"Hello World!">
# > Hello World!

p<"Hello", "World!">
# > Hello World!
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
