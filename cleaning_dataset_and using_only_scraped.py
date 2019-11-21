import csv
global_line_count = 0

# l = ["amazon_movies.csv","netflix_movies.csv","hbo_movies.csv","hulu_movies.csv"]
# for i in l:
#     with open(i) as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         for row in csv_reader:
#             if global_line_count == 0:
#                 # print(f'line_count,{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},service')
#                 global_line_count += 1
#             else:
#                 # print(f'{global_line_count},{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{i.split("_")[0]}')
#                 print(f'{row[0]}')
#                 global_line_count += 1
# print(global_line_count)
down= dict()
with open("movies_dataset_downloaded.csv",errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if global_line_count == 0:
                # print(f'line_count,{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},service')
                global_line_count += 1
            else:
                # print(f'{global_line_count},{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{i.split("_")[0]}')
                # print(f'{row[1]}')
                try:
                    k = row[1].split("(")[0]
                    down[row[0]] = k[0:len(k)-1]
                except Exception as e:
                    continue
                global_line_count += 1
global_line_count = 0
l = list()
with open("data.csv",errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if global_line_count == 0:
                print(f'GlobalId,localId,Name,Year,Rating,IMDB_Rating,RottenTomato,Genre,service')
                global_line_count += 1
            else:
                for i in down.keys():
                    if(row[1] == down[i]):
                        print(f'{i},{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]},{row[7]}')
                        break
                # print(f'{row[1]}')
                l.append(row[1])
                global_line_count += 1

# count = 0
# for i in down:
#     for j in l:
#         if(j == i):
#             # print(j)
#             count +=1
# print(l)
# print(global_line_count)
# print(down)
# print(len(l))
# print(len(down))