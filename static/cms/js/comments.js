// 排序
$(function () {
    $('#sort-select').change(function () {
       var value = $(this).val();
       var newHref1 = zlparam.setParam(window.location.href,'sort',value);
       var newHref2 = zlparam.setParam(newHref1,'page',1);
       window.location = newHref2;
   });
});

//删帖
$(function () {
   $('.remove-btn').click(function () {
      var self = $(this);
      var tr = self.parent().parent();
      var comment_id = tr.attr('data-id');
      zlalert.alertConfirm({
         'msg': '确认删除此评论？',
         'confirmText': '确认',
         'cancelText': '取消',
         'confirmCallback' : function(){
             zlajax.post({
               'url':'/cms/dcomment/',
               'data':{
                  'comment_id':comment_id
               },
               'success':function (data) {
                  if(data['code'] === 200){
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