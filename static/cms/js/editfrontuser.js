
$(function () {
    $('#black-btn').click(function (event) {
        event.preventDefault();

        var status = parseInt($(this).attr('user-status'));
        var user_id = $(this).attr('data-user-id');


        zlajax.post({
            'url': '/cms/black_front_user/',
            'data': {
                'user_id': user_id,
                'user_status': status
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(status){
                        msg = '恭喜！已经将该用户加入黑名单！';
                    }else{
                        msg = '恭喜！已经将该用户移出黑名单！';
                    }
                    zlalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfoToast(data['message']);
                }
            }
        })
    });
});
