import random 
import numpy
import matplotlib.pyplot as plt


n = 3
class Board:
    board = [0]*n*n
    dict = {1: "X", -1: "O", 0:"-"}
    def __init__(self, board = [0] * n*n):
        self.board = board

    def __hash__(self):
        prime = 31
        ret = 0
        for i in self.board: 
            i += 2
            ret = ret * prime + i
        return ret  

    def __eq__(self, other):
        for i in range(n*n):
            if self.board[i] != other.board[i]:
                return False
        return True

    def isSpaceFree(self, pos):
        if 0 > pos or pos > 8: 
            print("bad position")
        else:
            return self.board[pos] == 0

    def isBoardFull(self):
        for i in range(n*n):
            if self.isSpaceFree(i):
                return False
        return True

    def addToNewBoard(self, pos, player):
        board = self.board[:]
        board[pos] = player
        return Board(board)

    def emptySpaceList(self):
        return [i for i in range(n*n) if self.board[i] == 0]
    
    def isWinner(self, player):
        bo = self.board
        le = player
        return ((bo[7-1] == le and bo[8-1] == le and bo[9-1] == le) or # across the top
        (bo[4-1] == le and bo[5-1] == le and bo[6-1] == le) or # across the middle
        (bo[1-1] == le and bo[2-1] == le and bo[3-1] == le) or # across the bottom
        (bo[7-1] == le and bo[4-1] == le and bo[1-1] == le) or # down the left side
        (bo[8-1] == le and bo[5-1] == le and bo[2-1] == le) or # down the middle
        (bo[9-1] == le and bo[6-1] == le and bo[3-1] == le) or # down the right side
        (bo[7-1] == le and bo[5-1] == le and bo[3-1] == le) or # diagonal
        (bo[9-1] == le and bo[5-1] == le and bo[1-1] == le)) # diagonal

    def __str__(self):
        board = [self.dict[i] for i in self.board]
        ret = str(board[0]) + " | " + str(board[1]) + " | " + str(board[2])
        ret += "\n"
        ret += str(board[3]) + " | " + str(board[4]) + " | " + str(board[5])
        ret += "\n"
        ret += str(board[6]) + " | " + str(board[7]) + " | " + str(board[8])
        return ret
        
    def isGameOverAndWinnerIs(self): 
        # only 0 if game is still going on
        if self.isWinner(-1):
            return -1
        elif self.isWinner(1):
            return 1
        else:
            if 0 in self.board: 
                return 0
            else: 
                return -999
    def makeMove(self, pos, player):
        if not self.isSpaceFree(pos):
            print("Taken space")
        elif player != 1 and player != -1:
            print("bad player val")
        elif 0 > pos or pos > 8: 
            print("bad position")
        else:
            self.board[pos] = player

    def resetBoard(self):
        self.board = [0] * n * n

def allPossibleBoards():
    lst = []
    board = []
    def allPossibleBoardsHelper(board):
        if not (len(board) > n * n -1):
            board.append(0)
            lst.append(board[:])
            allPossibleBoardsHelper(board)
            del board[-1]
            board.append(-1)
            lst.append(board[:])
            allPossibleBoardsHelper(board)
            del board[-1]
            board.append(1)
            lst.append(board[:])
            allPossibleBoardsHelper(board)
            del board[-1]
    allPossibleBoardsHelper(board)
    boardList = []
    for board in lst:
        board = putInZeroes(board) 
        boardList.append(Board(board))

    ret = removeDuplicates(boardList)
    return ret

def removeDuplicates(seq): # Order preserving
  seen = set()
  return [x for x in seq if x not in seen and not seen.add(x)]

def putInZeroes(board):
    return board + [0] * (n*n - len(board))

class TTTAgent:
    boardDist = {}
    prevBoard = Board()
    e = 0.05
    alpha = 0.1
    def __init__(self):
        prevBoard = Board()
        allBoards = allPossibleBoards()
        for board in allBoards:
            winner = board.isGameOverAndWinnerIs()
            if winner == 1:
                self.boardDist[board] = 1
            elif winner == -1:
                self.boardDist[board] = 0
            else:
                self.boardDist[board] = 0.5
        # print(self.boardDist)
        # print(len(self.boardDist))

    def playPosition(self, board): 
        potentialPlays = board.emptySpaceList()
        if random.uniform(0, 1) < self.e:
            bestPlay = random.choice(potentialPlays)
        else: 
            bestPlay = potentialPlays[0]
            bestPlayProb = 0
            for play in potentialPlays:
                boardWithPlay = board.addToNewBoard(play, 1)
                bordWithPlayProb = self.boardDist[boardWithPlay]
                if bordWithPlayProb > bestPlayProb: 
                    bestPlayProb = bordWithPlayProb
                    bestPlay = play
            self.updatePreviousBoard(boardWithPlay)
        return bestPlay    

    def updatePreviousBoard(self, boardWithPlay):
        bestPlayProb = self.boardDist[boardWithPlay]
        prevPlayProb = self.boardDist[self.prevBoard]
        delta = bestPlayProb - prevPlayProb
        self.boardDist[self.prevBoard] = prevPlayProb + self.alpha * delta
        self.prevBoard = boardWithPlay

    # def __str__(self): #show the probability distribution
    #     board = [ for i in boardDist(self.prevboard)]
    #     ret = str(board[0]) + " | " + str(board[1]) + " | " + str(board[2])
    #     ret += "\n"
    #     ret += str(board[3]) + " | " + str(board[4]) + " | " + str(board[5])
    #     ret += "\n"
    #     ret += str(board[6]) + " | " + str(board[7]) + " | " + str(board[8])
    #     return ret


