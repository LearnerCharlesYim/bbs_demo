$(function () {
    var ue = UE.getEditor("editor",{
        'serverUrl': '/ueditor/upload/',
        "toolbars": [
            [
                'undo', //撤销
                'redo', //重做
                'bold', //加粗
                'italic', //斜体
                'source', //源代码
                'blockquote', //引用
                'selectall', //全选
                'insertcode', //代码语言
                'fontfamily', //字体
                'fontsize', //字号
                'simpleupload', //单图上传
                'emotion' //表情
            ]
        ]
    });
    window.ue = ue;
});

//事件委托
function eventDelegate (parentSelector, targetSelector, events, foo) {
  // 触发执行的函数
  function triFunction (e) {
    // 兼容性处理
    var event = e || window.event;

    // 获取到目标阶段指向的元素
    var target = event.target || event.srcElement;

    // 获取到代理事件的函数
    var currentTarget = event.currentTarget;

    // 处理 matches 的兼容性
    if (!Element.prototype.matches) {
      Element.prototype.matches =
        Element.prototype.matchesSelector ||
        Element.prototype.mozMatchesSelector ||
        Element.prototype.msMatchesSelector ||
        Element.prototype.oMatchesSelector ||
        Element.prototype.webkitMatchesSelector ||
        function(s) {
          var matches = (this.document || this.ownerDocument).querySelectorAll(s),
            i = matches.length;
          while (--i >= 0 && matches.item(i) !== this) {}
          return i > -1;
        };
    }

    // 遍历外层并且匹配
    while (target !== currentTarget) {
      // 判断是否匹配到我们所需要的元素上
      if (target.matches(targetSelector)) {
        var sTarget = target;
        // 执行绑定的函数，注意 this
        foo.call(sTarget, Array.prototype.slice.call(arguments))
      }

      target = target.parentNode;
    }
  }

  // 如果有多个事件的话需要全部一一绑定事件
    if (events){
        events.split('.').forEach(function (evt) {
    // 多个父层元素的话也需要一一绑定
    Array.prototype.slice.call(document.querySelectorAll(parentSelector)).forEach(function ($p) {
        $p.addEventListener(evt, triFunction);
        });
      });
    }
}


//评论点赞
$(eventDelegate('#ul', '#a1', 'click',
function() {
  console.log(this);
  var that = this;
  var comment_id = this.getAttribute('comment-id');
  var loginTag = document.getElementById('find-author-a');
  if (!loginTag) {
    window.location = '/login/';
  } else {
    var user_id = loginTag.getAttribute('user-id');
    if (this.getAttribute('statue') == "False") {
      zlajax.post({
        'url': '/like_comment/',
        'data': {
          'user_id': user_id,
          'comment_id': comment_id
        },
        'success': function(data) {
          if (data['code'] == 200) {
            var sum = data['data']['sum'];
            that.innerHTML = '<span  class="glyphicon glyphicon-thumbs-up author-info " aria-hidden="true"></span>' + '(' + sum + ')';
            that.setAttribute('statue', 'True');

          } else {
            zlalert.alertInfo(data['message']);
          }
        }
      });
    } else {
      zlajax.post({
        'url': '/dislike_comment/',
        'data': {
          'user_id': user_id,
          'comment_id': comment_id
        },
        'success': function(data) {
          if (data['code'] == 200) {
            that.setAttribute('statue', 'False');
            var sum = data['data']['sum'];
            that.innerHTML = '<span  class="glyphicon glyphicon-thumbs-up author-info " aria-hidden="true"></span>' + '(' + sum + ')';
          } else {
            zlalert.alertInfo(data['message']);
          }
        }
      });

    }
  }

}));

