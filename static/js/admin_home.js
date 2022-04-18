document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');


$("#submit-btn").click(function (e) {
    e.preventDefault()
    let addr = $(".addr").val()
    if (addr.length > 32) {
        Message.error('地址描述过长！')
        return;
    } else if (addr.length === 0) {
        Message.error('地址描述不能为空！')
        return;
    }
    $.ajax({
        type: 'POST',
        url: '/admin/add_device_ajax/', //路由加'/'否则会报ssh错误
        data: {
            'address_desc': addr,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                let device_info = data['device_info']
                Message.info(data['message'])
                $("#device-list").append(`<tr>
                        <th>${device_info['id']}</th>
                        <th>${device_info['code']}</th>
                        <th>${device_info['addr']}</th>
                        <th>${device_info['is_used']}</th></tr>`)
            } else {
                Message.error(data['message'])
            }

        },

    })

})

