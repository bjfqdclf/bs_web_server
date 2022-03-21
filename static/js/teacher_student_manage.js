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
        Message.error('学生名字为必填！')
        return;
    }
    if (phone_num !== "" && phone_num.length !== 11) {
        Message.error('请填写正确手机号！')
        return;
    }
    if (select.length === 0) {
        Message.error('学生未分配班级！')
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/teacher/add_student_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'name': name,
            'phone_num': phone_num,
            'select': select,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                Message.info('添加学生成功!')
                setTimeout('window.location.href = "/teacher/student_manage/"', 1000)
            } else {
                Message.error(data['message'])
            }

        },

    })

})

$("#submit-switch-btn").click(function (e) {
    e.preventDefault()
    let student_select = $("#left-bar-select-student")
    let class_select = $("#left-bar-select-class")
    let student_select_text = student_select.find("option:selected").text();
    let class_select_text = class_select.find("option:selected").text();
    let student_select_val = student_select.val()
    let class_select_val = class_select.val()
    Messagebox.show({
        title: "是否要更改学生所在班级",          //模态窗口的标题
        content: `${student_select_text}: 分配到[${class_select_text}]`,        //模态窗口的显示内容，支持html文本
        okText: "确定",         //确定按钮标题,如果不配置默认显示确定
        cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
        okEvent: function () {
            $.ajax({
                type: 'POST',
                url: '/teacher/switch_student_class_ajax/', //路由加'/'否则会报ssh错误
                data: {
                    'student_unique_code': student_select_val,
                    'class_unique_code': class_select_val,
                },
                success: function (data) {
                    data = JSON.parse(data);
                    if (data.status === 'success') {
                        Message.info('学生分配成功!')
                        setTimeout('window.location.href = "/teacher/student_manage/"', 1000)
                    } else {
                        Message.error(data['message'])
                    }

                },

            })
        },  //确定按钮单击时的执行的事件，如果不配置默认是关闭窗口
    });

})