//评论
$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();

        var loginTag = document.getElementById('find-author-a');
        if(!loginTag){
            window.location = '/login/';
        }else{
            if($("#comment-content")){
                 var comment_id = $("#comment-content").attr("comment-id");
            }else{
                comment_id = "";
            }
            var content = window.ue.getContent();
            var post_id = $("#post-content").attr("data-id");
            zlajax.post({
                'url': '/acomment/',
                'data':{
                    'comment_id':comment_id,
                    'content': content,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});

//帖子点赞
$(function () {
    $("#like-btn").click(function (event) {
        var loginTag = document.getElementById('find-author-a');
        if(!loginTag){
            window.location = '/login/';
        }else{
            button = document.getElementById('like-btn');
            var post_id = $("#post-content").attr("data-id");

            var user_id =loginTag.getAttribute('user-id');
            if ( button.className.indexOf('danger') > 0){
                zlajax.post({
                'url': '/astar/',
                'data':{
                    'user_id': user_id,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        button.className = 'glyphicon glyphicon-thumbs-up btn btn-primary btn-sm';
                        var raw = data['data']['sum'];
                        // var sum = raw.toString();
                        button.innerText = '取消点赞'+' '+raw;


                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });



        }else{
                zlajax.post({
                'url': '/dstar/',
                'data':{
                    'user_id': user_id,
                    'post_id': post_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        button.className = 'glyphicon glyphicon-thumbs-up btn btn-danger btn-sm';
                        var raw = data['data']['sum'];
                        // var sum = raw.toString();
                        button.innerText = ' 点 赞'+' '+raw;
                    }else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });


        }
        }


    })
});

//回复评论
$(eventDelegate('#ul', '#a2', 'click', function () {
         console.log(this);
         // var that = this;
         var comment_id = this.getAttribute('comment-id');
         if (document.getElementById('abc')){
             var divDom = document.getElementById('abc');
             var parent = divDom.parentNode;
             parent.removeChild(divDom);
         }
         var comment_id = this.getAttribute('comment-id');
         var loginTag = document.getElementById('find-author-a');
                     if(!loginTag){
            window.location = '/login/';
        }else{
            var user_id = loginTag.getAttribute('user-id');
            zlajax.get({
            'url': '/load_reply/',
            'data':{
                'comment_id': comment_id
            },
            'success': function (data) {
                if(data['code'] == 200){

                    var comment_author = data['data']['comment_author'];
                    var comment_content =  data['data']['comment_content'];
                    var parent = document.getElementById('addcomment');

                    var divDom = document.createElement("div");
                    divDom.id = 'abc';

                    divDom.innerHTML = `

                            <div class="bbs-post-web-quote-thread">
                                <div class="bbs-thread-comp quote-thread">
                                    <div class="bbs-thread-comp-container">
                                        <div class="quote-text">引用 @<a href="#">${comment_author}</a>发表的：</div>
                                        <div  id="comment-content" comment-id="${comment_id}" class="reply-thread">${comment_content}</div>
                                        <span id="buttons" class="reply-close-btn glyphicon glyphicon-remove aria-hidden="true"></button>
                                    </div>
                                </div>

                            </div>
                    `;
                    parent.insertBefore(divDom,document.getElementById("editor"));
                    var button = document.getElementById('buttons');
                    button.onclick = function () {
                        var parent = divDom.parentNode;
                        parent.removeChild(divDom);
                    };

                }else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
        }

}));


//异步加载评论
$(function () {
    var temp = 5;
    $("#click-more").click(function () {
        var loginTag = document.getElementById('find-author-a');
        if(!loginTag){
            zlalert.alertConfirm({
                'msg': '登录查看更多精彩评论！',
                'cancelText': '返回',
                'confirmText': '登录',
                'confirmCallback': function () {
                    window.location = '/login/';
                }
            });
        }else{
            var button = document.getElementById('click-more');
            var index =parseInt(button.getAttribute('index'));

            var post_id = $("#post-content").attr("data-id");
            zlajax.get({
                'url': '/load_comment/',
                'data':{
                    'post_id': post_id,
                    'index': index
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        index +=5;
                        var indexToString = index +'';
                        button.setAttribute('index',indexToString);
                        var comments_info = data['data']['comments_info'];
                        var parent = document.getElementById('ul');
                        var img = data['data']['logo_img'];
                        for(var i=0;i<comments_info.length;i++){
                            var comment_id = comments_info[i]['comment_id'];
                            var avatar = comments_info[i]['avatar'];
                            var content = comments_info[i]['content'];
                            var conmment_like_authors = comments_info[i]['conmment_like_authors'];
                            var create_time = comments_info[i]['create_time'];
                            var username = comments_info[i]['username'];
                            var comment_stars = comments_info[i]['comment_stars'];
                            var raw_time = new Date(parseInt(create_time)*1000);
                            var time = raw_time.toLocaleDateString().replace(/\//g, "-") + " " + raw_time.toTimeString().substr(0, 8);
                            var user_id =loginTag.getAttribute('user-id');
                            var statue;
                            if (conmment_like_authors.indexOf(user_id) == -1){
                               statue = 'False';
                            }else{ statue = 'True'}
                            var liDom = document.createElement("li");

                            var src;
                            if (avatar){
                                src = avatar;
                            }else{
                                src = img;
                            }
                            var text;
                            if(comments_info[i]['comment_father_author_name']){
                                text = `<div class="bbs-post-web-quote-thread">
                                                <div class="bbs-thread-comp quote-thread">
                                                    <div class="bbs-thread-comp-container">
                                                        <div class="quote-text">引用 @<a href="#">${comments_info[i]['comment_father_author_name']}</a>发表的：</div>
                                                        <div class="reply-thread">${comments_info[i]['comment_father_comment_content']}</div>

                                                    </div>
                                                </div>
                                                </div>
                                `;
                            }else{
                                text = '';
                            }

                            liDom.innerHTML = `
                                    <div class="itm">
                                        <div class="head">
                                            <img src=${src} alt="">
                                        </div>
                                    <div class="comment-content cntwrap">
                                        <div id="${comment_id}" class="cnt f-brk">
                                            <p class="author-info cnt f-brk">
                                                <a href="#">${username}</a> `+ text +
                                          `      
                                            ${content}
                                            </p>
                                        </div>
                                    <div>

                                        <div class="time s-fc4 author-info" style="float: left;">${time}</div>
                                        <div style="float: right;padding-right: 10px;">
                                            <a id="a1" href="javascript:void(0)" statue="${statue}" comment-id="${comment_id}" class="s-fc3 like-comment-a">
                                                <span  class="glyphicon glyphicon-thumbs-up author-info " aria-hidden="true"></span>(${comment_stars})
                                            </a>
                                            <span>|</span>
                                            <a id="a2" href="#addcomment" comment-id="${comment_id}" class="author-info">回复</a>
                                        </div>

                                    </div>
                                </div>
                            </div>
                            `;
                            parent.appendChild(liDom);
                        }



                    }else{
                        button.innerText = data['message'];
                    }



                }
            })
        }

    });
});



