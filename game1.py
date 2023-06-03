import string
import os
import time

alphabet = string.ascii_lowercase

index = 0
user_alphabets = ""
start_time = time.time() 

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    blank = ' '*(len(alphabet)-len(user_alphabets))
    print(f"[{user_alphabets}{blank}]")

    user_input = input("Insert alphabet: ")
    if user_input == alphabet[index]:
        index = index + 1
        user_alphabets = user_alphabets+user_input
        
        if index == len(alphabet):
            end_time = time.time()
            elapsed_time = end_time-start_time
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"[{user_alphabets} ]")
            print(f"Elapsed Time: {elapsed_time:.2f},  Sucess!\n")

            break
    else:
        print("Wrong alphabet ! Try again !\n")
        user_alphabets = ""
        index = 0
