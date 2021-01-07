'''
Here we set the CTF difficulty, where the options are ranging from 1-3 (1 = easiest, 3 = hardest)
its direct affect is: 
	1 = no SQL Injection vulnerability (admin is granted on click)
	2 = SQL Injection with explicit query response
	3 = SQL Injection with exception response (little information)
	4 = Blind SQL Injection -  no response

level 3 is recommended
'''

CTF_DIFFICULTY = 3 
