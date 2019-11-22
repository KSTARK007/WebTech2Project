function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}


function createElements(year,ImageSrc,imdb,tomato,nservices,service1,service2){


mainDiv = document.createElement("div")
mainDiv.classList.add("imageContainer")



image = document.createElement("img")
image.src = ImageSrc
image.classList.add("image")
image.style.width=100%
mainDiv.append(image)

service = document.createElement("img")
service.src = "static/img/"+service1+".svg"
service.classList.add("service1")
mainDiv.append(service)

if(nservices >= 2)
{
    sservice = document.createElement("img")
    sservice.src = "static/img/"+service2+".svg"
    sservice.classList.add("service2")
    mainDiv.append(sservice)
}


textDiv = document.createElement("div");
textDiv.innerHTML=year
textDiv.classList.add("text")


middleDiv = document.createElement("div");
middleDiv.classList.add("middle")
middleDiv.append(textDiv)
mainDiv.append(middleDiv)



imdbimg = document.createElement("img")
imdbimg.src = "static/img/imdb.svg"
imdbimg.classList.add("imdbimg")
mainDiv.append(imdbimg)

tomatoimg = document.createElement("img")
tomatoimg.src = "static/img/tomato.svg"
tomatoimg.classList.add("tomatoimg")
mainDiv.append(tomatoimg)

imdbScore = document.createElement("div");
imdbScore.innerHTML=imdb + "/10"
imdbScore.classList.add("text")
imdbScore.classList.add("imdbtext")
mainDiv.append(imdbScore)


tomatoScore = document.createElement("div");
tomatoScore.innerHTML=tomato
tomatoScore.classList.add("text")
tomatoScore.classList.add("tomatotext")
mainDiv.append(tomatoScore)

return mainDiv

}







$(document).ready(function(){

    $.get('http://localhost:5000/api/popMovie',function(d){
        var data = d ; 
        var c = 0;          
        for (var i = 0; i < data.data.length/2; i++) {
            $.get('http://localhost:5000/api/movie/'+data.data[i],function(d){
                console.log(d.ret[0])
                if(d.ret.length == 1){
                    imageSrc="static/img/"+d.ret[0]["service"]+"/"+d.ret[0]["Name"]+".jpg"
                    if(UrlExists(imageSrc)){
                    var k = createElements(d.ret[0]["Year"],imageSrc,d.ret[0]["IMDB_Rating"],d.ret[0]["RottenTomato"],1,d.ret[0]["service"])
                    }
                }
                if(d.ret.length == 2){
                    imageSrc="static/img/"+d.ret[0]["service"]+"/"+d.ret[0]["Name"]+".jpg"
                    if(UrlExists(imageSrc)){
                    var k = createElements(d.ret[0]["Year"],imageSrc,d.ret[0]["IMDB_Rating"],d.ret[0]["RottenTomato"],2,d.ret[0]["service"],d.ret[1]["service"])   
                    }
                }
                $('#0').append(k)
            });
        }

        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))
        $('<br>').insertAfter($('#0'))

         for (var i = 5; i < data.data.length; i++) {
            $.get('http://localhost:5000/api/movie/'+data.data[i],function(d){
                console.log(d.ret[0])
                if(d.ret.length == 1){
                    imageSrc="static/img/"+d.ret[0]["service"]+"/"+d.ret[0]["Name"]+".jpg"
                    var k = createElements(d.ret[0]["Year"],imageSrc,d.ret[0]["IMDB_Rating"],d.ret[0]["RottenTomato"],1,d.ret[0]["service"])
                }
                if(d.ret.length == 2){
                    imageSrc="static/img/"+d.ret[0]["service"]+"/"+d.ret[0]["Name"]+".jpg"
                    var k = createElements(d.ret[0]["Year"],imageSrc,d.ret[0]["IMDB_Rating"],d.ret[0]["RottenTomato"],2,d.ret[0]["service"],d.ret[1]["service"])
                }
                $('#1').append(k)
            });
        }



    });
});