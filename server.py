import random, os, json, datetime, time ,string
from flask import *
import hashlib
from pymongo import *
import string 
import datetime
import re
from flask_cors import CORS
import csv
from collections import Counter
import random

app = Flask(__name__)
CORS(app)


@app.errorhandler(404)
def page_not_found(e):
    return "bla",404

@app.route('/')
def index():
    return render_template('index.html')

# client = MongoClient('mongo',27017)
client = MongoClient(port=27017)
users_table  = client.webtech.user
movie_table = client.webtech.movie
counter = client.webtech.orgid_counter


### recommender functions 

number_data = 421261
number_of_movies_per_view = 15


user=dict()

def createData():
    global_line_count = 0
    global d
    d = dict()
    for i in range(number_data+1):
        sa = list()
        d[i]=sa
    with open("rating_data_real_syn.csv",errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if global_line_count == 0:
                global_line_count += 1
            else:
                d[int(row[0])].append(int(row[1]))
                global_line_count += 1


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
                continue

        maxheap = Counter(movie_r)
        maximum = maxheap.most_common(number_of_movies_per_view)
        for val in maximum:
            if(not(val[0] in Recomended_movies.keys())):
                Recomended_movies[val[0]]=val[1]
            else:
                Recomended_movies[val[0]]+=val[1]
    m = Counter(Recomended_movies)
    out = m.most_common(len(Recomended_movies))
    R=dict()
    for i in out:
        R[i[0]] = i[1] 
    # print(R)
    # print(len(R))
    # print(" ")
    return(R)




### End of recommender functions


### =========================================================================================================





### id increment

def getNextSequence(collection,name):
    collection.update_one( { '_id': name },{ '$inc': {'seq': 1}})
    return int(collection.find_one({'_id':name})["seq"])

### end of id increment


### =========================================================================================================






### User based API's

##
@app.route('/api/v1/users', methods=['POST'])
def process():

    j = request.get_json()
    name = j['name']
    password = j['password']
    # if( len(password) != 40 or not all(c in string.hexdigits for c in password) ):
    #     return jsonify({'code' : 600})

    # if name and password and password != "da39a3ee5e6b4b0d3255bfef95601890afd80709":
    #     if(db.count_documents({"name":name})>0):
    #         return jsonify({'code' : 405})
    result=db.insert_one({'userId': getNextSequence(counter,"userId"), 'name': name, 'password' : password })
    
    return jsonify({'code' : 201})
    # return jsonify({'code' : 400})



### =========================================================================================================

## sign up and init recommendation 
"""
input: 
{
    username : 
    password :
    movies : {}
}

extra 
    run recommendations


"""
@app.route('/api/adduser/', methods=['POST'])
def userSignup():
    j = request.get_json()
    val = users_table.find_one({"username":j['username']})
    if(val is not None):
        return jsonify({'error':'user already exist'})
    nextId = getNextSequence(counter,"userId")  
    k = recommend(nextId,j["movies"])
    ll = list()
    for i in k.keys():
        ll.append(int(i))
    result=users_table.insert_one({'userId':nextId,"username":j['username'],"password":j['password'],"movies":j['movies'],"recommendation":ll})
    return jsonify({'code':200})

### =========================================================================================================



### adding new movies watched and re running recomendation
"""
input:
{
    data: movieId ( int )
}

"""

@app.route('/api/v1/addView/<uid>', methods=['POST'])
def addMovieView():
    j = request.get_json()
    val = users_table.find_one({"userId":uid})
    if(val is not None):
        return jsonify({'error':'user does not exist'})
    ll = val["movies"]
    ll.append(int(j["data"]))
    k = recommend(uid,ll)
    dd = list()
    for i in k.keys():
        dd.append(int(i))
    users_table.update_one({"userId":uid},{"$unset":{"movies":""}})
    result=users_table.update_one({'userId':uid,'$set':{'movies':ll}})
    users_table.update_one({"userId":uid},{"$unset":{"recommendation":""}})
    result=users_table.update_one({'userId':uid,'$set':{'recommendation':dd}})
    return jsonify({'code':200})


### =========================================================================================================





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    createData()
    app.run(debug=True, host='0.0.0.0', port=port)