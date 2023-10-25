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
| null    | Null                     | X                 |

---

## Writing the Infamous Hello World Program

Start by making a new file. You can call it whatever you want, but make sure to add the _.cscr_ file extension.

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

> Note: Function calls of functions created in CommaScript will automatically be stored in memeory regardless of whether it has a return value. If there is no return value, it will be set to Null

You can also explicitly tell the program to store a variable using the set (`=>`) operator. Here's an example of that:

```py
=> 2 + 4,
=> "Hello World!"
```

The memory table will function exactly the same, but this can be used to force a variable to be stored when it normally wouldn't, or just to make the code base more readable.

Along with explicitly telling the program to store a variable, you can also tell the program to not store a variable. This is especially useful for macros and custom functions that don't return anything. If you put Null (`X`) in front of the set (`=>`) operator, it will tell the program to not store the result of that statement. Here's an example:

```py
x => 2 + 4,
x => "Hello World!"
```

Using this to "discard" the result can help clean up the memory table, and prevent unwanted side-effects. In this case, we are just telling the program to not store the two statements as variables

Now let's get to using the string that the user passed in. Memory is stored in a list of sorts, and to retrieve them, you use the keyword `m` followed by the index of the value you want to retrieve. So to obtain our inputed string, we will use the following syntax `m0`.

> Note: The index can be negative and works like pythons negative index getters for lists, dictionaries, etc. The syntax is no different, just put a minus sign (`-`) before the index like so: `m-1`. Using `m-1` will get the last stored variable, `m-2`, the second to last stored variable, and so on.

Let's print out the string with some added flavor.

```py
i<"Enter your name: ">,
p<"Hello " + m0 + "!">
```

Note that I added a comma after the first line. This is what is used to split statements. In this language, spaces don't matter, and thus the comma is necessary to tell the program that we want two different statements.

Inside the print function, we are using string concatenation to join the three strings together.

Now if you run this program, it will prompt you for your name, and then print out 'Hello _name_!"

---

## Formatted Strings

Formatted strings are a type of string that allow you to embed CommaScript expressions inside of them.

