while True:
    try:
        integer = int(input("Enter an integer: "))  
    except:
        integer = None 
    if integer!=None:
        break
    else:
        print('Invalid Number')
for i in str(integer):
    print(i)
