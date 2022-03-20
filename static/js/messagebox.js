'use strict';

var Messagebox = {};

Messagebox.global = this;

//信息框弹窗
Messagebox.messageBoxDialog = null;
//信息框标题
Messagebox.title = null;
//信息框内容
Messagebox.content = null;
//信息框右上角关闭按钮
Messagebox.closeBtn = null;
//信息框关闭事件
Messagebox.closeEvent = null;
//信息框内容
Messagebox.content = null;
//信息框确定按钮
Messagebox.okBtn = null;
//确定按钮单击事件
Messagebox.okClickEvent = null;
//信息款取消按钮
Messagebox.cancelBtn = null;



/**
 * 创建Dom
 */
Messagebox.createDom = function (tagName, className) {

	var container = document.createElement(tagName);
	container.setAttribute('class', className);
	return  container;

};

/**
 *创建
 */
Messagebox.create = function () {
    Messagebox.messageBoxDialog = Messagebox.createDom('div', 'message-box-dialog');

    let messageBox = Messagebox.createDom('div', 'message-box');

    Messagebox.title = Messagebox.createDom('div', 'message-box-title');
    Messagebox.content = Messagebox.createDom('div', 'message-box-content');
    Messagebox.closeBtn = Messagebox.createDom('div', 'message-box-close-btn');
    Messagebox.closeBtn.innerHTML = '×';

    Messagebox.okBtn = Messagebox.createDom('div', 'message-box-btn btn-ok');

    Messagebox.cancelBtn = Messagebox.createDom('div', 'message-box-btn btn-cancel');

    /*给关闭按钮绑定事件*/
    Messagebox.bindEvent(Messagebox.closeBtn, 'click', function (){
        Messagebox.close();
    });

    /*给关闭按钮绑定事件*/
    Messagebox.bindEvent(Messagebox.cancelBtn, 'click', function (){
        Messagebox.close();
    });

    messageBox.appendChild(Messagebox.closeBtn);
    messageBox.appendChild(Messagebox.title);
    messageBox.appendChild(Messagebox.content);
    messageBox.appendChild(Messagebox.okBtn);
    messageBox.appendChild(Messagebox.cancelBtn);
    Messagebox.messageBoxDialog.appendChild(messageBox);

    document.body.appendChild(Messagebox.messageBoxDialog);
};




/**
 * 绑定事件
 */
Messagebox.bindEvent = function (container, type, event) {

    if (typeof event != 'function') {
        return;
    }
    container.addEventListener(type, event, false);
}

/**
 * 移除事件
 */
Messagebox.removeEvent = function (container, type, event) {

    if(container == null){
        return ;
    }
    if (typeof event === "function") {
        container.removeEventListener(type, event, false);
    }
}


/**
 * 关闭窗口
 */
Messagebox.close = function () {
    Messagebox.messageBoxDialog.style.display = "none";
}

/**
 * 显示窗口
 */
Messagebox.show = function (opt) {

    if(opt == null){
        return ;
    }

    //设置标题
    if (opt.title === undefined) {
        opt.title = '提示';
    }
    Messagebox.title.innerHTML = opt.title;

    //设置内容
    if (opt.content === undefined) {
        opt.content = ''
    }
    Messagebox.content.innerHTML = opt.content;

    //设置确定按钮标题
    if (opt.okText === undefined) {
        opt.okText = '确定';
    }
    Messagebox.okBtn.innerHTML = opt.okText;

    //确定按钮事件处理
    Messagebox.removeEvent(Messagebox.okBtn, 'click', Messagebox.okClickEvent);//一定要移除,否则会累积绑定
    //配置了确定按钮点击方法
    if (typeof opt.okEvent === 'function') {
        //绑定了事件
        function hasOkEvent(){
            Messagebox.close();
			opt.okEvent();
        };

        Messagebox.okClickEvent = hasOkEvent;

        Messagebox.bindEvent(Messagebox.okBtn, 'click', Messagebox.okClickEvent);
    }else{

        function hasNotOkEvent(){
            Messagebox.close();
        };
        Messagebox.okClickEvent = hasNotOkEvent;
        Messagebox.bindEvent(Messagebox.okBtn, 'click', Messagebox.okClickEvent);
    }

	//设置取消按钮标题
    if (opt.cancelText === undefined) {
        //没有配置就隐藏按钮
        Messagebox.cancelBtn.style.display = "none";
    } else {
        Messagebox.cancelBtn.innerHTML = opt.cancelText;
        Messagebox.cancelBtn.style.display = "";
    }

	//显示
    Messagebox.messageBoxDialog.style.display = 'block';
}

Messagebox.create();
