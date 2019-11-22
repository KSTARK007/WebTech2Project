function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}





var a = -1
function update(){
    a = a + 1
    return a
}
function resetC(){
    a = -1
}

$(document).ready(function(){

    $.get('http://localhost:5000/api/recmovie/1000019',function(d){
        var data = d ;
        var c = 0;           
        for (var i = 0; i < 10; i++) {
            $.get('http://localhost:5000/api/movie/'+data.data[i],function(d){
                console.log(a)                
                imageSrc="static/img/"+d.ret[0]["service"]+"/"+d.ret[0]["Name"]+".jpg"
                $('#'+update()).find('img').attr("src",imageSrc)
            });
        }
        resetC()

       
    });

    $('.customer-logos').slick({
        slidesToShow: 6,
        slidesToScroll: 5,
        autoplay: true,
        autoplaySpeed: 2000,
        arrows: false,
        dots: false,
        pauseOnHover: true,
        responsive: [{
            breakpoint: 768,
            settings: {
                slidesToShow: 4
            }
        }, {
            breakpoint: 520,
            settings: {
                slidesToShow: 3
            }
        }]
    });


});