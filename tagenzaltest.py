import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('parsed_gcode.p', 'rb') as f:
    list = pickle.load(f)

print(list[0:5])

list_len = len(list)-3
counter_kleine_winkel = 0
winkel_list = []

for i in range(10000):#(list_len):
    #G2 G3 abfangen:
    #print(type(list[i+1][0]))
    if list[i+1][0] == 3:
        alpha = False
        print("False", i+1, "davor")
    elif list[i+2][0] == 3:
        print("False", i+1, "danach")
    else:
        #Zeile,Koordinaten,x/y
        #      1           0/1
        alpha12 = np.arctan2(list[i+1][1][1]-list[i][1][1], list[i+1][1][0]-list[i][1][0])
        alpha23 = np.arctan2(list[i+2][1][1]-list[i+1][1][1], list[i+2][1][0]-list[i+1][1][0])

        alpha = - alpha12 + alpha23
        if alpha >= np.pi:
            alpha = alpha-np.pi*2
            print("ABGEFANGEN Groß...")
        if alpha <= -np.pi:
            alpha = alpha+np.pi*2
            print("ABGEFANGEN Klein...")

        if ((alpha <= 0.0174533) and (alpha >= -0.0174533)):
            print("chillig...")
            counter_kleine_winkel += 1


        print("ALPHA", i+1, ": ", alpha, "  ( alpha12: ", alpha12, "  alpha23: ", alpha23," )")
        winkel_list.append(alpha)

print("kleine Winkel:", counter_kleine_winkel)


plt.hist(winkel_list, bins = 360)
plt.show()

ax = plt.figure().add_subplot(projection='3d')
ax.plot([line[1][0] for line in list], [line[1][1] for line in list], [line[1][2] for line in list], label='parametric curve')

plt.show()
