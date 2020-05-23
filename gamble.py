from random import randint
from math import ceil
import os
import time
from pynput import keyboard
from pynput.keyboard import Key, Controller
import sqlite3

def multiplier(start_cap):
	global con, your_value, stop_listen, value, end_cap, balance, count, cashed
	cashed = False
	count = 0
	login_val = (username, psw)
	c.execute('SELECT * from users WHERE username=? AND psw=?', login_val)
	usr_info = c.fetchone()
	balance = usr_info[2]
	value = 1
	con = True
	while True:
		print("x" + str(value))
		condition = chance(value)
		value = round(value + 0.01, 2)
		if condition == False:
			print("Final multipler: x" + str(round(value,2)))
			break
		if con == False and count == 1:
			your_value = round(value,2)
			con = True
			cashed = True
		if condition == False:
			print("Final multipler: x" + str(round(value,2)))
			#break
		time.sleep(0.075)
	count = 0
	if cashed:
		end_cap = round((start_cap * your_value) - start_cap, 2)
		print("Your final multiplier: x" + str(your_value))
		print("You earned " +str(end_cap))
		your_value = 0
		return False
	else:
		end_cap = -start_cap
		print("You lost " + str(start_cap))
		print("You didn't cash out in time :(, better luck next time")
		your_value = 0
		return False

def chance(value):
	global prob
	prob = randint(0, 1000)
	prob2 = randint(0, 80)
	if prob <= prob2:
		return False

def on_press(key):
	global con, stop_listen, count
	count = count + 1
	if key == keyboard.Key.esc:
		con = False

def main(start_cap):
	global restart
	while True:
		with keyboard.Listener(on_press = on_press) as listener:
			restart = multiplier(start_cap)
			if restart == False:
				break
			listener.join()

def game():
	global choice, end_cap
	choice = input("Signup or Login: [s/l] ")
	if choice == "s":
		signup()
		after_login()
	elif choice == "l":
		login()
		after_login()
	else:
		print("INVALID")
		game()

def after_login():
	global play, run_var, start_cap, username, psw
	play = input("Want to play? [y/n]")
	login_val = (username, psw)
	c.execute('SELECT * from users WHERE username=? AND psw=?', login_val)
	usr_info = c.fetchone()
	balance = usr_info[2]
	if play == "y":
		run_var = True
		print("Your current balance is: " + str(balance))
		try:
			start_cap = float(input("Bet amount: "))
			if start_cap > balance or None:
				print("You don't have that much money yet")
				print("Try again...")
				after_login()
		except:
			print("invalid input")
	elif play == "n":
		run_var = False
	else:
		print("Invalid response")

	while run_var:
		main(start_cap)
		new_bal = balance+end_cap
		print("Your new balance is " + str(new_bal) + "... go again and test your odds!")
		updated_usr = (new_bal, username, psw)
		c.execute("UPDATE users SET money=? WHERE username=? AND psw=?", updated_usr)
		conn.commit()

		play = input("Want to play again? [y/n]")
		login_val = (username, psw)
		c.execute('SELECT * from users WHERE username=? AND psw=?', login_val)
		usr_info = c.fetchone()
		balance = usr_info[2]
		if play == "y":
			run_var = True
			print("Your current balance is: " + str(balance))
			try:
				start_cap = float(input("Bet amount: "))
				if start_cap > balance:
					print("You don't have that much money yet")
					print("Try again...")
					after_login()
			except:
				print("invalid input")
		elif play == "n":
			run_var = False
			break
		else:
			print("Invalid response")
		
def signup():
	global conn, c, username, psw
	conn = sqlite3.connect("test1.db")
	c = conn.cursor()

	username = str(input("Please enter username: "))
	psw = str(input("Please enter password: "))
	money = float(input("Please enter money: "))

	signup_val = (username, psw, money)
	c.execute("INSERT INTO users VALUES (?,?,?)", signup_val)
	conn.commit()

def login():
	global conn, c, username, psw
	conn = sqlite3.connect("test1.db")
	c = conn.cursor()

	username = str(input("Please enter username: "))
	psw = str(input("Please enter password: "))
	login_val = (username, psw)
	c.execute('SELECT * from users WHERE username=? AND psw=?', login_val)
	usr_info = c.fetchone()
	try:
		if usr_info[0] == username and usr_info[1] == psw:
			print("Welcome " + username)
	except:
		print("INVALID DETAILS")
		game()


game()