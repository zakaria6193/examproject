from flask import Flask,render_template,request
import numpy as np
import cv2
import math
import os
import base64
import mysql.connector



app = Flask(__name__)
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames


    with open(filename, 'wb') as file:
        file.write(data)

@app.route('/')
def hello_world():
    files = os.listdir('examss/')
    lst=[]
    for file in files:
        lst.append(file.split('.')[0])

    #db = mysql.connector.connect(host="127.0.0.1", user="root", password='', db="exams")
    #c = db.cursor()

    #c.execute("SELECT ID_SCAN,matname FROM scan")

    #rows=c.fetchall()
    #dic=dict()
    #dic['idscan']=[]
    #dic['mat']=[]
    #for row in rows:
        #dic['idscan'].append(str(row[0]))
        #dic['mat'].append(row[1])
    #longueur=len(dic['mat'])




    return render_template('test.html',images=lst)



@app.route('/<path>/splice', methods=['GET', 'POST'])
def splice(path):
    img = cv2.imread("examss/"+path+".jpg")

    # horizontal
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 120)
    lines = cv2.HoughLinesP(edges, 1, math.pi / 2, 2, None, 30, 1);
    imgh = img
    for line in lines[0]:
        pt1 = (line[0], line[1])
        pt2 = (line[2], line[3])
        cv2.line(imgh, pt1, pt2, (0, 0, 255), 3)
    crop_img = imgh[0:line[0], 0:imgh.shape[1]]
    # extract head region
    cv2.imwrite('segments/head.jpg', crop_img)

    # vertical
    img = cv2.imread("examss/"+path+".jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 120)
    lines1 = cv2.HoughLinesP(edges, 1, math.pi, 2, None, 30, 1);
    imgv = img
    for line1 in lines1[0]:
        pt1 = (line1[0], line1[1])
        pt2 = (line1[2], line1[3])
        cv2.line(imgv, pt1, pt2, (0, 0, 255), 3)

    crop_right = imgv[line1[3]:line1[1], line1[0]:imgv.shape[1]]
    cv2.imwrite('segments/right.jpg', crop_right)

    crop_left = imgv[line1[3]:line1[1], 0:line1[0]]
    cv2.imwrite('segments/left.jpg', crop_left)

    vis = np.concatenate((crop_left, crop_right), axis=1)
    cv2.imwrite('splice/spliced.jpg', vis)
    empPicture = convertToBinaryData('segments/right.jpg')

    image = base64.b64encode(empPicture).decode("utf-8")
    return render_template('test2.html',value=image)

@app.route('/finalsplice', methods=['GET', 'POST'])
def finalsplice():
    if request.method == 'GET':
        path = request.args.get('path')






        #if len(path) % 4 != 0:
            #while len(path) % 4 != 0:
                #path = path + "="
            #print('this is len'+str(len(path)))
            #pathnew = base64.b64decode(path,' /')

        # else:
        #     print('this is len' + str(len(path)))
        #     pathnew = base64.b64decode(path,' /')
        # print('this is len '+str(len(path)))
        #arr = bytes(path, 'utf-8')
        #pathnew = base64.decodebytes(arr)



        #write_file(pathnew,'splice/testsplice.png')

        print(len(path))
        print(path)

        return "hello"



if __name__ == '__main__':
    app.run()