To create a formatted string, instead of using quotes (`'`) or double quotes (`"`), you use backticks (`` ` ``).

To embed an expression inside of a formatted string, you surround the expression with curly braces.

Here's an example of a formatted string:

```py
i<"What's your name? ">,
p<`Hello {m0}! How are you doing?`>
```

The formatted string will insert, at `{m0}`, what ever was inputed by the user before printing it out to the console.

There is no limit to the amount of embedded expressions you can put into a formatted string.

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
| Less Than             | <\  |
| Greater Than          | >\  |
| Less Than or Equal    | <=  |
| Greater Than or Equal | >=  |
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
?? m0 >\ 0:
    p<m.0>,
    s.0 => m.0 - 1
;
```

> You can find this script, `countdown.cscr`, in the `example_scripts` folder

Now there is quite a lot to digest here, so let's break it down.

On line 1, we start by storing the number 5 in memory.

Line 2 starts with `??`, which is the keyword for while. We then define the conditional, `m0 >\ 0`. This states that the while loop will run as long as the value at the 0th index in memory is greater than 0.

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

## Changing Variable Values

When it comes to changing the value of previously declared variables, there are 5 different options. All of which start with the same syntax.

Using `s`, the keyword for setting, followed by any number of periods (`.`), and then an integer for the index, tells the program that you want to set the variable in the corresponding scope and index. The number of periods determines how many scopes out of the current scope you want to search. The integer is the index of the value you want from the scopes memory table.

From here is where you have multiple options: `=>`, `+`, `-`, `++`, `--`.

`=>` Allows you to set the value directly.

```py
0,
p<m0>,
# > 0 #
s0 => 22,
p<m0>
# > 22 #
```

`+` Allows you to set the value to the current value plus another value.

```py
143,
p<m0>,
# > 143 #
s0 + 20,
p<m0>
# > 163 #
```

`-` Allows you to set the value to the current value minus another value.

```py
143,
p<m0>,
# > 143 #
s0 - 20,
p<m0>
# > 123 #
```

`++` Will increment the value by `1`.

```py
3,
p<m0>,
# > 3 #
s0++,
p<m0>
# > 4 #
```

`--` Will decrement the value by `1`.

```py
19,
p<m0>,
# > 19 #
s0--,
p<m0>
# > 18 #
```

All of the binary operation rules apply so you can use the set `+` to concatenate two strings, but you cannot add an integer to a string. This also means that `++` and `--` only work on integers and floats.

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

### Tuples

```py
(5,2,9,67)
```

The above statments are all the syntax you need to create lists, dictionaries and tuples, and using `m`, you can obtain the whole collection object later in the code.

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

> Note: Tuples are immutable, which means you can not modify the collection after creating it.

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

## Break

Using the keyword `b`, you can break out of both while and for loops. Here's some examples:

```py
4,
?? m0 >\ 0:
    p<m.0>,
    ? m.0 = 2:
        b
    ;,
    s.0 => m.0 - 1
;
# > 4 #
# > 3 #
# > 2 #
```

```py
?/6:
    p<m0>,
    ? m0 = 2:
        b
    ;
;
# > 0 #
# > 1 #
# > 2 #
```

---

## Continue

Using the keyword `c`, you can stop a current run through a loop and continue on to the next.

```py
?/20:
    ? m0 % 2 = 0:
        c
    ;,
    p<m0>
;
```

This will print the numbers 0 to 19, skipping all even numbers.

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

### Return Statements

Return statements are statements that can only be used when inside of a function block.

Using these statements allows you to return values out of functions to be used else where.

Here's an example:

```py
2:
    m0 + m1 * m0,
    r<m2>
;,
m0<5,8>,
p<m1>
# > 45 #
```

The return statement has the syntax of a function call. In this example, we are passing 5 and 8 to the function, it's doing some math, and then returning the result. That result then get's stored in memory, and then we are printing it out.

### Default Values

When creating functions, you can add default values for your parameters.

Here's an example:

```py
1||'Hello world!':
    ?/m0:
        p<m.1>
    ;
;,
m0<5>,
m0<5,'Hello friend!'>

# > Hello world! #
# > Hello world! #
# > Hello world! #
# > Hello world! #
# > Hello world! #
# > Hello friend! #
# > Hello friend! #
# > Hello friend! #
# > Hello friend! #
# > Hello friend! #
```

Putting `||` after the number of parameters, allows you to add more parameters with the default values specified. So this function has a total of 2 parameters, one is required, and the other will default to `'Hello world!'` if not passed in.

> Like before, omiting the number before `||` is the same as putting a `0`.

The default value can even be obtained from a variable. The following code does the same thing as the code shown above, but uses a variable getter to obtain the default value.

```py
'Hello world!',
1||m0:
    ?/m0:
        p<m.1>
    ;
;,
m1<5>,
m1<5,'Hello friend!'>
```

---

## Passing Functions as Variables

To pass a function as a variable, you can prefix the function with a `~`.

For example:

```py
1:m0<25>;,
m0<~p>
# > 25 #
```

Inside of the function taking a function as a parameter, you can reference it like normal and pass values into it to call the passed in function.

You can also pass around custom functions in the same manner.

```py
1:m0<25>;,
1:p<m0*2>;,
m0<~m1>
# > 50 #
```

## Macros

Macros are similar to functions, but they run within the scope they are called from instead of their own. Macros can cause seemingly weird behaviors if you don't fully know how they work. They can access variables, create variables, and pretty much anything else you can do outside of macros, you can do inside macros. They are also somewhat unstable, as they rely on runtime error checking for variable getting, as they have no knowledge on what variables they have access to beforehand.

The syntax of a macro is as follows, a right angle bracket (`>`) followed by a colon (`:`) to start the macro block and then a semicolon (`;`) to close the macro block. Here's an example of a macro that just prints out "Hello World":

```py
>:
    p<"Hello World">
;,
m0
```

You can put return, break, and continue statements inside of macros and they will affect the scope from which it is called.

Just like functions, Macros can take in parameters, including support for default valued parameters. But in order to access them you have to use the macro specific variable getter `k`. It works exactly the same as `m`, but without scope advancing (`.`). While in the macro, you can access the parameters using `k` without the need to worry about what scope you are in.

Check the `macro_auth.cscr` example script for a more complex example.

---

## Manipulating Files

Reading and Writing files can be a very useful tool when creating a variety of programs. Opening files in CommaScript uses three different keywords, `fr`, `fw` and `fa`. Using these keywords, it allows you to open the file in different modes, reading (`fr`), writing (`fw`) and appending (`fa`). Here are some examples:

```py
fr "test.txt":
    # file reading code goes here #
;
```

```py
fw "test.txt":
    # file writing code goes here #
;
```

```py
fa "test.txt":
    # file appending code goes here #
;
```

The file pointer gets saved in memory so you can access it while within the block using `m0`. The file will be automatically closed when leaving the block of code.

Opening the file for reading allows you to use the function `rf<>` to read the contents, and opening the file for writing or appending allows you to use the function `wf<>` to write or append to the file.

When opening in write mode, if the file does not exist, it will be automatically created. This is the only file mode that can create files.

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
x => $0m1 # > Hello World! #
```

> Note: imports don't get stored in memory, so in the above file, `main.cscr`, only one variable gets stored, which is `9`.

---

## Built-in Functions

### Function Syntax

```py
function_name<arg, ...>
```

---

### Dot Notation Syntax

```py
obj.function_name<arg, ...>
```

You can use any function (including custom made ones, and imported functions) with this syntax instead of the prior. Using this syntax will pass `obj` as the first argument into the function.

For example:

```py
[1,2,3],
m0.a<4>
```

---

### p<\*obj>

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

### i\<prompt>

Takes input from the user

#### Example

```py
i<"Enter a number: ">
```

---

### rnd\<min, max, count=1, unique=False>

Generates a random integer between the min and max integers and returns it. If `count` is set to a number higher than 1, it will instead return a list of numbers of `count` length. If `unique` is then set to True, it will ensure the numbers generated are distinct. If more numbers are requested than the range provides and `unique` is set to True, it will just return as many as it can.

#### Examples

```py
rnd<4,8> # 6 #
```

```py
rnd<1,5,4> # [2,4,2,3] #
```

```py
rnd<1,5,4,T> # [3,1,2,4] #
```

---

### lrnd\<collection, count=1, unique=False>

Returns a random element from the provided list. If `count` is set to a number higher than 1, it will instead return a list of elements of `count` length. If `unique` is then set to True, it will ensure the elements selected are distinct. If more elements are requested than the length of the list and `unique` is set to True, it will just return as many as it can.

#### Examples

```py
lrnd<[1,4,6,34,2]> # 34 #
```

```py
lrnd<[1,4,6,34,2],4> # [4,34,2,4] #
```

```py
lrnd<[1,4,6,34,2],4,T> # [4,34,2,1] #
```

---

### cs\<obj>

Casts the passed value to a string and returns the result

#### Example

```py
cs<540> # "540" #
```

---

### ci\<obj>

Casts the passed value to an int and returns the result

#### Example

```py
ci<"138"> # 138 #
```

---

### cf\<obj>

Casts the passed value to a float and returns the result

#### Example

```py
cf<"42.14"> # 42.14 #
```

---

### cb\<obj>

Casts the passed value to a bool and returns the result

#### Examples

```py
cb<"string">, # True #
cb<234>, # True #
cb<0> # False #
```

---

### r\<return_val>

Exits the function and gives it the return value of the passed value

#### Example

```py
2:
    r<m0 + m1>
;,
m0<4, 5> # 9 #
```

---

### a\<collection, \*args>

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
m0.a<4>, # [1,2,3,4] #
m0.a<2,5> # [1,2,5,3,4] #
```

```py
{'john':2,'jane':4},
m0.a<'doe',6>, # {'john':2,'jane':4,'doe':6} #
m0.a<'john',10> # {'john':10,'jane':4,'doe':6} #
```

---

### rm\<collection, index/key>

Removes an index/key from a list or dictionary

#### Examples

```py
['john','jane','doe'],
m0.rm<1> # ['john','doe'] #
```

```py
{'john':2,'jane':4,'doe':6},
m0.rm<'jane'> # {'john':2,'doe':6} #
```

---

### rmv\<collection, value>

Removes an element/value from a list or dictionary

#### Examples

```py
['john','jane','doe'],
m0.rmv<'jane'> # ['john','doe'] #
```

```py
{'john':2,'jane':4,'doe':6},
m0.rmv<4> # {'john':2,'doe':6} #
```

---

### pop\<collection, index/key=-1>

Removes and returns the element/value at the index/key from a list or dictionary. Index defaults to -1 (end of the list, or the integer key of -1 for dictionaries)

#### Examples

```py
[12,13,43,2],
p<m0.pop>,
# > 2 #
p<m0.pop<1>>,
# > 13 #
p<m0>
# > [12,43] #
```

```py
{"Harold":4,"Jill":32,"John":44},
p<m0.pop<"Jill">>,
# > 32 #
p<m0>
# > {"Harold":4,"John":44} #
```

---

### kys\<dictionary>

Returns the keys of the dictionary as a list

#### Example

```py
{
  "jane":23,
  "john":29,
  "dave":10
},
p<m0.kys>
# > ['jane', 'john', 'dave'] #
```

---

### vls\<dictionary>

Returns the values of the dictionary as a list

#### Example

```py
{
  "jane":23,
  "john":29,
  "dave":10
},
p<m0.vls>
# > [23, 29, 10] #
```

---

### l\<obj>

Returns the length of a list, dictionary, tuple, string, or number

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

### wf\<file, string>

Writes the given string to the given file. The given file must be opened in either write or append mode.

#### Examples

```py
fw "example.txt":
    m0.wf<"Hello, every-nyan. How are you? Fine, thank you."> # Overwriting example.txt's file contents #
;,
```

```py
fa "example.txt":
    m0.wf<"Hello, every-nyan. How are you? Fine, thank you."> # Appending to the end of example.txt's file contents #
;,
```

---

### rf\<file>

Gets and returns the given file's contents. The given file must be opened in read mode.

#### Example

```py
fr "example.txt":
    m0.rf<> # Gets and returns example.txt's file contents
;,
```

---

### sl\<secs>

Sleeps the program for a given amount of seconds.

#### Example

```py
p<"Before sleep">,
sl<2>, # Waits for 2 seconds #
p<"After sleep">
```

---

### srt\<collection, reverse=False, key=None>

Sorts the given list in the direction specified. The key, if specified, is a function that will be called on each list element prior to making comparisons.

#### Example

```py
[3,2,25,23,45,3,3546,2,13,4546,3],
srt<m0>,
p<m0>
# > [2, 2, 3, 3, 3, 13, 23, 25, 45, 3546, 4546] #
```

---

### srtd\<collection, reverse=False, key=None>

Returns a sorted version of the given list in the direction specified. The key, if specified, is a function that will be called on each list element prior to making comparisons.

#### Examples

```py
[3,2,25,23,45,3,3546,2,13,4546,3],
m0.srtd.p
# > [2, 2, 3, 3, 3, 13, 23, 25, 45, 3546, 4546] #
```

```py
[3,2,25,23,45,3,3546,2,13,4546,3],
m0.srtd<T>.p
# > [4546, 3546, 45, 25, 23, 13, 3, 3, 3, 2, 2] #
```

---

### ab\<number>

Returns the absolute value of a number. The argument may be an integer, or a float.

#### Example

```py
-123,
ab<m0> # 123 #
```

---

### mx\<\*objs>

### mx\<iterable>

Returns the item with the highest value.

If the values are strings, an alphabetical comparison is done.

#### Example

```py
mx<2,53,13,65>, # 65 #
mx<[2,53,13,65]> # 65 #
```

---

### mn\<\*objs>

### mn\<iterable>

Returns the item with the lowest value.

If the values are strings, an alphabetical comparison is done.

#### Example

```py
mn<4,3,35,23,42>, # 3 #
mn<[4,3,35,23,42]> # 3 #
```

---

### al\<iterable>

Returns True if all elements of the iterable are true (or if the iterable is empty).

#### Examples

```py
al<[T, T, T]>, # T #
al<[T, F, T]>, # F #
al<[]> # T #
```

---

### ay\<iterable>

Returns True if any element of the iterable is true. If the iterable is empty, it returns False.

#### Examples

```py
ay<[T, F, T]>, # T #
ay<[F, F, F]>, # F #
ay<[]> # F #
```

---

### up\<string>

Capitalizes all of the letters in the string, and returns the result.

#### Examples

```py
"Example String",
p<up<m0>>
# > EXAMPLE STRING #
```

---

### lw\<string>

Lowercases all of the letters in the string, and returns the result.

#### Examples

```py
"exAmpLe STring",
p<lw<m0>>
# > example string #
```

---

### cp\<string>

Capitalizes the first letter in the string, lowercases the rest, and returns the result.

#### Examples

```py
"exAmpLe STring",
p<cp<m0>>
# > Example string #
```

---

### sp\<string, sep=None, maxsplit=-1>

Separates the string by `sep` (if `None`, it separates by whitespace characters). If `maxsplit` is set, it will only split `maxsplit` times (if `-1`, it has no limit). Returns a list.

#### Examples

```py
"Hello World!",
sp<m0> # [Hello, World!] #
```

```py
"Martin,48,Dikdi Avenue,Dafdata"
sp<m0, ','> # [Martin, 48, Dikdi Avenue, Dafdata] #
```

---

### jn\<collection, sep=" ">

Joins the collection on `sep`.

#### Examples

```py
["This", "is", "a", "seperated", "string"],
m0.jn # "This is a seperated string" #
```

```py
[4,1,5,6,3,1,0],
m0.jn<", "> # "4, 1, 5, 6, 3, 1, 0" #
```

---

## Using Python's built-in functions

Using `^`, you can call all of [python's built-in functions](https://docs.python.org/3/library/functions.html)

> When calling Python's built-in functions, unless they are nested within another statement, they will always store the return value in memory, regardless of whether the function actually returns a value or not. For example, calling Python's print will store None in memory, while calling CommaScript's print will not. You can get around this by using the null setter, `x => ^print<"">` (more on this in the 'Getting Input from the User' section).

> This has only been lightly tested, so use with caution

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

---

## Using Python Modules

Like using python's built-in functions, using `^` will give you access to python's modules. Here are some examples:

```py
@^'random',
p<$0randint<1,100>>
# > 36 #
```

```py
@^'math',
p<$0pi>
# > 3.141592653589793 #
```

Putting a `^` after the `@` for importing, will tell the program that you are importing a python module, and not a CommaScript file. To use the imported modules, it's the same as using imported files. `$` followed by the index of which import you want, followed by the function or attribute you want to use.

> This has only been lightly tested, so use with caution

---
