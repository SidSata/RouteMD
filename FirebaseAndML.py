import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pickle
import math

############## DATABASE PART ##################
#This function connects us to the firebase SDK. Don't bother reading it.
def StartDB():
	if not firebase_admin._apps:
		cred = credentials.Certificate("firebase_sdk.json")	
		firebase_admin.initialize_app(cred,{
			"databaseURL": "https://cal-hacknow-2020.firebaseio.com/",
		})

#To enter new values into the database. Accepts a dictionary, which is the patient record.
"""
example usage:
>>>EnterIntoDB({"Age": 17, "Alcoholism-Drug History": "False"...})
"""
def EnterIntoPatientDB(Entered_Dict):
	StartDB()
	#Entering patient Database:
	ref = db.reference('/Patients')
	#Setting keys:
	if(ref.get() == None):
		next_key = "patient1"
	else:
		current_keys = ref.get().keys()
		current_max_id = max([int(this_id[7:]) for this_id in current_keys])
		next_id = current_max_id + 1
		next_key = "patient" + str(next_id)
	#Appending mortality rate, as obtained from the Diseases DB:
	ref2 = db.reference("Diseases")
	Entered_Dict["mortality rate"] = ref2.get()[Entered_Dict["disease"]]
	#Room allocation (if available): 
	chosen_room = None
	if(Entered_Dict['critical'] == 'True'):
		ref3 = db.reference("/Rooms/Critical")
		for keys,values in ref3.get().items():
			if(values['Beds']>values['Occupied']):
				chosen_room = keys
	else:
		ref3 = db.reference("/Rooms/NonCritical")
		for keys,values in ref3.get().items():
			if(values['Beds']>values['Occupied']):
				chosen_room = keys
	Entered_Dict['eco_status'] = int(Entered_Dict['eco_status'])
	#Setting economic status
	if Entered_Dict['eco_status'] < 10000:
		Entered_Dict['eco_status'] = 1
	elif Entered_Dict['eco_status'] < 35000:
		Entered_Dict['eco_status'] = 2
	elif Entered_Dict['eco_status'] < 70000:
		Entered_Dict['eco_status'] = 3
	elif Entered_Dict['eco_status'] < 200000:
		Entered_Dict['eco_status'] = 4
	else:
		Entered_Dict['eco_status'] = 5
	#Invoking ML if room not available:
	if chosen_room == None:
		[potential_critical,potential_noncritical] = GetTopPatient()
		if Entered_Dict['critical'] == 'True':
			return potential_critical
		else:
			return potential_noncritical
	else:
		Entered_Dict['room'] = chosen_room
		IncreaseOccupancy(chosen_room)
		#Entering values into the database
		ref = db.reference("/Patients/"+next_key) 
		ref.set(Entered_Dict)
#Count the total occupancy of the entire hospital
def TotalOccupancy():
	StartDB()
	total_occ = 0
	ref1 = db.reference("/Rooms/Critical")
	ref2 = db.reference("/Rooms/NonCritical")
	for room in ref1.get().values():
		total_occ += int(room["Beds"])
	for room in ref2.get().values():
		total_occ += int(room["Beds"])	
	return total_occ
#For modularity
def IncreaseOccupancy(chosen_room):
	StartDB()
	ref = db.reference("/Rooms/Critical")
	for keys,values in ref.get().items():
		if keys == chosen_room:
			values["Occupied"] += 1
			ref2 = db.reference("/Rooms/Critical/"+keys)
			ref2.set({"Beds": values["Beds"],"Occupied": values["Occupied"]})
	ref3 = db.reference("/Rooms/NonCritical")
	for keys,values in ref3.get().items():
		if keys == chosen_room:
			values["Occupied"] += 1
			ref4 = db.reference("/Rooms/NonCritical/"+keys)
			ref4.set({"Beds": values["Beds"],"Occupied": values["Occupied"]})

#For ML.
def GetPatientRecordByID(id):
	StartDB()
	ref = db.reference("Patients")
	return ref.get()[id]

#To retrieve a record by its number (eg: patient1 can be retrieved by 1)
"""
example usage:
>>> GetPatientRecordByNumber(1)
{#patient1_record}
"""
def GetPatientRecordByNumber(number):
	StartDB()
	ref = db.reference("Patients")
	return ref.get()["patient" + str(number)]

