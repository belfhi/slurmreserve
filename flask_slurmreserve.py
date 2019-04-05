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

	if request.method == 'POST':

		
		dic = create_dict()
		dic['name'] = request.form['name']
		dic['node_cnt'] = (int)(request.form['node_cnt'])

		dic['start_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['start_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
		dic['end_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['end_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
		dic["users"] = "roses"
		dic["partition"] = partition
		
		try:
			res_id = create_reservation(dic)
		except ValueError as e:
			return render_template('new.html',  partition=partition, error="value error", name=dic['name'], node_cnt=dic['node_cnt'], now=now, start_time=request.form['start_time'], end_time=request.form['end_time'])

		return redirect('/partitions/' + partition + '/reservations')

		
	return render_template('new.html',  partition=partition, now=now, start_time=now, end_time=now)


@app.route('/partitions/<string:partition>/reservations/<string:res_id>/edit', methods=['GET', 'POST'])
def editReservations(partition, res_id):

	if request.method == 'POST':
		dic = create_dict()
		dic['name'] = res_id
		dic['node_cnt'] = (int)(request.form['node_cnt'])
		if request.args.has_key('start_time'):
			dic['start_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['start_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))
		dic['end_time'] = (int)(time.mktime(datetime.datetime.strptime(request.form['end_time'], "%Y-%m-%dT%H:%M:%S").timetuple()))

		try:
			update_reservation(dic)
		except ValueError as e:
			return "Error on edit"

		return redirect('/partitions/' + partition + '/reservations')

	reservation = get_reservation(partition,  res_id);
	now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S");
	startTime = datetime.datetime.strptime(reservation['start_time'], "%Y-%m-%dT%H:%M:%S")


	return render_template('edit.html', partition=partition, res_id=res_id, reservation=reservation, showStart= (startTime > datetime.datetime.now())
	 ,now=now)

@app.route('/partitions/<string:partition>/reservations/<string:res_id>/delete', methods=['POST'])
def deleteReservations(partition, res_id):
	if request.method == 'POST':
		try:
			delete_reservation(res_id,"test")
		except ValueError as e:
			return "Error on delete"
	return "delete"