// 排序的事件
$(function () {
    $('#sort-select').change(function (event) {
       var value = $(this).val();
       var newHref1 = zlparam.setParam(window.location.href,'sort',value);
       var newHref2 = zlparam.setParam(newHref1,'page',1);
       window.location = newHref2;
   });
});
