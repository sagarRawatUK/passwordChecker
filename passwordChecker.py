import requests
import hashlib
import sys
from tkinter import *

def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API')
    return res

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

def check_pwd():
    password = passwords.get()
    if password != "" :
        count = pwned_api_check(password)
        if count == 0:
            l = Label(root,text="Your Password has not been Hacked yet. It is SAFE.",fg="green")
            l.pack()
        else:
            l = Label(root,text=password+" was hacked "+count+" times. NOT SAFE.",fg="red")
            l.pack()
    else :
        l = Label(root,text="Password field is Empty.")
        l.pack()


root = Tk()
root.geometry("500x300")
root.title("Password Checker")
font = ("poppins",25,"normal")
Label(root,text="Password Checker",width="50",bg="gray",font=("Calibri",18,"bold")).pack()
Label(root,text="").pack()
Label(root,text="").pack()
Label(root,text="Enter Password : ",font=("Calibri",18)).pack()
passwords = StringVar()
password_entry = Entry(root,textvariable = passwords,width="30")
password_entry.pack()
Label(root,text="").pack()
Button(root,text="Search",command=check_pwd,font=("Calibri",12,"bold")).pack()
Label(root,text="").pack()

root.mainloop()
