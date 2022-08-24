import os
from flask import Blueprint, render_template, request, url_for, make_response, current_app
from file_handle import list_path
from werkzeug.utils import secure_filename

home = Blueprint('views', __name__)


@home.route('', methods=['GET'])
def index():
    search_path = request.args.get("path", None)
    data_content = list_path(search_path)
    data_head = ['文件名', '文件类型', '文件大小', '最后更新日期']
    data = {
        'data_head': data_head,
        'data_content': data_content
    }
    return render_template('index.html', data=data)


@home.route('/upload', methods=['POST'])
def upload():
    # Remember the paramName was set to 'file', we can use that here to grab it
    file = request.files['file']
    media_root_path = current_app.config.get("MEDIA_ROOT")
    
    # secure_filename makes sure the filename isn't unsafe to save
    filename = secure_filename(file.filename)
    save_path = os.path.join(media_root_path, filename)
    
    # We need to append to the file, and write as bytes
    with open(save_path, 'ab') as f:
        # Goto the offset, aka after the chunks we already wrote
        f.seek(int(request.form['dzchunkbyteoffset']))
        f.write(file.stream.read())
    
    # Giving it a 200 means it knows everything is ok
    return make_response(('Uploaded Chunk', 200))
