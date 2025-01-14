from random import random


class ecosystem:
    def __init__(self, river, fish, bear, steps):
        self.river = int(river)
        self.fish = int(fish)
        self.bear = int(bear)
        self.steps = int(steps)

    def createNew(self, animal, RN):
        global List
        L = []
        String = "".join(RN)
        a0 = a1 = 0
        while True:
            a1 = String.find('N', a0)
            if a1 == -1:
                break
            L.append(a1)
            a0 = a1 + 1
        if len(L) != 0:
            n = int(random() * len(L))
            RN[L[n]] = animal
            List.append(L[n])

    def simulation(self):
        global List
        List = []

        # create a list

        R = []
        count0 = 0
        while True:
            count0 += 1
            R.append('F')
            if count0 == self.fish:
                break
        count1 = 0
        while True:
            count1 += 1
            R.append('B')
            if count1 == self.bear:
                break
        count2 = 0
        while True:
            if count2 == self.river - self.bear - self.fish:
                break
            count2 += 1
            R.append('N')

        # sort the list randomly

        RN = []
        count3 = self.river
        while True:
            index = int(random() * count3)
            RN.append(R[index])
            R.remove(R[index])
            count3 -= 1
            if count3 == 0:
                break

        # move

        count = 1

        while True:
            print('The ecosystem at the beginning of the step ' + str(count) + ':')
            print(RN)
            flag1 = True
            flag2 = True
            p0 = 0
            List = []
            while True:
                flg = False
                pB = pF = -1
                try:
                    pB = RN.index('B', p0)
                except:
                    flag1 = False
                try:
                    pF = RN.index('F', p0)
                except:
                    flag2 = False
                if flag1 is False and flag2 is False:
                    break
                box = [0, 1, -1]
                movement = box[int(random() * 3)]  # random step

                # B

                if (pB < pF and pB != -1) or pF == -1:
                    for l in List:  # The newly generated animals will NOT take actions in the current step
                        if pB == l:
                            flg = True
                    if flg:
                        p0 += 1
                        continue
                    if pB == 0:

                        if movement == 1:
                            if RN[1] == 'B':
                                p0 = pB + 1
                                self.createNew('B', RN)
                            else:
                                p0 = pB + 2
                                RN[1] = 'B'
                                RN[0] = 'N'
                        else:
                            p0 = pB + 1
                            movement = 0
                    elif pB == (len(RN) - 1):
                        p0 = pB + 1
                        if movement == -1:
                            if RN[-2] == 'B':
                                self.createNew('B', RN)
                            else:
                                RN[-2] = 'B'
                                RN[-1] = 'N'
                        else:
                            movement = 0
                    else:
                        if movement == 1 and RN[movement + pB] != 'B':
                            p0 = pB + 2
                        else:
                            p0 = pB + 1
                        if movement == 1:
                            if RN[pB + 1] == 'B':
                                self.createNew('B', RN)
                            else:
                                RN[pB] = 'N'
                                RN[pB + 1] = 'B'
                        elif movement == -1:
                            if RN[pB - 1] == 'B':
                                self.createNew('B', RN)
                            else:
                                RN[pB] = 'N'
                                RN[pB - 1] = 'B'

                    print('Animal B, Action:', movement)

                # F

                elif (pF < pB and pF != -1) or pB == -1:
                    for l in List:  # The newly generated animals will NOT take actions in the current step
                        if pF == l:
                            flg = True
                    if flg:
                        p0 += 1
                        continue
                    if pF == 0:

                        if movement == 1:
                            if RN[1] == 'F':
                                p0 = pF + 1
                                self.createNew('F', RN)
                            elif RN[1] == 'B':
                                p0 = pF + 1
                                RN[0] = 'N'
                            else:
                                p0 = pF + 2
                                RN[1] = 'F'
                                RN[0] = 'N'
                        else:
                            p0 = pF + 1
                            movement = 0
                    elif pF == (len(RN) - 1):
                        p0 = pF + 1
                        if movement == -1:
                            if RN[-2] == 'F':
                                self.createNew('F', RN)
                            elif RN[-2] == 'B':
                                RN[-1] = 'N'
                            else:
                                RN[-2] = 'F'
                                RN[-1] = 'N'
                        else:
                            movement = 0
                    else:
                        if movement == 1 and RN[movement + pF] == 'N':
                            p0 = pF + 2
                        else:
                            p0 = pF + 1
                        if movement == 1:
                            if RN[pF + 1] == 'B':
                                RN[pF] = 'N'
                            elif RN[pF + 1] == 'F':
                                self.createNew('F', RN)
                            else:
                                RN[pF] = 'N'
                                RN[pF + 1] = 'F'
                        if movement == -1:
                            if RN[pF - 1] == 'B':
                                RN[pF] = 'N'
                            elif RN[pF - 1] == 'F':
                                self.createNew('F', RN)
                            else:
                                RN[pF] = 'N'
                                RN[pF - 1] = 'F'
                    print('Animal F, Action:', movement)

                print('The current ecosystem after the action:')
                print(RN)

            if count == self.steps:
                break
            count += 1
