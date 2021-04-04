$(function () {
   $("#submit").click(function (event) {
       event.preventDefault();
       var emailE = $("input[name='email']");
       var passwordE = $("input[name='password']");
       var rememberE = $("input[name='remember']");

       var email = emailE.val();
       var password = passwordE.val();
       var remember = rememberE.checked ? 1:0;

       zlajax.post({
           'url':'/cms/login/',
           'data':{
               'email':email,
               'password':password,
               'remember':remember
           },
           'success':function (data) {
               if(data['code'] == 200){
                   zlalert.alertSuccessToast('登录成功!');
                   setTimeout(function () {
                       window.location = '/cms/'
                   },1200)

               }else{
                   var message = data['message'];
                   $("#message-p").html(message);
                   $("#message-p").show();
                   passwordE.val("");
                   if(message =='请输入正确邮箱格式'){
                       emailE.val("");
                   }
                }
           },
           'fail':function (error) {
               zlalert.alertNetworkError();

           }
       })
   })
});