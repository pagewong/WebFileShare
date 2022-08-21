from flask import Flask, send_from_directory,current_app
from views import home
import os
from config_handle import read_cfg


def create_app(*args, **kwargs):
    print(args,kwargs)
    app = Flask(__name__)
    print("defaultcfg:",app.config)

    cfg = read_cfg()
    app.config.update(cfg)

    default_media_root = home.root_path + '/media/'
    MEDIA_ROOT = os.environ.get("MEDIA_ROOT")
    app.config['MEDIA_ROOT'] = MEDIA_ROOT if MEDIA_ROOT else app.config['MEDIA_ROOT'] or default_media_root

    print("cfg:",app.config)


    @app.route('/media/<path:filename>')
    def media(filename):
        media_root = current_app.config.get("MEDIA_ROOT")
        return send_from_directory(media_root, filename)


    app.register_blueprint(home, url_prefix="/")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=app.config.get('PORT'), host=app.config.get('HOST'))