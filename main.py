from flask import *
from datetime import timedelta
import FirebaseAndML as fnm

#initialize
app = Flask(__name__)
app.secret_key = "bananas"

app.permanent_session_lifetime = timedelta(days = 5)


#home-page
@app.route("/")
def home():
	arr = [fnm.CountNumberOfPatients(), fnm.TotalOccupancy()]
	#arr = [10, 20]
	return render_template("index.html", content = arr)

#patient-form
@app.route("/add", methods = ["POST", "GET"])
def add():
	if request.method == "POST":

		#make an array to store the info
		patient_info = {};
		patient_info["name"] = request.form["name"]
		patient_info["age"] = request.form["age"]
		patient_info["gender"] = request.form["gender"]
		patient_info["blood"] = request.form["blood"]
		patient_info["mobile"] = request.form["mobile"]
		patient_info["email"] = request.form["email"]
		patient_info["alcohol"] = request.form["alcohol"]
		patient_info["criminal"] = request.form["criminal"]
		patient_info["critical"] = request.form["critical"]
		patient_info["disease"] = request.form["disease"]
		patient_info["eco_status"] = request.form["eco_status"]
		patient_info["marital_status"] = request.form["marital_status"]
		patient_info["dependents"] = request.form["dependents"]

		#update evrything through firebase
		temp = fnm.EnterIntoPatientDB(patient_info)
		session["patient_info"] = patient_info
		if temp is None:			
			#redirect to the same page  
			flash("Patient added successfully", "success")
			return redirect(url_for("add"))
		else:
			return render_template("ml.html",content = temp)
	else:
		temp = fnm.GetDiseaseList()
		return render_template("add.html", content = temp)


#update patient 
@app.route("/update", methods = ["POST", "GET"])
def update():
	if request.method == "POST":
		name = request.form["name"]
		ids = request.form["patient_id"]
		critical = request.form["critical"]
    
		#function
    
		flash("Patient information updated successfully", "sucess")
		fnm.UpdateRecord(ids, name,critical)
		return redirect(url_for("update"))
	else:
		return render_template("update.html")

#discharge patient
@app.route("/discharge", methods = ["POST", "GET"])
def discharge():
	if request.method == "POST":
		name = request.form["name"]
		ids = request.form["patient_id"]
        #firebase
		fnm.DeletePatientByNumberAndName(ids,name)
        
		flash("Patient removed successfully", "sucess")
		return redirect(url_for("discharge"))
	else:
		return render_template("discharge.html")


#remove rooms
@app.route("/removeroom", methods = ["POST"])
def removeroom():
	name = request.form["name"]
	fnm.RemoveRooms(name)
	return redirect(url_for("room"))

@app.route("/replace", methods = ["POST"])
def replace():
	info = session["patient_info"]
	fnm.ReplacePatient(info)
	fnm.GradientDescent(info ,0)
	return redirect(url_for("home"))


@app.route("/notreplace", methods = ["POST"])
def notreplace():
	info = session["patient_info"]
	fnm.GradientDescent(info ,1)
	return redirect(url_for("home"))

@app.route("/about", methods = ["GET"])
def about():
	return render_template("about.html")


@app.route("/room", methods = ["GET"])
def room():
	temp = fnm.GetRoomsWithPatients()
	return render_template("room.html", content = temp)


@app.route("/addroom", methods = ["POST"])
def addroom():

	name = request.form["name"]
	number_of_beds = request.form["capacity"]
	critical = request.form["critical"]
	fnm.AddRooms(name, number_of_beds, critical)
	return redirect(url_for("room"))


if __name__ == "__main__":
	app.run(port=5001, debug = True)

