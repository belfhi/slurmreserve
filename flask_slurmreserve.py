from flask import Flask, redirect, request, render_template
import slurmreserve.slurmreserve as slurmreserve


app = Flask(__name__)

@app.route('/')
def showPartitions():
	partitions = slurmreserve.get_partition("test")

	return render_template('partitions.html', partitions=partitions)



@app.route('/partitions/<string:partition>/reservations')
def showReservations(partition):
	
	reservations = slurmreserve.get_reservation(partition);

	if reservations:
		return render_template('reservations.html', partition=partition, reservations=reservations)
	
	return render_template('reservations.html', partition=partition)

@app.route('/partitions/<string:partition>/new', methods=['GET', 'POST'])
def newReservations(partition):
	

	return "new"

@app.route('/partitions/<string:partition>/edit', methods=['GET', 'POST'])
def editReservations(partition):
	

	return "edit"

@app.route('/partitions/<string:partition>/delete', methods=['POST'])
def deleteReservations(partition):
	

	return "delete"