#To delete a record by its number (eg: patient1 can be deleted by 1)
#Returns -1 if the ID and name don't match
def DeletePatientByNumberAndName(number,name):
	StartDB()
	ref = db.reference("/Patients/patient" + str(number))
	if((ref.get()["name"]).upper() == name.upper()):
		ref.delete()
	else:
		return -1

#To get a list that contains the names of all available rooms
def RetrieveAllRooms():
	StartDB()
	roomlist = []
	ref = db.reference("Rooms/Critical")
	ref2 = db.reference("Roomes/NonCritical")
	for room in ref.get():
		roomlist.append(room)
	for room in ref2.get():
		roomlist.append(room)
	return roomlist

#To return all data stored in patient DB in the form of a list of dictionaries. 
"""
example usage:
>>>RetrieveAllRecords()
[{#patient1_record},{#patient2_record}]
"""
def RetrieveAllPatientRecordValues():
	StartDB()
	ref = db.reference("Patients")
	return (ref.get().values())

#For ML.
def RetrieveAllPatientRecords():
	StartDB()
	ref = db.reference("Patients")
	return ref.get()

#To return the count of the total number of patients
"""
example usage:
>>>CountNumberOfPatients()
3
"""
def CountNumberOfPatients():
	StartDB()
	ref = db.reference("Patients")
	return (len(ref.get().values()))

#This function gets the total number of rooms in the DB:
"""
example usage:
>>>CountNumberOfRooms()
2
"""
def CountNumberOfRooms():
	StartDB()
	ref1 = db.reference("/Rooms/Critical")
	ref2 = db.reference("/Rooms/NonCritical")
	return (len(ref1.get()) + len(ref2.get()))

def GetAllPatientsInTheRoom(roomname):
	StartDB()
	list_of_patients = []
	ref = db.reference("/Patients")
	for patient in ref.get().values():
		if patient["room"] == roomname:
			list_of_patients.append({"name": patient["name"],"disease": patient["disease"]})
	return list_of_patients

#To return a dictionary where all keys are rooms and the values 
#are all patients names and diseases in that room
"""
example usage:
>>>GetRoomsWithPatients()
{'Blackwell': [{'name': 'Jack', 'disease': 'covid'}], 'Greywell': [], 
'Whitewell': [{'name': 'Devang', 'disease': 'COVID-19'}, {'name': 'Devang', 'disease': 'COVID-19'}, 
{'name': 'Palash', 'disease': 'COVID-19'}, {'name': 'Vaibhav', 'disease': 'COVID-19'}]}
"""
def GetRoomsWithPatients():
	StartDB()
	dict1 = {}
	ref = db.reference("/Rooms/Critical")
	for room in ref.get():
		dict1[room] = GetAllPatientsInTheRoom(room)
	ref2 = db.reference("/Rooms/NonCritical")
	for room in ref2.get():
		dict1[room] = GetAllPatientsInTheRoom(room)
	return dict1
#To add room by providing the room name, the number of beds,
#and if it houses critical patients or not ("True"/"False")  
def AddRooms(name,number_of_beds,critical):
	StartDB()
	if critical == 'True':
		ref = db.reference("/Rooms/Critical/"+name)
		ref.set({"Beds":int(number_of_beds),"Occupied":0})
	else:
		ref = db.reference("/Rooms/NonCritical/"+name)
		ref.set({"Beds":int(number_of_beds),"Occupied":0})

#Remove a room by taking the name of the room as an input
def RemoveRooms(name):
	StartDB()

	for key,value in RetrieveAllPatientRecords().items():
		if value["room"] == name:
			ref = db.reference("/Patients/"+key)
			ref.delete()

	ref = db.reference("/Rooms/Critical/"+name)
	ref.delete()
	
	ref2 = db.reference("/Rooms/NonCritical/"+name)
	ref2.delete()

#For ML.
def GetCountPatients():
	StartDB()
	num_critical = 0
	num_noncritical = 0
	for patient in list(RetrieveAllPatientRecords().values()):
		if patient["critical"] == "True":
			num_critical += 1
		else:
			num_noncritical +=1
	return [num_critical,num_noncritical]


#This function returns the names of all the diseases as a List
"""
example usage:
>>>GetDiseaseList()
['Cancer-related Intensive care', 'Heart Failure', 'Post-operative Intensive Care',
'Respiratory Failure', 'Ruptured Brain Aneurysm', 'Sepsis', 'Shock', 'Stroke', 'Trauma',
 'Traumatic Brain Injury']
"""
def GetDiseaseList():
	StartDB()
	ref = db.reference("Diseases")
	return list(ref.get().keys())
