const ERR_STATUS = 2
const SUCCESS_STATUS = 1
const NORMAL_STATUS = 0
const BUSY_STATUS = 3

window.onload=function(){
            toggle_sub_bt(0);
            choose_file_change();
            file_bt_click();
}
function choose_file_change(){
    document.getElementById("select_file_input").addEventListener("change",function () {
        console.log("change:", this.value);
        toggle_sub_bt(1);
        msg_show(this.value, NORMAL_STATUS);
    });
}

function file_bt_click(){
    document.getElementById("file_sub_bt").addEventListener("click",function () {
        toggle_sub_bt(0);
        msg_show("上传中...", BUSY_STATUS);
        upload();

    });
}

function toggle_sub_bt(toggle_val){
    if (toggle_val === 0){
        document.getElementById("file_sub_bt").setAttribute('disabled', true);
        document.getElementById("file_sub").style.background="gray";
    }else{
        document.getElementById("file_sub_bt").removeAttribute('disabled');
        document.getElementById("file_sub").style.background="#3276b1";
    }
}

function msg_show(msg, show_type){
    let msg_elem = document.getElementById("msg");
    msg_elem.innerText = msg;
    switch(show_type)
    {
        case ERR_STATUS:
            msg_elem.style.color='red';
            break;
        case SUCCESS_STATUS:
            msg_elem.style.color='green';
            break;
        default:

    }

}

function upload(){

    // let files = document.querySelector('#select_file_input').files
    let files = document.getElementById("select_file_input").files;
    console.log("fii:", files)
    if (files.length <= 0) {
        msg_show('请选择要上传的文件！', ERR_STATUS)
    }

  let formData = new FormData();
    for(let i = 0 ;i<files.length;i++){
        let file = files[i];
        // file_list.push(file);
        formData.append('upload_file', file);

    }

    console.log("formdata:", formData)
  var xhr = new XMLHttpRequest();
  xhr.timeout = 3000;
  xhr.responseType = "text";
  xhr.open('POST', '/', true);
  xhr.onprogress = function(){
    console.log("加载状态READYSTATE"+ xhr.readyState);
  }
  xhr.onload = function(e) {
    if(this.status === 200){
        msg_show(this.responseText, SUCCESS_STATUS);
    }else{
        msg_show(this.responseText||"上传失败", ERR_STATUS);
    }
  };
  xhr.ontimeout = function(e) {
        console.log("连接超时")
        msg_show("连接超时", ERR_STATUS);

  };
  xhr.onerror = function(e) {
      console.log("error");
      msg_show("连接错误："+ e, ERR_STATUS);
  };

  xhr.send(formData);


}