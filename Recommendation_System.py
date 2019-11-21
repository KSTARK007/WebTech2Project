import csv
from collections import Counter
import random

number_data = 421261
number_of_movies_per_view = 15

d = dict()
for i in range(number_data+1):
    sa = list()
    d[i]=sa
global_line_count = 0
with open("rating_data_real_syn.csv",errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if global_line_count == 0:
            global_line_count += 1
        else:
            d[int(row[0])].append(int(row[1]))
            global_line_count += 1

user=dict()
def recommend(id,v):
    friend=dict()
    movie_r=dict()
    Recomended_movies=dict()
    user[id]=v
    for j in user[id]:
        for i in range(number_data):
            if(j in d[i]):
                friend[i]=d[i]
        for ii in friend.keys():
            for jj in friend[ii]:
                if(not(jj in movie_r.keys())):
                    movie_r[jj] = 1
                else:
                    movie_r[jj] += 1
        for val in user[id]:            
            try:
                del movie_r[val]  
                
            except Exception as e:
                print("Key 'testing' not found")
                print(e)
                continue
        # print(movie_r)
        # print(" ")
        # print(friend)
        maxheap = Counter(movie_r)
        maximum = maxheap.most_common(number_of_movies_per_view)
        # print(maximum)
        # print("  ")
        for val in maximum:
            if(not(val[0] in Recomended_movies.keys())):
                Recomended_movies[val[0]]=val[1]
            else:
                Recomended_movies[val[0]]+=val[1]
    # print(Recomended_movies)
    m = Counter(Recomended_movies)
    out = m.most_common(len(Recomended_movies))
    R=dict()
    for i in out:
        R[i[0]] = i[1] 
    print(R)
    print(len(R))
    print("")
    print("")
    print("")
    return(R)

recommend(500000,[58972, 2858, 1198, 1580, 296])
## TESTING

"""
global_line_count = 0
dd = list()
with open("final_data.csv",errors='ignore') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if global_line_count == 0:
            global_line_count += 1
        else:
            dd.append(int(row[0]))
            global_line_count += 1

n_user = random.randint(5,20)
print("Number of users")
print(n_user)

final_ans = dict()

for i in range(n_user):
    m_user = random.randint(1,15)
    print("Number of movies watched by the users")
    print(m_user)
    print(" ")
    li = list()
    for j in range(m_user):
        li.append(random.choice(dd))
    print(li)
    b = recommend(500000,li)
    for i in b.keys():
        if(i in final_ans.keys()):
            final_ans[i] +=1
        else:
            final_ans[i] = 1

mmm = Counter(final_ans)
ooout = mmm.most_common(len(final_ans))
Rr=dict()
for i in ooout:
    Rr[i[0]] = i[1] 

print(" ")
print(" ")
print(" ")
print("Number of users")
print(n_user)
print("number of recommend movies")
print(len(Rr))
print(" ")
print(Rr)

"""