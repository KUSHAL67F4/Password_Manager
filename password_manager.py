from cryptography.fernet import Fernet

# Run only the below function first. Then, run the remaining program excluding the below function 
'''def write_key():
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)
add
write_key()'''

#After executing only the above function, run the below mentioned code(excluding the above function)
def load_key():
    file= open("key.key", "rb")
    key=file.read()
    file.close()
    return key


key = load_key()
fer = Fernet(key)


def view():
    with open('passwords.txt','r') as f:
        for line in f.readlines():
            data = line.rstrip() # rstrip() is used so that a new line is not printed at the end
            user, passwd = data.split("|")
            print("User:", user, "| Password:", fer.decrypt(passwd.encode()).decode())

def add():
    name = input("Account Name: ")
    pwd= input("Password: ")
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")

while True:
    mode=input("would you like to add a new password or view existing ones (view, add). Press Q to quit? ").lower()
    if mode == "q":
        break
    if mode== "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid Mode")


