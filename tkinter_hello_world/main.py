import tkinter

def myFunction():
    print("myCallBackFunction was called")

oButton = tkinter.Button(text="Click me", command=myFunction)