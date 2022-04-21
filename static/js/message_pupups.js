document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/js/messagebox.js" type="text/javascript" charset="utf-8"></script>');
document.write('<script src="/static/static/toastr.min.js" type="text/javascript" charset="utf-8"></script>');


function message_pupus() {
    $.ajax({
        type: 'POST',
        url: '/message_center_pupups_ajax/', //路由加'/'否则会报ssh错误
        data: {},
        success: function (data) {
            data = JSON.parse(data);
            let message_conunt = data['message_count']
            let message_list = data['message_list']
            if (message_conunt === 0) {
                return
            }

            // 先发送有几条未读信息
            toastr.error(`有${message_conunt}条未读消息，请及时查看！`);

        },
    })
}
    toastr.options = {
    "closeButton": true, //是否显示关闭按钮
    "debug": false, //是否使用debug模式
    "progressBar": true, //是否显示进度条，当为false时候不显示；当为true时候，显示进度条，当进度条缩短到0时候，消息通知弹窗消失
    "positionClass": "toast-top-center",//显示的动画时间
    "showDuration": "400", //显示的动画时间
    "hideDuration": "1000", //消失的动画时间
    "timeOut": "7000", //展现时间
    "extendedTimeOut": "1000", //加长展示时间
    "showEasing": "swing", //显示时的动画缓冲x方式
    "hideEasing": "linear", //消失时的动画缓冲方式
    "showMethod": "fadeIn", //显示时的动画方式
    "hideMethod": "fadeOut" //消失时的动画方式
};


//调用方式
// toastr.error("连接不能打开！");
// toastr.success("连接已建立，可以进行通信！")
// toastr.success("连接已建立，可以进行通信！", "成功")
// toastr.warning("连接建立失败，请重试！")
// toastr.info("请先登录！")
message_pupus()

// setInterval('10000',message_pupus);
