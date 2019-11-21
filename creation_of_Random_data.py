import random
import csv

global_line_count = 0
d = list()
with open("final_data.csv",errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if global_line_count == 0:
            global_line_count += 1
        else:
            d.append(int(row[0]))
            global_line_count += 1

total_data_points = 3800000
i = 283229
while not(total_data_points == 0):
	k = random.randint(5,50)
	if(total_data_points - k < 0):
		k = total_data_points
		total_data_points = 0
	for j in range(k):
		print(f'{i},{random.choice(d)},{random.choice([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])}')
	i +=1
	if(not(total_data_points - k < 0)):
		total_data_points -= k