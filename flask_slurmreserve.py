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

@app.route('/partitions/<string:partition>/new', methods=['GET', 'POST'])
def newReservations(partition):
	
	if request.method == 'POST':
		return redirect('/partitions/' + partition + '/reservations')



	return render_template('new.html', now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

@app.route('/partitions/<string:partition>/<string:res_id>/edit', methods=['GET', 'POST'])
def editReservations(partition, res_id):
	
	reservation = get_reservation(partition,  res_id);
	return render_template('edit.html', res_id=res_id, reservation=reservation, now=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))

@app.route('/partitions/<string:partition>/delete', methods=['POST'])
def deleteReservations(partition):
	

	return "delete"


