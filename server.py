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

@app.route('/login')
def loginPage():
    return render_template('login.html')


# client = MongoClient('mongo',27017)
client = MongoClient(port=27017)
users_table  = client.webtech.user
movie_table = client.webtech.movie
counter = client.webtech.orgid_counter



### =========================================================================================================
### recommender functions 
### =========================================================================================================

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
### =========================================================================================================



def getNextSequence(collection,name):
    collection.update_one( { '_id': name },{ '$inc': {'seq': 1}})
    return int(collection.find_one({'_id':name})["seq"])




### =========================================================================================================
### User based API's
### =========================================================================================================


## login 

"""
input
{
    username : 
    password : 
}

"""
@app.route('/api/login', methods=['POST'])
def login():
    j = request.get_json()
    name = j['username']
    password = j['password']
    val = users_table.find_one({"username":j['username']})
    if(val is None):
        return jsonify({'error':'user does not exist'})
    if(password != val['password']):
        return jsonify({'error':'wrong password'})   
    return jsonify({'code' : 200})





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




## adding new movies watched and re running recomendation
"""
input:
{
    data: movieId ( int )
}

"""

@app.route('/api/addView/<uid>', methods=['POST'])
def addMovieView(uid):
    uid = int(uid)
    j = request.get_json()
    val = users_table.find_one({"userId":uid})
    if(val is None):
        return jsonify({'error':'user does not exist'})
    ll = val["movies"]
    if(int(j["data"]) in ll):
        return jsonify({'error':'already added to view'})
    ll.append(int(j["data"]))
    k = recommend(uid,ll)
    dd = list()
    for i in k.keys():
        dd.append(int(i))
    p = users_table.update_one({"userId":uid},{'$unset':{"movies":""}})
    result=users_table.update_one({"userId":uid},{"$set":{"movies":ll}})
    users_table.update_one({"userId":uid},{"$unset":{"recommendation":""}})
    result=users_table.update_one({"userId":uid},{"$set":{"recommendation":dd}})
    return jsonify({'code':200})



## Geting the user ID of the username

"""

Output:
{
    data: movieId (int)
}
"""
@app.route('/api/getUserId/<username>', methods=['GET'])
def getUserId():
    j = request.get_json()
    val = users_table.find_one({"username":username})
    if(val is None):
        return jsonify({'error':'user does not exist'})   
    return jsonify({'data':val['userId']})



### =========================================================================================================
###  Movie based APIs
### =========================================================================================================

#To Be Done - Jaydeep

#home page pop movies
"""
output
{
    data: [<10 movies> (int)]
}
"""
@app.route('/api/popMovie', methods=['GET'])
def popMovie():
    l = [1203,296,1198,1580,2858,1291,32,1136,640,185029]
    return jsonify({"data":l})


@app.route('/api/recmovie/<userid>', methods=['GET'])
def rMovie(userid):
    val = users_table.find_one({"userId":int(userid)})
    if(val is None):
        return jsonify({'error':'user does not exist'})   
    return jsonify({'data':val['recommendation']})



# list of movies for signup
"""
output
{
    data: [ <80 movies> ] <present 20>
}

# d["Animation"] = [178827,181235,5690,161644,171013,3751,741,27186,181671,166291]
# d["Biography"] = [74324,56744,527,1228,102819,6620,4211,106100,63876,27020]
# d["Comedy"] = [73881,163745,190089,184807,187531,176349,170729,3061,164369,167990]
# d["Crime"] = [1203,190857,3966,2130,162418,111,2917,6898,8645,8042]
# d["Documentary"] = [100196,118920,1361,172705,117364,1361,1192,183329,105744,173197]
# d["Drama"] = [33288,2071,5169,4522,2071,27410,97984,27410,186505,192385]
# d["Horror"] = [179749,155625,2160,7115,640,5489,2664,1345,123107,144976]

"""
@app.route('/api/signupMovies', methods=['GET'])
def signupMovie():
    outMovies = dict()
    outMovies["data"] = [179749,155625,2160,7115,640,5489,2664,1345,123107,144976,33288,2071,5169,4522,2071,27410,97984,27410,186505,192385,100196,118920,1361,172705,117364,1361,1192,183329,105744,173197,1203,190857,3966,2130,162418,111,2917,6898,8645,8042,73881,163745,190089,184807,187531,176349,170729,3061,164369,167990,86892,185087,7072,1224,71468,117928,1209,1301,2947,189333,178827,181235,5690,161644,171013,3751,741,27186,181671,166291,178827,181235,5690,161644,171013,3751,741,27186,181671,166291]
    final = random.sample(outMovies["data"],40)
    return jsonify({"data":final})




# Given a mi=ovie ID return the details of the movie
@app.route('/api/movie/<movieId>', methods=['GET'])
def Movie(movieId):
    caty = movie_table.find({"GlobalId" : movieId},{'_id':False})
    ret = list()
    for x in caty:
        ret.append(x)
    return jsonify({'ret':ret}),200







if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    createData()
    app.run(debug=True, host='0.0.0.0', port=port)