class RandomOpponent: 
    def playPosition(self, board):
        potentialPlays = board.emptySpaceList()
        return random.choice(potentialPlays)

class SmartOpponent: 
    # train smart opponent by running agent against random opponent and taking distribution
    # train it again by running smart opponent against agent 
    boardDist = {}
    def __init__(self, boardDist):
        self.boardDist = boardDist
    def playPosition(self, board): 
        potentialPlays = board.emptySpaceList()
        bestPlay = potentialPlays[0]
        bestPlayProb = 0
        for play in potentialPlays:
            boardWithPlay = board.addToNewBoard(play, 1)
            bordWithPlayProb = self.boardDist[boardWithPlay]
            if bordWithPlayProb > bestPlayProb: 
                bestPlayProb = bordWithPlayProb
                bestPlay = play
        return bestPlay    

showBoards = False
class Game:
    player1 = TTTAgent() #Agent must be player 1
    player2 = RandomOpponent()
    board = Board()
    gamesPlayed = 0
    gamesWonBy1 = 0
    gamesWonBy2 = 0
    winRateList = []
    def __init__(self, player1 = TTTAgent(), player2 = RandomOpponent()):
        self.gamesPlayed = 0 
        self.gamesWonBy1 = 0
        self.gamesWonBy2 = 0
        self.player1 = player1
        self.player2 = player2

    def playGame(self):
        turnCounter = random.choice([ 1, 0])
        while self.board.isGameOverAndWinnerIs() == 0: 
            # print(self.board)
            # print("----------------------")
            if turnCounter % 2 == 0:
                pos = self.player1.playPosition(self.board)
                self.board.makeMove(pos, 1)
            else: 
                pos = self.player2.playPosition(self.board)
                self.board.makeMove(pos, -1)
            turnCounter += 1
        if self.board.isGameOverAndWinnerIs() == 1:
            self.gamesWonBy1 += 1
        if self.board.isGameOverAndWinnerIs() == -1:
            self.gamesWonBy2 += 1
        self.gamesPlayed += 1
        # print(self.board)
        # if showBoards:
            # print(self.board.board)
            # print(self.player1.boardDist)


    def runNGames(self, n):
        self.winRateList = []
        for _ in range(n):
            self.playGame()
            self.board.resetBoard()
            # print("Player 1 has won " + str(self.gamesWonBy1) + " games")
            # print("Player 1 win rate: " + str(self.gamesWonBy1/self.gamesPlayed))
            # print("Player 2 win rate: " + str(self.gamesWonBy2/self.gamesPlayed))
            winRate = self.gamesWonBy1/(1+self.gamesWonBy2+self.gamesWonBy1)
            self.winRateList.append(winRate)
        
        print("Player 1 win rate w/o ties " + str(self.gamesWonBy1/(self.gamesWonBy2+self.gamesWonBy1)))
        # print(self.player1.__class__.__name__)
        # print(self.player2.__class__.__name__)
        plt.plot(self.winRateList)
        axes = plt.gca()
        axes.set_ylim([0,1])
        plt.show()
trainingAgent = TTTAgent()            

print("-----------------------------------")
print("RANDOM VS. RANDOM")
game6 = Game(RandomOpponent(), RandomOpponent())
game6.runNGames(1000)
print("-----------------------------------")

print("AGENT VS. RANDOM")
game = Game(trainingAgent, RandomOpponent())
game.runNGames(1000)
print("-----------------------------------")

print("RANDOM VS. AGENT CLONE")
game4 = Game(RandomOpponent(), SmartOpponent(trainingAgent.boardDist.copy()))
game4.runNGames(1000)
print("-----------------------------------")

print("OLD AGENT VS. AGENT CLONE ???")
showBoards = True
game2 = Game(trainingAgent, SmartOpponent(trainingAgent.boardDist.copy()))
game2.runNGames(1000)
game2.player1.alpha = 0.2
game2.runNGames(1000)
print("-----------------------------------")

print("NEW AGENT VS. AGENT CLONE ???")
game7 = Game(TTTAgent(), SmartOpponent(trainingAgent.boardDist.copy()))
game7.runNGames(1000)
game7.player1.alpha = 0.4
game7.runNGames(1000)
print("-----------------------------------")

print("RANDOM VS NEW AGENT CLONE")
game3 = Game(RandomOpponent(), SmartOpponent(trainingAgent.boardDist.copy()))
game3.runNGames(1000)
print("-----------------------------------")
print("RANDOM VS UNTRAINED AGENT CLONE")
untrainedAgent = TTTAgent()
game8 = Game(RandomOpponent(), SmartOpponent(untrainedAgent.boardDist.copy()))
game8.runNGames(1000)
print("-----------------------------------")
print("AGENT VS AGENT ???")
game5 = Game(TTTAgent(), TTTAgent())
game5.runNGames(1000)
print("-----------------------------------")



def test():
    x = Board()
    x.makeMove(2, 1)
    x.makeMove(5, -1)
    x.makeMove(7, 10)
    x.makeMove(10, 1)
    print(x)
    print(x.isGameOverAndWinnerIs())
    print(x.isSpaceFree(5))
    print(x.isSpaceFree(0))
    print(x.isBoardFull())
    print(x.emptySpaceList())
    for i in range(9):
        x.makeMove(i, 1)
    print(x.isBoardFull())
    print(x.emptySpaceList())
    print(x.isGameOverAndWinnerIs())

