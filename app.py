from flask import Flask ,escape , request,render_template
import pickle
import numpy as np


app = Flask(__name__)
model = pickle.load(open('modelnew.pkl','rb'))



@app.route("/")
def home():
    return  render_template("index.html")


@app.route('/predict',methods=['GET','POST'])
def predict():
    if request.method== 'POST':
        gender = request.form['gender']
        marriedstatus = request.form['marriedstatus']
        dependents = request.form['dependents']
        education = request.form['education']
        selfemployed = request.form['selfemployed']
        credithistory= request.form['credithistory']
        propertyarea = request.form['propertyarea']
        applicantincome= float(request.form['applicantincome'])
        coapplicantincome = float(request.form['coapplicantincome'])
        loanamount = float(request.form['loanamount'])
        loanamounterm = float(request.form['loanamountterm'])
        #gender
        if(gender =="Male"):
            male=1
        else:
            male=0

        #married
        if(marriedstatus=="Yes"):
            marriedstatus =1
        else:
            marriedstatus =0
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
        elif (dependents == '3+'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0
        if (education == "Not Graduate"):
            not_graduate = 1
        else:
            not_graduate = 0
        if (selfemployed == "Yes"):
            employed_yes = 1
        else:
            employed_yes = 0
        if (credithistory == "Yes"):
            credithistory = 1
        else:
            credithistory = 0
        if (propertyarea == "Semiurban"):
            semiurban =1
            urban = 0
        elif(propertyarea == "Urban"):
            semiurban =0
            urban =1
        else:
            semiurban =0
            urban =0
        applicantincomelog = np.log(applicantincome)
        totalincomelog = np.log(applicantincome+coapplicantincome)
        loanamountlog = np.log(loanamount)
        loanamountermlog = np.log(loanamounterm)
        prediction = model.predict([[credithistory,applicantincomelog,loanamountlog,loanamountermlog,totalincomelog,male,marriedstatus,dependents_1,dependents_2,dependents_3,not_graduate,employed_yes,semiurban,urban]])

        if(prediction=="N"):
            prediction="Not eligible"
        else:
            prediction = "Yes you are eligible"
        return render_template("prediction.html",prediction_text="loan status is {}".format(prediction))



    else:
        return  render_template("prediction.html")


if __name__ == '__main__':
    app.run(debug=True)