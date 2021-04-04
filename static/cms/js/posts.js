$(function () {
    $(".highlight-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";
        }else{
            url = "/cms/hpost/";
        }
        zlajax.post({
            'url': url,
            'data': {
                'post_id': post_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $('.remove-btn').click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var post_id = tr.attr("data-id");
        zlalert.alertConfirm({
            'msg': '确认删除这篇帖子？',
            'confirmText': '确认',
            'cancelText': '取消',
            'confirmCallback': function(){
                zlajax.post({
                    'url': '/cms/dpost/',
                    'data': {
                        'post_id': post_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                    }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        })
    }
});
})
});

// 排序的事件
$(function () {
    $('#sort-select').change(function (event) {
       var value = $(this).val();
       var newHref = zlparam.setParam(window.location.href,'sort',value);
       window.location = newHref;
   });
});


// 板块过滤的
$(function () {
    $("#board-filter-select").change(function (event) {
       var value = $(this).val();
       var newHref = zlparam.setParam(window.location.href,'board',value);
       var newHref = zlparam.setParam(newHref,'page',1);
       window.location = newHref;
   });
});