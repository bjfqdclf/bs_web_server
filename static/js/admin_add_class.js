document.write('<script src="/static/js/message.js" type="text/javascript" charset="utf-8"></script>');

$('#add-btn').click(function (e) {
    e.preventDefault();
    var last_div = $(".class-form .item").eq(-1)
    var id_next = last_div.attr('id')
    if (id_next === "10") {
        Message.error("添加行数以达到上限！")
    } else {
        var add_item = `<div class="item" id="${++id_next}">
                <i class="fas fa-greater-than" style="font-size:24px"></i>
                <input type="text" id="class-name" placeholder="班级名称">
            </div>`
        $(".class-form .item").eq(-1).after(add_item)
    }
})


$("#lower-btn").click(function (e) {
    e.preventDefault();
    var last_div = $(".class-form .item").eq(-1)
    if (last_div.attr('id') === "1") {
        Message.error("不可再删除！")
    } else {
        last_div.remove()
    }

})

$("#submit-btn").click(function (e) {
    e.preventDefault();
    var datalist = [];
    var all_div = $(".class-form .item")
    all_div.each(function (index, one_div) {
        datalist.push({
            "id": index,
            "name": $(this).find('input').val()
        })
    })
    $.ajax({
        type: 'POST',
        url: '/admin/add_class_ajax/', //路由加'/'否则会报ssh错误
        data: JSON.stringify(datalist),
        // dataType: 'JSON',
        success: function (data) {
            data = JSON.parse(data);
            if (data.status === 'success') {
                Message.success("创建班级成功！")
                setTimeout('window.location.href = \'/admin/class_manage/\'',1000)

            }
        },
    })
})
