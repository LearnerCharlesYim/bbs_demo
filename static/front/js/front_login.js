//点击随机生产验证码
$(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});

$(function(){
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var graph_captcha_input = $("input[name='graph_captcha']");
        var remember_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var graph_captcha = graph_captcha_input.val();
        var remember = remember_input.checked ? 1:0;


        zlajax.post({
            'url': '/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'graph_captcha':graph_captcha,
                'remember':remember
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                    zlalert.alertSuccessToast('登录成功!');
                    setTimeout(function () {
                        if(return_to){
                        window.location = return_to;
                    }else{
                        window.location = '/';
                    }
                    },1200);

                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});