from flask import Flask, render_template, request, jsonify, Response
import io
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly
import plotly.express as px
import pandas as pd
import numpy as np
import datetime
import operator
from flask.helpers import url_for
import openpyxl

app = Flask(__name__)

# def saveFile(uploaded_file):
#     UPLOAD_FOLDER = 'static'
#     app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#     uploaded_file.save(file_path)

def duration(start_value, end_value):

    Start = datetime.datetime.fromisoformat(start_value)
    End = datetime.datetime.fromisoformat(end_value)

    start_value = Start            
    end_value = End

    duration = End - Start
    seconds = int(duration. total_seconds())

    return seconds, Start, End

def generateDictArray(csvFile):
    data = []

    global df
    
    with open(f'static/{csvFile}.csv', 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                # print(row)
                para = duration(row['START'], row['END'])
                
                row['DURATION'] = para[0] 
                row['START'] = para[1] 
                row['END'] = para[2]
                data.append(row)

                # duration = row['start_time'] - row['end_time']
                # data.append(row)
    df = pd.read_csv(f'static/{csvFile}.csv')
    return data

def filterData(data, min='', max='', recordDate='', mobileNo='', Type=''):

    filteredData = []

    if min=='':
        min = 0
    else:
        min = int(min)

    if max=='':
        max=1000000  #change with INT MAX
    else:
        max = int(max)

    if recordDate == '':
        recordDate=datetime.date.today()
        # print(recordDate, type(recordDate))
    else:
        recordDate = datetime.datetime.strptime(recordDate, '%Y-%m-%d').date()
        # print(recordDate, type(recordDate))
    
    if Type == 'ALL':
    
        for dict in data:
           
            if dict['DURATION']>=min and dict['DURATION']<=max and dict['START'].date() < recordDate :
                if mobileNo == '': 
                    filteredData.append(dict)
                elif dict['PHONE'] == mobileNo: 
                    filteredData.append(dict)
    else:
        for dict in data:
        
            if dict['DURATION']>=min and dict['DURATION']<=max and dict['START'].date() < recordDate and dict['TYPE'] == Type:
                if mobileNo == '': 
                    filteredData.append(dict)
                elif dict['PHONE'] == mobileNo: 
                    filteredData.append(dict)


    # print(filteredData, len(filteredData))

    if len(filteredData)==0:
        return 'No Records Found'
    else:
        return filteredData

@app.route('/duration.png')
def plot_duration():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    duration=[]
    for i in range(100):
        start=datetime.datetime.strptime(df['START'][i],'%Y-%m-%d %H:%M:%S')
        end=datetime.datetime.strptime(df['END'][i],'%Y-%m-%d %H:%M:%S')
        duration.append((end-start).total_seconds())
        callee_duration={}
    for i in range(100):
        if(str(df['PHONE'][i]) in callee_duration):
            callee_duration[str(df['PHONE'][i])]+=duration[i]
        else:
            callee_duration[str(df['PHONE'][i])]=duration[i]
    callee_duration= dict( sorted(callee_duration.items(), key=operator.itemgetter(1),reverse=True))

    axis.bar(callee_duration.keys(),callee_duration.values())
    axis.set_xticks(callee_duration.keys())
    
    axis.set_xticklabels(callee_duration.keys(),rotation=40)    
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/frequency.png')
def plot_frequency():
    
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    numbers=df['PHONE'].astype('str').value_counts().head(10).index
    freq=df['PHONE'].value_counts().head(10)
    axis.bar(numbers,freq)
    axis.set_xticks(numbers)
    axis.set_xticklabels(numbers,rotation=40)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/type.png')
def plot_type():
 
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.bar(df['TYPE'].value_counts().index,df['TYPE'].value_counts())
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/imei.png')
def plot_imei():
    
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    imei=[]
    for i in df['IMEI1']:
        imei.append(i)
    uniq,count=np.unique(imei,return_counts=True)
    unique=[]
    for i in uniq:
        unique.append(str(i))
    axis.bar(unique,count)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/',methods=["POST", "GET"])
def home():
    if request.method == "POST":
        
        data=[]
        formData= request.form
        # print(formData)
        # print(type(request.files['file']))

        csvFile = request.form['selected']
        Type = request.form['TYPE']
        min = request.form['min']
        max = request.form['max']
        recordDate = request.form['date']
        mobileNo = request.form['number']
        f = request.files['file']

        name = f.filename
        # print(type(f))

        # print(min, max, recordDate, type(recordDate), mobileNo, type(mobileNo))

        if name == '':
            data = generateDictArray(csvFile)
            
            # print(data)

                # uploaded_file = request.files['file']
                # saveFile(uploaded_file)
                # csvFile = request.form['file']
                # print(csv_input)
                # for row in csv_input:
                #     print(row)
            # else:
            #     print(jsonify({"result": request.get_array(field_name='file')}))

        elif 'csv' in name:
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_file = csv.DictReader(stream)
            for row in csv_file:
                
                para = duration(row['START'], row['END'])
                row['DURATION'] = para[0]
                
                row['START'] = para[1] 
                row['END'] = para[2]

                data.append(row)
            
            # print(data)

            field_names = data[0].keys()
            print(field_names)
            print(field_names)
            with open('static/temp.csv', 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = field_names)
                writer.writeheader()
                writer.writerows(data)

            global df 
            df = pd.read_csv('static/temp.csv')

        elif 'xlsx' in name:
            data_xls = pd.read_excel(f, engine='openpyxl')
            file = data_xls.to_csv ('static/target.csv', index = None, header=True)
            csvFile = 'target'
            data = generateDictArray(csvFile)


        if min == '' and max == '' and recordDate == '' and mobileNo == '' and Type == '':
            filteredData = data
        else:
            filteredData = filterData(data, min, max, recordDate, mobileNo, Type)

        display = 'display: block'
       
        array = df.T.values.tolist()
        # print(array)
        # stream = io.TextIOWrapper(f.stream._file, "UTF8", newline=None)
        # csv_input = csv.reader(stream)
        
        # data = sample,
        return render_template("index.html",  display = display, filteredData=filteredData, array = array )
    else:
        display = 'display: none'
        return render_template("index.html", display = display, array = [[]])

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/how-to-use')
def howToUse():
    return render_template("howToUse.html")

@app.route('/project-details')
def projectDetails():
    return render_template("projectDetails.html")

@app.route('/samples')
def samples():

    sample1 = generateDictArray('Sample1')
    sample2 = generateDictArray('Sample2')
    sample3 = generateDictArray('Sample3')
    return render_template("sample.html",Sample1 = sample1, Sample2 = sample2, Sample3 = sample3 )

# @app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
# def download(filename):
#     uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
#     return send_from_directory(directory=uploads, filename=filename)


if __name__ == "__main__":
    app.run(debug=True)
