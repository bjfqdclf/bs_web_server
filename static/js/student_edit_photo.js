document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');

$(function () {
    $(".pic").click(function () {
        let can_edit_info = $(this).attr('id')
        if (can_edit_info === "False") {
            Messagebox.show({
                title: '无权限',          //模态窗口的标题
                content: '当前用户没有权限录入人脸，是否申请修改人脸录入？',        //模态窗口的显示内容，支持html文本
                okText: "确定",         //确定按钮标题,如果不配置默认显示确定
                cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
                okEvent: function () {
                    apply_edit_photo()
                },  //确定申请人脸录入
            });
            return;
        }

        $("#upload").click(); //隐藏了input:file样式后，点击头像就可以本地上传
        $("#upload").on("change", function () {
            var objUrl = getObjectURL(this.files[0]); //获取图片的路径，该路径不是图片在本地的路径
            if (objUrl) {
                Messagebox.show({
                title: '系统提示',          //模态窗口的标题
                content: '是否确定上传该图片？',        //模态窗口的显示内容，支持html文本
                okText: "确定",         //确定按钮标题,如果不配置默认显示确定
                cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
                okEvent: function () {
                    $(".pic").attr("src", objUrl); //将图片路径存入src中，显示出图片
                    $(".pic").attr("id", "False");
                    up_img();
                },
            });

            }
        });
    });
});

//建立一?可存取到?file的url
function getObjectURL(file) {
    var url = null;
    if (window.createObjectURL != undefined) { // basic
        url = window.createObjectURL(file);
    } else if (window.URL != undefined) { // mozilla(firefox)
        url = window.URL.createObjectURL(file);
    } else if (window.webkitURL != undefined) { // webkit or chrome
        url = window.webkitURL.createObjectURL(file);
    }
    return url;
}

//上传头像到服务器
function up_img() {
    var pic = $('#upload')[0].files[0];
    var file = new FormData();
    file.append('image', pic);
    $.ajax({
        url: "/upload_img_ajax/",
        type: "post",
        data: file,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data);
            var res = data;
            $("#resimg").append("<img src='/" + res + "'>")
        }
    });
}

function apply_edit_photo() {
    $.ajax({
        url: "/student/initiate_approval_ajax/",
        type: "post",
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                Message.success(data['message'])
            } else {
                Message.error(data['message'])
            }

        }
    });
}

$(".btn-primary").click(function () {
    Messagebox.show({
        title: '发起审批',          //模态窗口的标题
        content: '是否确认申请修改人脸录入？',        //模态窗口的显示内容，支持html文本
        okText: "确定",         //确定按钮标题,如果不配置默认显示确定
        cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
        okEvent: function () {
            apply_edit_photo()
        },  //确定申请人脸录入
    });
})
