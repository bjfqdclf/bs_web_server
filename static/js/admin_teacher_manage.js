document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');

function limitWords(txt, len) {
    var str = txt;
    if (txt.length <= len) {
        return str;
    }
    str = str.substr(0, len) + '...';
    return str;
}


$("#submit-btn").click(function (e) {
    e.preventDefault()
    let name = $("#name").val()
    let phone_num = $("#phone-num").val()
    let select = $("#select-class").val()
    if (name === "") {
        Message.error('教师名称为必填！')
        return;
    }
    if (phone_num !== "" && phone_num.length !== 11){
        Message.error('请填写正确手机号！')
        return;
    }
    // if (select.length === 0) {
    //     Message.warn('教师未分配班级！')
    // }
    $.ajax({
        type: 'POST',
        url: '/admin/add_teacher_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'name': name,
            'phone_num': phone_num,
            'select': JSON.stringify(select),
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                Message.info('添加教师成功')
                setTimeout('window.location.href = "/admin/teacher_manage/"', 1000)

            } else {
                Message.error(data['message'])
            }

        },

    })

})

$(".teacher-class-info").click(function () {
    let teacher_unique_code = $(this).attr('id')
    let teacher_id = $(this).attr('name')
    $.ajax({
        type: 'POST',
        url: '/admin/get_teacher_class_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'teacher_unique_code': teacher_unique_code,
            'teacher_id': teacher_id,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {

                let class_list = data['class_list']
                if (class_list.length === 0) {
                    var content_text = "未配置管理班级"
                } else {
                    var content_text = ""
                    for (var i = 0, len = class_list.length; i < len; i++) {
                        content_text = content_text + "[" + class_list[i] + "]";
                    }
                }

                Messagebox.show({
                    title: `班级表（${limitWords(data['username'], 5)}）`,          //模态窗口的标题
                    content: content_text,        //模态窗口的显示内容，支持html文本
                    okText: "确定",         //确定按钮标题,如果不配置默认显示确定
                    // cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
                    okEvent: function () {
                    },  //确定按钮单击时的执行的事件，如果不配置默认是关闭窗口
                });

            } else {
                Message.error(data['message'])
            }

        },

    })
})
