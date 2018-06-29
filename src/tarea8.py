# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

if __name__ == "__main__":
    import threading
import time
import random
import json

"""
ARGS & VARS
"""
read = json.loads(open('turtleHare.json').read())
laps = read['laps']
delay = read['delay']
sleepTime = read['sleepTime']

threads = []
waitLocks= {}
ranking=[]
rankLock=threading.Condition();

for lock in range(laps):
    waitLocks[lock]=threading.Condition()


"""
TURTLE
"""
def turtle(laps,delay):
    for counter in range(laps):
        print (threading.currentThread().getName()+"["+str(counter)+"]")
        time.sleep(delay);
        waitLocks[counter].acquire()
        waitLocks[counter].notifyAll()
        waitLocks[counter].release()
    rankLock.acquire()
    ranking.append(threading.currentThread().getName())
    rankLock.release()
    return
"""
HARE
"""
def hare(laps,sleepTime):
    slept=0
    for counter in range(laps):
        print (threading.currentThread().getName()+"["+str(counter)+"]")
        randomDice=random.randint(1, 100)
        if slept == 0 and randomDice > 80 :
            print (threading.currentThread().getName()+"[zzzZZZZ]")
            waitLocks[counter].acquire()
            sleepQuality=waitLocks[counter].wait(sleepTime)
            waitLocks[counter].release()
            slept=1

            if not sleepQuality :
                hareStatus="woken Up"
            else:
                hareStatus="God morning sunshine"
            print (threading.currentThread().getName()+"["+hareStatus+"]")
    rankLock.acquire()
    ranking.append(threading.currentThread().getName())
    rankLock.release()
    return

"""
MAIN LOOPS
"""

for i in range(read['turtle']):
    turtleName="turtle"+str(i)
    t = threading.Thread(name=turtleName,target=turtle,args=(laps,delay))
    threads.append(t)
    t.start()

for i in range(read['hare']):
    hareName="hare"+str(i)
    t = threading.Thread(name=hareName,target=hare,args=(laps,sleepTime))
    threads.append(t)
    t.start()

"""Polling"""
for animalThread in threads :
    animalThread.join()

counter=0
print  ("RANKING")
for animal in ranking:
    print ("#",counter,animal)
    counter+=1
