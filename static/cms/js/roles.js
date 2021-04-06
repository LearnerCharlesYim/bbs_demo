$(function () {
    $('.delete-role-btn').click(function (event) {
        event.preventDefault();
        var role_id = $(this).attr('data-role-id');
        zlalert.alertConfirm({
            msg: '您确定要删除这个分组吗？',
            confirmCallback: function () {
                // 发送ajax
                zlajax.post({
                    url: '/cms/croles/delete/',
                    data:{
                        'role_id': role_id
                    },
                    success: function (data) {
                        if(data['code'] == 200){
                            setTimeout(function () {
                                zlalert.alertSuccessToast('恭喜！CMS组删除成功！');
                            },200);
                            setTimeout(function () {
                                // 重新加载这个页面
                                window.location.reload();
                            },1400);
                        }else{
                            setTimeout(function () {
                                zlalert.alertInfoToast(data['message']);
                            },200);
                        }
                    }
                })
            }
        });
    });
});


$(function () {
   $('#new-group-btn').click(function () {
       $("#edit-btn").css('display','none');
       $("#submit-btn").css('display','');
   })
});

// 添加用户组
$(function () {
    $("#submit-btn").click(function (event) {
        event.preventDefault();

        // 获取组名
        var name = $("input[name='name']").val();
        var desc = $("input[name='desc']").val();
        var permission_inputs = $("input[name='permission']:checked");
        var permissions = [];
        $.each(permission_inputs,function (idx,obj) {
            permissions.push($(obj).val());
        });
        var data = {
            name:name,
            desc:desc,
            permissions: permissions
        };

        zlajax.post({
            url: '/cms/croles/',
            data: data,
            success: function (data) {
                if(data['code']==200){
                    zlalert.alertSuccessToast('恭喜，CMS组添加成功！');
                setTimeout(function () {
                    // 跳转到组管理页面
                    window.location = '/cms/croles/';
                },1200);
                }else{
                    zlalert.alertInfoToast(data['message']);
                }
            },
        });
    });
});


//修改
$(function(){
    $('.edit-role-btn').click(function(event){
        $("#submit-btn").css('display','none');
        $("#edit-btn").css('display','');
        var self = $(this);
        var role_id = $(this).attr('data-role-id');
        var dialog = $("#role-dialog");
        dialog.modal("show");
        var tr = self.parent().parent();
        var name = tr.attr('role-name');
        var desc = tr.attr("role-desc");
        var permissions = tr.attr("role.permissions");

        var nameInput = dialog.find("input[name='name']");
        var descInput = dialog.find("input[name='desc']");
        var permissionInputs = dialog.find("input[name='permission']");
        nameInput.val(name);
        descInput.val(desc);
        var reg = /\{\d{1,3}\:/g;

        var arry1 = [];
        var arry2 = permissions.match(reg);
        for ( let i=0;i<arry2.length;i++){
            let reg = /\d{1,3}/;
            arry1.push(arry2[i].match(reg)[0]);
            }

        for(let i=0;i<arry1.length;i++){
            for(let j=0;j<permissionInputs.length;j++){
                if(permissionInputs[j].value == arry1[i]){
                    permissionInputs[j].checked = true;
                }
            }
        }

         $("#edit-btn").click(function (event) {
             var name = $("input[name='name']").val();
             var desc = $("input[name='desc']").val();
             var permission_inputs = $("input[name='permission']:checked");
             var permissions = [];
             $.each(permission_inputs,function (idx,obj) {
                permissions.push($(obj).val());
             });
             zlajax.post({
             url: '/cms/roles/edit',
             data: {
                'id': role_id,
                'name':name,
                'desc':desc,
                'permissions': permissions
                },
            success: function (data) {
                if(data['code']==200){
                    zlalert.alertSuccessToast('恭喜，CMS组修改成功！');
                setTimeout(function () {
                    // 跳转到组管理页面
                    window.location = '/cms/croles/';
                },1200);
                }else{
                    zlalert.alertInfoToast(data['message']);
                }
            },
        });

         })


    })
});


$(function () {
    $('#role-dialog').on('hide.bs.modal', function () {
        var dialog = $("#role-dialog");
        var nameInput = dialog.find("input[name='name']");
        var descInput = dialog.find("input[name='desc']");
        var permissionInputs = dialog.find("input[name='permission']");

        nameInput.val("");
        descInput.val('');
        for(let i=0;i<permissionInputs.length;i++){
            if(permissionInputs[i].checked == true){
                 permissionInputs[i].checked = false;
            }
        }
});
});