
$(function () {
   $('#submit').click(function (event) {
       event.preventDefault();

       var checkedInputs = $(':checkbox:checked');
       var roles = [];
       checkedInputs.each(function () {
          var role_id = $(this).val();
           roles.push(role_id);
       });
        var user_id = $(this).attr('data-user-id');
        zlajax.post({
            'url': '/cms/cusers/edit/',
            'data':{
                'user_id': user_id,
                'roles': roles
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('恭喜！CMS用户信息修改成功！');
                    setTimeout(function () {
                        window.location.href = '/cms/cusers';
                    },1000)
                }else{
                    zlalert.alertInfoToast(data['message']);
                }
            }
        })
   });
});

$(function () {
   $('#black-list-btn').click(function (event) {
       event.preventDefault();
        var user_id = $(this).attr('data-user-id');
        var is_active = parseInt($(this).attr('data-is-active'));

        var is_black = is_active;

        zlajax.post({
            'url': '/cms/cusers/black_cuser/',
            'data':{
                'user_id': user_id,
                'status': is_black
            },
            'success': function (data) {
                if(data['code'] == 200){
                    var msg = '';
                    if(is_black){
                        msg = '恭喜！已经将该用户拉入黑名单！'
                    }else{
                        msg = '恭喜！已经将该用户移出黑名单！'
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
   })
});
