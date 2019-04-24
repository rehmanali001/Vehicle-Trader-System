from flask import Flask, abort, jsonify, request, render_template
from sklearn.externals import joblib
import numpy as np
import json

TrainedModel = joblib.load('model.pkl')

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/routes")
def routes():
    sample_list = []
    Routes_dict = {}
    Routes_dict['Makes'] = "/makes"
    Routes_dict['Years'] = "/years"
    sample_list.append(Routes_dict)
    return jsonify(sample_list)


def Get_Prediction_Matrix(data):
    # initialize the target vector with zero values
    Prediction_Matrix = np.zeros(53)
    # set the numerical input as they are
    Prediction_Matrix[0] = data['Year']
    Prediction_Matrix[1] = data['Mileage']
    ##################### Mark #########################
   
    Trained_Model_Columns = ['Year', 'Mileage', 'Make_AM', 'Make_Acura', 'Make_Aston', 'Make_Audi',
       'Make_BMW', 'Make_Bentley', 'Make_Buick', 'Make_Cadillac',
       'Make_Chevrolet', 'Make_Chrysler', 'Make_Dodge', 'Make_FIAT',
       'Make_Ford', 'Make_GMC', 'Make_Genesis', 'Make_HUMMER', 'Make_Honda',
       'Make_Hyundai', 'Make_INFINITI', 'Make_Isuzu', 'Make_Jaguar',
       'Make_Jeep', 'Make_Kia', 'Make_Lamborghini', 'Make_Land', 'Make_Lexus',
       'Make_Lincoln', 'Make_Lotus', 'Make_MINI', 'Make_Maserati',
       'Make_Maybach', 'Make_Mazda', 'Make_Mercedes-Benz', 'Make_Mercury',
       'Make_Mitsubishi', 'Make_Nissan', 'Make_Oldsmobile', 'Make_Plymouth',
       'Make_Pontiac', 'Make_Porsche', 'Make_Ram', 'Make_Saab', 'Make_Saturn',
       'Make_Scion', 'Make_Subaru', 'Make_Suzuki', 'Make_Tesla', 'Make_Toyota',
       'Make_Volkswagen', 'Make_Volvo', 'Make_smart']

    # redefine the the user inout to match the column name
    User_Selected_Model = 'Make_'+data['Make']

    # Make sure that the index exists in the columns of the trained model to prevent 'ValueError' 
    if User_Selected_Model in Trained_Model_Columns :
        # search for the index in columns name list 
        Make_Column_Index = Trained_Model_Columns.index(User_Selected_Model)
        # fullfill the found index with 1
        Prediction_Matrix[Make_Column_Index] = 1
        return Prediction_Matrix
    else:
        return None

@app.route('/api',methods=['POST'])
def Make_Prediction():
    result=request.form
    year = result['year_model']
    mileage = result['mileage']
    make = result['mark']
    
    User_Inputs = {'Year':year, 'Mileage':mileage,  'Make':make}
    
    matrix = Get_Prediction_Matrix(User_Inputs)
    if (matrix is not None):
        #Make prediction from the model. 
        Price = TrainedModel.predict([matrix])[0]
        Price = round(Price, 2)
        return json.dumps({'Price':Price})
    else:
        return json.dumps({'Price':-1})

@app.route('/makes')
def Supported_Makes():
    MakeList =[]
    MakeDictionary={}
    MakeDictionary['Makes'] = Get_Makes() 
    MakeList.append(MakeDictionary)
    return jsonify(MakeList)  

def Get_Makes():
    # Need to fetched from mongo. But hardcoded at the moment!
    makes = ['Acura', 'AM', 'Aston', 'Audi', 'Bentley', 'BMW', 'Buick',
       'Chevrolet', 'Chrysler', 'Dodge', 'FIAT', 'Ford', 'Genesis', 'GMC', 'Honda',
       'HUMMER', 'Hyundai', 'INFINITI', 'Isuzu', 'Jaguar', 'Jeep', 'Kia',
       'Lamborghini', 'Land', 'Lexus', 'Lincoln', 'Lotus', 'Maserati',
       'Maybach', 'Mazda', 'Mercedes-Benz', 'Mercury', 'MINI',
       'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac',
       'Porsche', 'Ram', 'Saab', 'Saturn', 'Scion', 'smart', 'Subaru', 'Suzuki', 
       'Tesla', 'Toyota', 'Volkswagen', 'Volvo']
    return makes


@app.route('/years')
def Supported_Years():
    YearsList =[]
    YearsDictionary={}
    
    # Need to be fetched from mongo. But hardcoded at the momement.  
    years = [ '1997','1998' , '1999' , '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007','2008', '2009', '2010', '2011', '2012', '2013','2014', '2015', '2016', '2017', '2018']

    YearsDictionary['Years'] = years 
    YearsList.append(YearsDictionary)
    # print(YearsList)
    return jsonify(YearsList)  

  
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(port=8080, debug=True)