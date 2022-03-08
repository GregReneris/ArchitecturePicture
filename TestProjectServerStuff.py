

import io, os , sys
from flask import Flask
from flask import current_app as app
from flask import send_file
from flask import render_template , request , jsonify, make_response

import numpy as np

import cv2


from PIL import Image, ImageOps

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"




def send_image(img):
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    return send_file(buf, mimetype = 'image/jpeg')


@app.route('/rotate90', methods=['POST'])
def nop():

    file = request.files['image'] 
    img = Image.open(file.stream)

    img = img.rotate(90)

    return send_image(img)

@app.route('/grey', methods=['POST'])
def grey():

    file = request.files['image'] 
    img = Image.open(file.stream)

    img = ImageOps.grayscale(img)

    return send_image(img)


@app.route('/resize', methods=['POST'])
def resize():

    file = request.files['image']
    img = Image.open(file.stream)
    x = request.form['x']
    y = request.form['y']
    x = int(x)
    y = int(y)

    img = img.resize((x,y))

    return send_image(img)



@app.route('/rotate270', methods=['POST'])
def rotateleft():
    file = request.files['image'] 
    img = Image.open(file.stream)
    img = img.rotate(270)
    return send_image(img)


#currently only sends 80x80 thumbnails. Need to work
#on dynamic size scaling.
@app.route('/thumbnail', methods=['POST'])
def thumbnail():

    file = request.files['image']
    img = Image.open(file.stream)
    x = 80
    y = 80

    img = img.resize((x,y))

    return send_image(img)


@app.route('/flipVert', methods=['POST'])
def flipVert():

    file = request.files['image']
    img = Image.open(file.stream)
    img = ImageOps.flip(img)

    return send_image(img)

@app.route('/flipHoriz', methods=['POST'])
def flipHoriz():

    file = request.files['image']
    img = Image.open(file.stream)
    img = ImageOps.mirror(img)

    return send_image(img)




# The below methods are test methods used to experiment with different masking
# and HTTP request methods. Post, Get, and sending bytes across.
# There ended up being a smoother way to receive images with requests
# But I found these useful nonetheless.

@app.route("/view")
def hello_view():
    # "returns transformed image"

    obj = im

#    return Flask.send_static_file(io.BytesIO(obj.read()),
#                    attachment_filename='PixPix.jpg',
#                    mimetype = 'image/png')

    return send_file(filepath, mimetype = 'image/jpg')


@app.route('/nop2', methods=['GET'])
def nop2():

    filepath = r"C:\TemporyFolder\test.jpeg"    

    return send_file(filepath, as_attachment=True, attachment_filename="yoda.jpeg", mimetype = 'image/jpeg')
    
    data = open(filepath, 'rb').read()
    data = io.BytesIO(data)
    response = make_response(data)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set('Content-Disposition', 'attachment', filename = 'yodaAAA.jpeg')

    return response

    #return send_file(filepath, as_attachment=True, attachment_filename="yoda.jpeg", mimetype = 'image/jpeg')

@app.route('/transform', methods=['POST'])
def transform():

    file = request.files['image'] #.read()
    img = Image.open(file.stream)
    print("got here")
    print(img)
    print(file)
    img.save("C:\\TemporyFolder\\test.jpeg")
    #has been sent to server and saved.
    
    #do transformations

    parameters = request.form
    print(parameters)

    
    filepath = r"C:\\TemporyFolder\\test.jpeg"
    


    return send_file(filepath, as_attachment=True, download_name="yoda.jpeg", mimetype = 'image/jpeg')


#Extra roll method to turn an image into a roll. Neat!
def roll(image, delta):
    """Roll an image sideways."""
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0:
        return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part1, (xsize - delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize - delta, ysize))

    return image




@app.route('/maskImage' , methods=['POST'])
def mask_image():
    # print(request.files , file=sys.stderr)
    file = request.files['image'].read() ## byte file
    npimg = np.fromstring(file, np.uint8)
    
    
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    
    
    ######### Do preprocessing here ################
    # img[img > 150] = 0
    ## any random stuff do here
    ################################################
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})



if __name__ == '__main__':
    app.run("127.0.0.1", 5000)

