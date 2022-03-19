document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');


$('#re-password-btn').click(function (e) {
    e.preventDefault()
    let old_password = $('#old_password').val();
    let new_password = $('#new_password').val();
    let re_password = $('#re_password').val();
    if (re_password !== "" && new_password !== "" && old_password !== "") {
        //预先发送csrf值，防止出现403错误
        $.ajaxSetup({data: {csrfmiddlewaretoken: '{{ csrf_token }}'}});
        $.ajax({
            type: 'POST',
            url: '/edit_passwd_ajax/', //路由加'/'否则会报ssh错误
            data: {
                'old_password': old_password,
                'new_password': new_password,
                're_password': re_password,
            },
            // dataType: 'JSON',
            success: function (data) {
                data = JSON.parse(data);
                if (data.status == 'success') {
                    // alert('111')
                    Message.info('修改密码成功，请重新登录')
                    setTimeout('window.location.href = \'/login/\'',1000)

                } else {
                    // alert(data['message'])
                    Message.error(data['message'])

                }

            },

        })
    } else {
        // alert('填写有误')
        Message.error('填写有误')
    }
})
