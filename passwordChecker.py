import requests
import hashlib
import sys
from tkinter import *

def request_api_data(query):
    global l
    try:
        url = 'https://api.pwnedpasswords.com/range/' + query
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}, check the API')
        return res
    except:
        l = Label(root,text="Internet Connection Required!")
        l.pack()

def get_leaks(hashes, password):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == password:
            return count
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5)
    return get_leaks(response , tail)

def clear():
    password_entry.delete(0,END)
    l.destroy()

def check_pwd():
    global l
    password = passwords.get()
    if password != "" :
        count = pwned_api_check(password)
        if count == 0:
            l = Label(root,text="Your Password has not been used yet. It is SAFE.",fg="green")
            l.pack()
        else:
            l = Label(root,text=password+" has been used "+count+" times. NOT SAFE.",fg="red")
            l.pack()
    else :
        l = Label(root,text="Password field is Empty.")
        l.pack()


root = Tk()
root.geometry("500x400")
root.title("Password Checker")
font = ("poppins",25,"normal")
Label(root,text="Password Checker",width="50",height="2",bg="medium sea green",fg="white",font=("Calibri",22,"bold")).pack()
Label(root,text="").pack()
Label(root,text="").pack()
Label(root,text="Enter Password : ",fg="gray26",font=("Calibri",16,"bold")).pack()
passwords = StringVar()
password_entry = Entry(root,textvariable = passwords,width="44")
password_entry.pack()
Label(root,text="").pack()

top = Frame(root)
bottom = Frame(root)
top.pack(side=TOP)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)


b1=Button(root,text="Search",command=check_pwd,width="8",fg="gray26",font=("Calibri",12,"bold")).pack(in_=top, side=LEFT)
Label(root,text="").pack(in_=top, side=LEFT)
b2=Button(root,text="Clear",command=clear,width="8",fg="gray28",font=("Calibri",12,"bold")).pack(in_=top, side=LEFT)
Label(root,text="").pack()

root.mainloop()
