import re
from flask import Flask, request, jsonify, send_file, url_for
from PIL import Image
from image.styler import style_image
import pathlib as pth
import uuid


app = Flask(__name__)

@app.route('/')
def index():
   return 'Hello go on /image/edit and style your images'

@app.route('/image/<file_name>', methods=["GET"])
def image_get(file_name: str):
    file_path = None
    
    files = pth.Path('files').glob('*.*')
    for file in files:
        if file.name == file_name:
            file_path = file
            break
    if file_path:
        return send_file(file_path.absolute(), mimetype='image/jpeg')
    
    else:
        return '404 not found'


@app.route('/image/edit', methods=["GET"])
def image_styler_get():
    return 'image styling'



@app.route('/image/edit', methods=["POST"])
def image_styler_post():
    # reading data
    file = request.files['image1']
    style = request.form['style']
    styling = request

    # image path.
    img_path = pth.Path(f'files/{file.filename}')

    # Read the image via file.stream
    img = Image.open(file.stream)
    img.save(open(str(img_path.absolute()), 'wb'))

    print(style, img_path)
    styled_img_path = img_path.parent.absolute() / (str(uuid.uuid4().hex)+img_path.suffix)
    
    styled_image = style_image(img_path, style)
    styled_image.save(open(str(styled_img_path.absolute()), 'wb'))

    img_url =  request.host_url + url_for('image_get', file_name=styled_img_path.name)

    return jsonify({'styled': {'image': img_url}, 'size': [img.width, img.height]})


if __name__ == '__main__':
   app.run()