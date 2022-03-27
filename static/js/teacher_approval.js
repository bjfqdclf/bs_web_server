document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');

$(".select-approval").click(function () {
    let unique_code = $(this).attr('id')
    $.ajax({
        url: "/teacher/get_approval_ajax/",
        type: "post",
        data: {'unique_code': unique_code},
        success: function (data) {
            data = JSON.parse(data);
            let approval_title = data['approval_info']['title']
            let approval_message = data['approval_info']['message']
            let user_info = data['approval_info']['user_info']
            let class_name = data['approval_info']['class_name']
            let approval_unique_code = data['approval_info']['unique_code']
            if (data.status === 'success') {
                let img_path = data['img_path']
                $(".right-bar").empty() // 移除原有的内容
                if (data['approval_type'] === 1) {
                    var left_bar_html = `<div class="left-bar-info">
                <h5>${approval_title}</h5>
                <h6>姓名：${user_info}</h6>
                <h6>班级：${class_name}</h6>
                <img style="width:200px;height:200px;border: black solid 1px;border-radius:50%;" src="${img_path}">
                <p>审批内容：${approval_message}</p>
                <input class="btn btn-primary approval-pass" type="submit" value="审核通过" id=${approval_unique_code}>
            </div>`

                } else if (data['approval_type'] === 2) {  // 发起请求上传照片权限
                    var left_bar_html = `<div class="left-bar-info">
                <h5>${approval_title}</h5>
                <h6>姓名：${user_info}</h6>
                <h6>班级：${class_name}</h6>
                <p>审批内容：${approval_message}</p>
                <input class="btn btn-primary approval-pass" type="submit" value="审核通过" id=${approval_unique_code}>
            </div>`
                }
                $(".right-bar").append(left_bar_html)
            }

        }
    });

})


$(".right-bar").on('click', '.approval-pass', function () {
    let unique_code = $(this).attr('id')
    Messagebox.show({
        title: "审批",          //模态窗口的标题
        content: "是否通过该审批？",        //模态窗口的显示内容，支持html文本
        okText: "确定",         //确定按钮标题,如果不配置默认显示确定
        cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
        okEvent: function () {
            $.ajax({
                url: "/teacher/approval_pass_ajax/",
                type: "post",
                data: {'unique_code': unique_code},
                success: function (data) {
                    data = JSON.parse(data);
                    if (data.status === 'success') {
                        Message.success(data['message'])
                    } else {
                        Message.error(data['message'])
                    }
                    $(`tbody #${unique_code}`).remove()
                }
            });
        },  //确定按钮单击时的执行的事件，如果不配置默认是关闭窗口
    });
})
