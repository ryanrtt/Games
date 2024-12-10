import time
import random

winningChoices = {
    "rock" : "paper",
    "paper" : "scissors",
    "scissors" : "rock",
}

print("Welcome to Rock Paper Scissors!")
for i in range(1,4):
    time.sleep(0.9)
    print('.' * i)
time.sleep(1)

invalidChoices = ["Cmon, choose properly!", "What??", "Try again.", "Don't make me ask again."]
choiceNo = ["Scared...", "I didn't think so.", "Come back when you have the guts to play..."]
invalidAnswer = ["That's not part of the game!", "Do you even know how to play?", "Seriously?!"]
computerLose = ["Arghhh!", "You're so lucky...", "You cheated.", "Whatever."]
computerWin = ["Better luck next time.", "I never lose.", "You really thought you'd win?", "Too easy."]
computerDraw = ["Why would you choose that?!", "Ugh."]
computerChoice = ["rock", "paper", "scissors"]

while True:
    playGame = input("Are you ready to lose? Y/N \n")
    if playGame.lower() in ('n', "no", 'y', "yes"):
        break
    print()
    print(invalidChoices[random.randrange(0, len(invalidChoices))])
    time.sleep(1)

if (playGame.lower() in ('n', "no")):
    print()
    print(choiceNo[random.randrange(0, len(choiceNo))]) 
    time.sleep(1)
    quit()

while True:
    print()
    print("Ready?")
    for i in range (3,0, -1):
        time.sleep(1)
        print(i)
    time.sleep(1)
    print('.\n')
    answer = input()
    if (answer.lower() in ("rock", "paper", "scissors")):
        break
    print(invalidAnswer[random.randrange(0, len(invalidAnswer))])
    time.sleep(1)

computerAnswer = computerChoice[random.randrange(0, len(computerChoice))]
time.sleep(0.1)
print()
print(computerAnswer.upper() + '!\n')
if (answer.lower() == computerAnswer):
    print(computerDraw[random.randrange(0, len(computerDraw))])
elif (answer.lower() == winningChoices[computerAnswer]):
    print(computerLose[random.randrange(0, len(computerLose))])
else:
    print(computerWin[random.randrange(0, len(computerWin))])
time.sleep(1)
quit()