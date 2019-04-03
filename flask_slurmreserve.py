from slurmreserve import *
import datetime
from flask import Flask, redirect, request, render_template

app = Flask(__name__)

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
	
	if request.method == 'POST':
		dic = create_dict()
		dic['name'] = request.form['name']
		dic['node_cnt'] = request.form['node_cnt']
		dic['start_time'] = request.form['start_time']
		dic['end_time'] = request.form['end_time']
		res_id = create_reservation(dic)
		print ("REST_ID: " + res_id)
		return redirect('/partitions/' + partition + '/reservations')

	return render_template('new.html',  partition=partition, now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

@app.route('/partitions/<string:partition>/reservations/<string:res_id>/edit', methods=['GET', 'POST'])
def editReservations(partition, res_id):

	if request.method == 'POST':
		dic = create_dict()
		dic['name'] = request.form['name']
		dic['node_cnt'] = request.form['node_cnt']
		dic['start_time'] = request.form['start_time']
		dic['end_time'] = request.form['end_time']

		return redirect('/partitions/' + partition + '/reservations')

	reservation = get_reservation(partition,  res_id);
	return render_template('edit.html', partition=partition, res_id=res_id, reservation=reservation, now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

@app.route('/partitions/reservations/<string:partition>/reservations/<string:res_id>/delete', methods=['POST'])
def deleteReservations(partition, res_id):
	if request.method == 'POST':
		print(res_id);

	return "delete"


