from tkinter import *
import fractions
import math

root = Tk()
root.title('simple calculator')
root.resizable=False
e = Entry(root,width=50,borderwidth=8)
e.grid(row=0,column=0,columnspan=5,padx=10,pady=10)
isOff = True
firstClick = True
answerIsInvalid = False
ans = 0

def calculateAnswer():
    global answerIsInvalid,isOff
    
    if(isOff): 
        return

    userInput = e.get()
    e.delete(0, END)
    nums,symbs = seperateThings(userInput)
    if(len(nums)-1!=len(symbs)):
        answerIsInvalid = True
        return "INVALID"
    #convert string to nums
    invalidPercentage = list(filter(lambda num: "%"==num or num[0]=="%" or num.count("%")>1,nums))
    nums , invalidDecimals = getInvalidDecimals(nums)
    if len(invalidPercentage)>0 or len(invalidDecimals)>0:
        answerIsInvalid = True
        return "INVALID"
    nums = list(map(lambda num:float(num),nums))
    return takeNumsAndOp(nums,symbs)


def calculatePercentage(num):
    num = num.replace("%","")
    return str(float(num)/100)


def getInvalidDecimals(nums):
    invalidDecimals = []
    for index,num in enumerate(nums): 
        if '%' in num:
            nums[index] = calculatePercentage(num)
        else:
            try:
                float(num)
            except Exception:
                invalidDecimals.append(num)
    return nums,invalidDecimals


def takeNumsAndOp(nums,ops):
    operators = {'+':lambda num1,num2:num1+num2,
                 '-':lambda num1,num2:num1-num2,
                 '/':lambda num1,num2:num1/num2,
                 '^':lambda num1,num2:math.pow(num1,num2),
                 'x':lambda num1,num2:num1*num2}
    temp =''
    if len(nums)==1:
        return nums[0]

    for index in range(len(nums)-1):
        if index==0:
            num1 = nums.pop(0)
            num2 = nums.pop(0)
            op = ops.pop(0)
        else:
            num1 = temp
            num2 = nums.pop(0)
            op = ops.pop(0)

        temp = operators[op](num1,num2)
    return temp


def seperateThings(userInput):
    validOps = ['+','-','/','^','x']
    savedChars = ''
    nums=[]
    symbs=[]
    for index,char in enumerate(userInput):
        if char in validOps:
            nums.append(savedChars)
            symbs.append(char)
            savedChars=''
            continue
        savedChars+=char
        if(index==len(userInput)-1 and len(savedChars)>0):
            nums.append(savedChars)
    return nums,symbs


def clicked(number):
    global isOff,firstClick,answerIsInvalid
    if(isOff): 
        return
    
    if(answerIsInvalid):
        e.delete(0,END)
    
    if(firstClick):
        e.delete(0,END)
        firstClick = False
    answerIsInvalid = False
    e.insert(END, number)


def clickedSymbol(symbol):
    global isOff,firstClick,answerIsInvalid
    if(isOff): 
        return
    
    if(answerIsInvalid):
        e.delete(0,END)
    
    if(firstClick and symbol=='%'):
        firstClick = False
        e.insert(END, symbol)
        return

    if(firstClick):
        e.delete(0,END)
        firstClick = False

    answerIsInvalid = False
    e.insert(END, symbol)


def backSpace():
    if(isOff): 
        return
    screenText = e.get()
    if(len(screenText)==1):
        clearScreen()
    else:
        e.delete(0,END)
        e.insert(0, screenText[:len(screenText)-1])


def OnAndOff():
    global isOff, firstClick
    if(isOff):
        e.insert(0, 0)
        isOff = False
    else:
        isOff = True
        firstClick = True
        e.delete(0, END)


def clearScreen():
    global firstClick,isOff
    if(isOff):return
    e.delete(0, END)
    e.insert(0,0)
    firstClick = True

def equal_sign():
    if(isOff):return
    e.insert(0, calculateAnswer())

#buttons
bnt0 = Button(root,text='0',padx=30,pady=7,command=lambda:clicked('0'))
bnt1 = Button(root,text='1',padx=30,pady=10,command=lambda:clicked('1'))
bnt2 = Button(root,text='2',padx=30,pady=10,command=lambda:clicked('2'))
bnt3 = Button(root,text='3',padx=30,pady=10,command=lambda:clicked('3'))
bnt4 = Button(root,text='4',padx=30,pady=10,command=lambda:clicked('4'))
bnt5 = Button(root,text='5',padx=30,pady=10,command=lambda:clicked('5'))
bnt6 = Button(root,text='6',padx=30,pady=10,command=lambda:clicked('6'))
bnt7 = Button(root,text='7',padx=30,pady=10,command=lambda:clicked('7'))
bnt8 = Button(root,text='8',padx=30,pady=10,command=lambda:clicked('8'))
bnt9 = Button(root,text='9',padx=30,pady=10,command=lambda:clicked('9'))

equals = Button(root,text='=',padx=30,pady=7,command=lambda:equal_sign())
add = Button(root,text='+',padx=30,pady=10,command=lambda:clickedSymbol('+'))
minus = Button(root,text='-',padx=31,pady=10,command=lambda:clickedSymbol('-'))
divide = Button(root,text='/',padx=31,pady=10,command=lambda:clickedSymbol('/'))
percentage = Button(root,text='%',padx=28,pady=10,command=lambda:clickedSymbol('%'))
multiply = Button(root,text='x',padx=31,pady=10,command=lambda:clickedSymbol('x'))
clear = Button(root,text='Clear',padx=19,pady=10,command=clearScreen)
comma = Button(root,text='.',padx=31,pady=7,command=lambda:clickedSymbol('.'))
Ans = Button(root,text='Ans',padx=23,pady=7,bg='green',fg='white')
exponent = Button(root,text='exp',padx=24,pady=10,command=lambda:clickedSymbol('^'))
offOrOn = Button(root,text='on/off',padx=16,pady=5,bg='red',fg='white',command=OnAndOff)
backspace = Button(root,text='<x]',padx=22,pady=5,bg='orange',fg='white',command=backSpace)
emptyElement = Label(root,text='')

#positioning
Ans.grid(row=7,column=0)
bnt0.grid(row=7,column=1)
comma.grid(row=7,column=2)
equals.grid(row=7,column=3)

bnt7.grid(row=6,column=0)
bnt8.grid(row=6,column=1)
bnt9.grid(row=6,column=2)
multiply.grid(row=6,column=3)

bnt4.grid(row=5,column=0)
bnt5.grid(row=5,column=1)
bnt6.grid(row=5,column=2)
minus.grid(row=5,column=3)

bnt1.grid(row=4,column=0)
bnt2.grid(row=4,column=1)
bnt3.grid(row=4,column=2)
add.grid(row=4,column=3)

percentage.grid(row=3,column=0)
clear.grid(row=3,column=1)
exponent.grid(row=3,column=2)
divide.grid(row=3,column=3)

emptyElement.grid(row=2,column=1)

offOrOn.grid(row=1,column=0)
backspace.grid(row=1,column=3)
root.mainloop()
