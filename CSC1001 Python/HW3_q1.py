class Flower:
    def __init__(self, name, petals, price):  # initializing
        self.name = name
        self.petals = petals
        self.price = price

    # def of information method

    def Information(self):
        flag = True
        if type(self.name) != str:
            print('The input of the flower name is incorrect. A string is required.')
            flag = False
        if type(self.petals) != int:
            print('The input of the number of petals is incorrect. An integer is required.')
            flag = False
        elif self.petals <= 0:
            print('The input of the number of petals is incorrect. A positive integer is required.')
            flag = False
        if type(self.price) != float:
            print('The input of the price is incorrect. A type of float is required.')
            flag = False
        elif self.price <= 0:
            print('The input of the price is incorrect. A positive float is required.')
            flag = False
        if flag:
            print('Here is the information of your flower. Name: ' + self.name + ', Number of petals: ' + str(
                self.petals) + ', Price: ' + str(self.price))

    # def of get methods

    def getName(self):
        if type(self.name) != str:
            print('The input of the flower name is incorrect. A string is required.')
        else:
            print('The name of your flower is ' + str(self.name) + '.')

    def getPrice(self):
        if type(self.price) != float or self.price <= 0:
            print('The input of the price is incorrect. A positive float is required.')
        else:
            print('The price of your flower is ' + str(self.price) + '.')

    def getPetals(self):
        if type(self.petals) != int or self.petals <= 0:
            print('The input of the number of petals is incorrect. A positive integer is required.')
        else:
            print('The number of petals of your flower is ' + str(self.petals) + '.')

    # def of set methods

    def setName(self, n):
        if type(n) != str:
            print('The input of the flower name is incorrect. A string is required.')
        else:
            self.name = n

    def setPrice(self, pr):
        if type(pr) != float or pr <= 0:
            print('The input of the price is incorrect. A positive float is required.')
        else:
            self.price = pr

    def setPetals(self, pt):
        if type(pt) != int or pt <= 0:
            print('The input of the number of petals is incorrect. A positive integer is required.')
        else:
            self.petals = pt
