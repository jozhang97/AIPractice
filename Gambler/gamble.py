import random
import matplotlib.pyplot as plt

class GambleAgent:
    # S = [i for i in range (101)]
    S = [i for i in range (1, 100)]
    y = 0.9
    pi = {}
    v = {}
    delta = 0
    p = 0.4
    e = 0.1
    def __init__(self, p = 0.4):
        self.p = p
        for s in self.S:
            self.pi[s] = s
            self.v[s] = 0
        # self.pi[0] = 0
        # self.pi[100] = 0
        self.v[0] = 0
        self.v[100] = 0

    def reward(self, s):
        if s >= 100:
            return 1
        else:
            return 0

    def calcQ(self, s, a):
        ret = self.p * (self.reward(s + a) + self.y * self.v[s + a])
        ret += (1 - self.p) * (self.reward(s - a) + self.y * self.v[s - a])
        return ret

    def policyEvaluate(self):
        while (True):
            self.delta = 0
            for s in self.S:
                temp = self.v[s]
                a = self.pi[s]
                # A = [i for i in range(min(s, 100 - s) + 1)]
                # self.v[s] = 0
                # for a in A:
                self.v[s] = self.calcQ(s, a)
                self.delta = max(self.delta, abs(self.v[s] - temp))
            if self.delta < self.e:
                break

    def policyImprove(self):
        stable = True
        for s in self.S:
            temp = self.pi[s]
            A = [i for i in range(min(s, 100 - s) + 1)]
            best = A[0]
            bestVal = 0
            for a in A:
                currVal = self.calcQ(s, a)
                if currVal > bestVal:
                    best = a
                    bestVal = currVal
                elif bestVal == 0:
                    continue
                elif abs(currVal - bestVal)/(bestVal) < 0.01 ** 2:
                    if random.random() > 0.95:
                        best = a
                        # print("random", currVal, bestVal)
                        # print(abs(currVal - bestVal)/(bestVal), self.e)
            self.pi[s] = best
            if temp != self.pi[s]:
                stable = False
        return not stable

    def policyEvaluate2(self):
        while (True):
            self.delta = 0
            for s in self.S:
                temp = self.v[s]
                # a = self.pi[s]
                A = [i for i in range(min(s, 100 - s) + 1)]
                self.v[s] = 0
                for a in A:
                    self.v[s] = max(self.v[s], self.calcQ(s, a))
                self.delta = max(self.delta, abs(self.v[s] - temp))
            if self.delta < self.e:
                break


    def execute(self):
        counter = 0
        while self.policyImprove():
            self.policyEvaluate2()
            counter += 1
        self.plot(self.pi)
        self.plot(self.v)
        print("Times ran: " + str(counter))
        return self.pi, self.v

    def plot(self, dict):
        keys = dict.keys()
        vals = dict.values()
        plt.plot(keys, vals)
        # axes = plt.gca()
        # axes.set_ylim([0,1])
        plt.show()

gambleAgent = GambleAgent(0.8)
gambleAgent.execute()