import sys


f = open('route.txt' , 'r')

for x in range (0,13):
        if(x%2 == 0):
            lane = f.readline()
            lane = lane[::1]
            print(lane.strip('\n'))
                  
        elif(x%2 == 1):
            lane = f.readline()
            lane = lane[::-1]
            print(lane.strip('\n'))


