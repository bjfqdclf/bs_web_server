document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');

$(".not-read-info").click(function () {
    let message_unique_code = $(this).attr('id')
    $.ajax({
        type: 'POST',
        url: '/get_message_detail_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'message_unique_code': message_unique_code,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                let message = data['message_info']
                Messagebox.show({
                    title: message['title'],          //模态窗口的标题
                    content: message['message'],        //模态窗口的显示内容，支持html文本
                    okText: "已读",         //确定按钮标题,如果不配置默认显示确定
                    cancelText: "取消",     //取消按钮标题，如果不配置则不显示取消按钮
                    okEvent: function () {
                        Message.info('该条通知已移入已读区')
                        $.ajax({
                            type: 'POST',
                            url: '/message_read_ajax/', //路由加'/'否则会报ssh错误
                            data: {
                                'message_unique_code': message_unique_code,
                            },
                            success: function (data) {
                                data = JSON.parse(data);
                                if (data.status === 'success') {
                                    let tr_box = $(`tbody #${message_unique_code}`)
                                    tr_box.remove()
                                    $("#is-read-tbody").prepend(`<tr>
                        <th> ${message['title']} </th>
                        <th> ${message['gen_time']} </th>
                        <th>
                            <a style="cursor:pointer;" id="${message_unique_code}">详情</a>
                        </th>
                    </tr>`)

                                } else {
                                    Message.error(data['message'])
                                }

                            },

                        })
                    },  //确定按钮单击时的执行的事件，如果不配置默认是关闭窗口
                });

            } else {
                Message.error(data['message'])
            }

        },

    })
})

$("#is-read-tbody").on('click','tr th a' ,function () {
    let message_unique_code = $(this).attr('id')
    $.ajax({
        type: 'POST',
        url: '/get_message_detail_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'message_unique_code': message_unique_code,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                let message = data['message_info']
                Messagebox.show({
                    title: message['title'],          //模态窗口的标题
                    content: message['message'],        //模态窗口的显示内容，支持html文本
                    okText: "返回",         //确定按钮标题,如果不配置默认显示确定
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
