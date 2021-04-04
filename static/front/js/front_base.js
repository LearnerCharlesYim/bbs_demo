//网页置顶功能
$(function () {
    var button = document.getElementById('return-top');
    document.onscroll = function(){
        // console.log(document.documentElement.scrollTop);
        if(document.documentElement.scrollTop > 0){
            button.style.display = null;
        }else {
             button.style.display = "none";
        }
    };
    button.onclick = function () {
    var timer = setInterval(function(){
            if(document.documentElement.scrollTop <= 0){
                document.documentElement.scrollTop = 0;
                clearInterval(timer);
            }else{
                var temp = document.documentElement.scrollTop;
                document.documentElement.scrollTop = (temp - 50);
            }
        },1000/1800)
    };

}
);

