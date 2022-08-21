from pathlib import Path
import datetime
from flask import current_app
import os


def float_to_datetime(num):
    return datetime.datetime.fromtimestamp(num).strftime("%Y-%m-%d %H:%M:%S")

def tree(directory):
    print(f'+ {directory}')
    for path in sorted(directory.rglob('*')):
        depth = len(path.relative_to(directory).parts)
        spacer = '    ' * depth
        print(f'{spacer}+ {path.name}')


def list_path(src_path=None):
    
    media_root = current_app.config.get("MEDIA_ROOT")
    media_root = Path(media_root)
    
    if not src_path:
        file_path = media_root
    else:
        file_path = media_root / Path(src_path)
    # tree(file_path)
    
    data = []
    if not file_path.exists:
        return
    for f in file_path.iterdir():
        file_name = f.name
        file_szie = f.stat().st_size
        file_st_atime = f.stat().st_atime
        file_st_ctime = f.stat().st_ctime
        file_st_mtime = f.stat().st_mtime
        if f.is_dir():
            file_type = 'dir'
        else:
            file_type = f.suffix
        
        # print(f"{file_name}-{file_type}-{file_szie}-{float_to_datetime(file_st_atime)}-{float_to_datetime(file_st_ctime)}-{float_to_datetime(file_st_mtime)}")
        print(media_root, f.absolute(), f.parent)
        media_root_str = str(media_root)
        file_absolute_str = str(f.absolute())
        base_path = os.path.commonpath([media_root_str, file_absolute_str])
        rel_path = file_absolute_str[len(base_path):].replace(r"\\", "/")
        file_rel_path = rel_path if file_type != 'dir' else f"?path={rel_path[1:]}"
        data.append({
            "file_name": file_name,
            "file_type": file_type,
            "file_size": file_szie,
            "file_st_mtime": float_to_datetime(file_st_mtime),
            "file_path": file_rel_path
        })

        
        
    if data:
        data = sorted(data, key=lambda x: x['file_name'])
    
    return data
        

