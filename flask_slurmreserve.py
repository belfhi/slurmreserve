from slurmreserve import *
import datetime
import time
import mimetypes
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

app.config['LDAP_PROVIDER_URL'] = ""

mimetypes.add_type('image/svg+xml', '.svg')

@app.route('/')
def showPartitions():
	partitions = get_partition("test")

	return render_template('partitions.html', partitions=partitions)

@app.route('/partitions/<string:partition>/reservations')
def showReservations(partition):
	
	reservations = get_all_reservations(partition);

	if reservations:
		return render_template('reservations.html', partition=partition, reservations=reservations)
	
	return render_template('reservations.html', partition=partition)

@app.route('/partitions/<string:partition>/reservations/filter/<string:filter_string>')
def showFilteredReservations(partition, filter_string):

	reservations = get_all_reservations(partition);

	if reservations:
		filtered_list = []
		for d in reservations:
	
			if(filter_string in d["users"] or filter_string in d["name"]):
				filtered_list.append(d)

		return render_template('reservations.html', partition=partition, reservations=filtered_list, filter_string=filter_string)
	
	
	return render_template('reservations.html', partition=partition)

@app.route('/partitions/<string:partition>/reservations/new', methods=['GET', 'POST'])
def newReservations(partition):
	
	now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S");
	error = False

	if request.method == 'POST':
		dic = create_dict()
		dic['name'] = request.form['name']
		dic['node_cnt'] = (int)(request.form['node_cnt'])

		try:
			dic['start_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['start_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
			dic['end_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['end_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
		except:
			print("Can't parse time.")
			error = True

		dic["users"] = request.form['users'].replace(" ", "")
		dic["partition"] = partition
		
		try:
			res_id = create_reservation(dic)
		except ValueError as e:
			error = True

		if error:
			return render_template('new.html',  partition=partition, error="value error", name=dic['name'], node_cnt=dic['node_cnt'], now=now, 
				start_time=request.form['start_time'], end_time=request.form['end_time'], users=dic["users"])

		return redirect('/partitions/' + partition + '/reservations')

		
	return render_template('new.html',  partition=partition, now=now, start_time=now, end_time=now)


@app.route('/partitions/<string:partition>/reservations/<string:res_id>/edit', methods=['GET', 'POST'])
def editReservations(partition, res_id):

	error = False
	dic = {}
	startTime = ""
	endTime = ""

	if request.method == 'POST':
		dic = create_dict()
		dic['name'] = res_id
		dic['node_cnt'] = (int)(request.form['node_cnt'])
		dic["users"] = request.form['users'].replace(" ", "")

		try:
			startTime = request.form['start_time']
			if request.args.has_key('start_time'):
				dic['start_time'] = (int)(time.mktime(datetime.datetime.strptime(startTime, "%Y-%m-%dT%H:%M:%S").timetuple()))

			endTime = request.form['end_time']
			dic['end_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['end_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
		except:
			print("Can't parse time.")

		try:
			res = update_reservation(dic)

			print(res);
			if res == 0:
				return redirect('/partitions/' + partition + '/reservations')

		except ValueError as e:
				print("Error on edit")
		error = True		

		
	
	reservation = dic
	reservation['start_time'] = startTime
	reservation['end_time'] = endTime

	showStartTimeInput = True

	if not error:
		reservation = get_reservation(partition,  res_id);
		reservation['users'] = ",".join(reservation['users'])

	try:
		startTime = datetime.datetime.strptime(reservation['start_time'], "%Y-%m-%dT%H:%M:%S")
		showStartTimeInput = (startTime > datetime.datetime.now())
	except:			
		print("Can't parse time.")

	now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S");

	return render_template('edit.html', partition=partition, error=error, res_id=res_id, reservation=reservation, showStart=showStartTimeInput, now=now)

@app.route('/partitions/<string:partition>/reservations/<string:res_id>/delete', methods=['POST'])
def deleteReservations(partition, res_id):
	if request.method == 'POST':
		try:
			delete_reservation(res_id,"test")
		except ValueError as e:
			return "Error on delete"
	return "delete"