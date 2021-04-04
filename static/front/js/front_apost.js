
$(function () {
    var ue = UE.getEditor("editor",{
        "serverUrl": '/ueditor/upload/'
    });

    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var boardSelect = $("select[name='board_id']");
        var a = document.getElementById('find-author-a');
        var author_id =a.getAttribute('user-id');


        var title = titleInput.val();
        var board_id = boardSelect.val();
        //获取文本内容
        var content = ue.getContent();

        zlajax.post({
            'url': '/add_post/',
            'data': {
                'title': title,
                'content':content,
                'board_id': board_id,
                'author_id': author_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertConfirm({
                        'msg': '恭喜！帖子发表成功！',
                        'cancelText': '回到首页',
                        'confirmText': '再发一篇',
                        'cancelCallback': function () {
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            titleInput.val("");
                            ue.setContent("");
                        }
                    });
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});