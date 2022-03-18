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
                    window.location.href = '/login/'
                } else {
                    alert(data['message'])
                }

            },

        })
    } else {
        alert('填写有误')
    }
})
