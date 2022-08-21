import os
from flask import Blueprint, render_template, request, url_for, make_response, current_app
from file_handle import list_path
from werkzeug.utils import secure_filename

home = Blueprint('views', __name__)


@home.route('', methods=['GET', 'POST'])
def index():
    media_root_path = current_app.config.get("MEDIA_ROOT")
    if request.method == 'POST':
        try:
            files = request.files.getlist('upload_file')
        except Exception as e:
            resp = make_response(f"接收错误:{e}", 400)
            return resp
        if not files:
            resp = make_response("没有提交任何文件", 400)
            return resp
        for file in files:
            if not file.filename:
                continue
            filename = secure_filename(file.filename)
            file.save(os.path.join(media_root_path, filename))
        return "上传成功"
    else:
        search_path = request.args.get("path", None)
        data_content = list_path(search_path)
        data_head = ['文件名', '文件类型', '文件大小', '最后更新日期']
        data = {
            'data_head': data_head,
            'data_content': data_content
        }
        return render_template('index.html', data=data)
