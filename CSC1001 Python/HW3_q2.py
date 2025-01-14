class process_derivative:
    def __init__(self, poly):
        self.poly = poly

    def get_first_derivative(self):
        p0 = p1 = 0
        L0 = []
        L01 = []
        L1 = []

        # split each term into a list

        self.poly = self.poly.replace('-', '+-')  # replace minus characters
        while True:
            p1 = self.poly.find('+', p0)
            if p1 == -1:
                L01.append(self.poly[p0:])
                break
            L01.append(self.poly[p0:p1])
            p0 = p1 + 1

        # create a new list for new terms

        if len(L01) == 1 and self.poly.find('*') == -1:  # for constant
            L1.append('0')
        else:
            for mon in L01:
                if mon.find('*') == -1:
                    continue
                else:
                    multi = mon.find('*')
                    power = mon.find('^')
                    variable = mon[multi + 1]
                    L0.append(variable)
                    if power == -1:
                        L1.append(mon[:multi])
                    else:
                        deri = str(int(mon[:multi]) * int(mon[power + 1:]))
                        newPower = str(int(mon[power + 1:]) - 1)

                        if mon[power + 1:] == '2':
                            L1.append(deri + '*' + variable)
                        else:
                            L1.append(deri + '*' + variable + '^' + newPower)

        # decide whether it is a valid input

        flag = True
        if len(L0) == 1 or len(L0) == 0:
            pass
        else:
            init = L0[0]
            for var in L0:
                if init != var:
                    flag = False
                    break

        # return the derivative

        if flag:
            count = 0
            newString = ''
            for mon in L1:
                count += 1
                if count == len(L1):
                    newString += mon
                else:
                    newString = newString + mon + '+'
            newString = newString.replace('+-', '-')
            return newString
        else:
            return 'invalid input!'