#This function returns the most recent record entered into the database. Used for ML.
def GetRecentRecord():
	StartDB()
	ref = db.reference("Patients")
	current_keys = ref.get().keys()
	current_max_id = max([int(this_id[7:]) for this_id in current_keys])
	recent_patient = GetPatientRecordByNumber(current_max_id)
	return recent_patient

#Take the patient ID, patient name, and the kind of unit (critical/non-critical)
#that the patient is to be sent to.
def UpdateRecord(patient_id,patient_name,critical):
	record = GetPatientRecordByNumber(patient_id)
	DeletePatientByNumberAndName(patient_id,patient_name)
	if critical == "True":
		record['critical'] = "True"
	else:
		record['critical'] = "False"
	EnterIntoPatientDB(record)

############## ML PART ##################

def GetTheta():
	f1 = open("Theta.obj","rb")
	Theta = pickle.load(f1)
	return Theta

#Called whenever a record is input after going through ML decision making
def GradientDescent(patient,Input,Alpha = 0.01):
	X = FeatureMaker(patient)
	Theta = GetTheta()
	partial_derivative = [0 for _ in range(0,len(Theta))]
	for i in range(0,len(X)):
		partial_derivative[i] = (Hypothesis() - Input)*X[i]
		Theta[i] -= Alpha * partial_derivative[i]

#High scores are bad
def FeatureMaker(patient_chosen = None):
	if patient_chosen == None:
		patient_taken = GetRecentRecord()
	else:
		patient_taken = patient_chosen
	X = []
	X.append(float(patient_taken["age"])/50)
	if(patient_taken["alcohol"] == "True"):
		X.append(1)
	else:
		X.append(0)
	if(patient_taken["criminal"] == "True"):
		X.append(1)
	else:
		X.append(0)
	if(patient_taken["critical"] == "True"):
		X.append(1)
	else:
		X.append(0)
	X.append(5/float(patient_taken["eco_status"]))
	if(patient_taken["marital_status"] != "single"):
		X.append(0)
	else:
		X.append(1)
	X.append(3/(float(patient_taken["dependents"])+1))
	X.append(patient_taken["mortality rate"]/100)
	X.extend([pow(k,2) for k in X])	
	return X

def Hypothesis(patient_chosen = None):
	if patient_chosen == None:
		patient_taken = None
	else:
		patient_taken = patient_chosen
	Theta = GetTheta()
	X = FeatureMaker(patient_taken)
	Z = 0
	for i in range(0,len(X)):
		Z += X[i]*Theta[i]
	hypo = 1/(1+pow(math.e,(-1*Z)))
	return hypo
#On calling this function, you will be given the record of the patient
#which is the most likely to be removed from the system.
def GetTopPatient():
	All_Patients = RetrieveAllPatientRecords()
	max_hypo_c = 0
	max_hypo_nc = 0
	max_patient_c = None
	max_patient_nc = None
	for patient,values in All_Patients.items():
		if (Hypothesis(All_Patients[patient]))>=max_hypo_c and values['critical'] == 'True':
			max_hypo_c = Hypothesis(All_Patients[patient])
			max_patient_c = patient
		elif (Hypothesis(All_Patients[patient]))>=max_hypo_nc and values['critical'] == 'False':
			max_hypo_nc = Hypothesis(All_Patients[patient])
			max_patient_nc = patient
	return [GetPatientRecordByNumber(int(max_patient_c[7:])),GetPatientRecordByNumber(int(max_patient_nc[7:]))]  

#This is called once the doctor is affirmative that he wants to replace the patient
def ReplacePatient(patient_to_replace):
	StartDB()
	[critical_patient,non_critical_patient] = GetTopPatient()
	if patient_to_replace['critical'] == 'True':
		patient_being_replaced = critical_patient
	else:
		patient_being_replaced = non_critical_patient
	replaced_patient_status = patient_being_replaced['critical']
	patient_to_replace['room'] = patient_being_replaced['room']
	patient_to_replace['critical'] = patient_being_replaced['critical']
	for key,value in RetrieveAllPatientRecords().items():
		if value == patient_being_replaced:
			found_key = key
	patient_being_replaced['critical'] = "False"
	ref2 = db.reference("/Patients/"+found_key)
	ref2.set(patient_to_replace)
	if replaced_patient_status == "True":
		EnterIntoPatientDB(patient_being_replaced)
	else:
		pass

