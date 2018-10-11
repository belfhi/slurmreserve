from flask import Flask, redirect, request, render_template

app = Flask(__name__)

@app.route('/')
def showPartitions():
	partitions = [{'name': "Test1"},{'name': "bl1"},{'name': "root_79"},{'name':"test4"}]

	return render_template('partitions.html', partitions=partitions)



@app.route('/partitions/<string:partition>/reservations')
def showReservations(partition):
	
	reservations = {'bl1': {'accounts': [], 'burst_buffer': [], 'core_cnt': 20, 'end_time': 1539619200, 'features': [], 'flags': 'IGNORE_JOBS,SPEC_NODES', 'licenses': {}, 'node_cnt': 1, 'node_list': 'max-p3a009', 'partition': None, 'start_time': 1538060858, 'tres_str': ['cpu=40'], 'users': ['alfaro', 'baris', 'baumannt', 'blume', 'bollre', 'defanis', 'doerners', 'grychtol', 'hartmang', 'ilchen', 'jkotan', 'kartikv', 'kracht', 'kschuber', 'kuhnm', 'kurz', 'leejason', 'lschwob', 'medved', 'mfleck', 'mimeyer', 'musicv', 'ovcharen', 'rolled', 'rosem', 'rothkirc', 'rowoldt', 'schluenz', 'schmidtp', 'schooft', 'sternber', 'tmazza', 'tnunez', 'yakubov', 'yuelong']}, 'root_79': {'accounts': [], 'burst_buffer': [], 'core_cnt': 1584, 'end_time': 1539100800, 'features': [], 'flags': 'MAINT,SPEC_NODES', 'licenses': {}, 'node_cnt': 44, 'node_list': 'max-exfl[101,103,105,107,109,111,113,115,117,119,121,123,125,127,129,131,133,135,137,139,141,143,145,147,149,151,153,155,157,159,161,163,165,167,169,171,173,175,177,179,181,183,185,187]', 'partition': None, 'start_time': 1538978400, 'tres_str': ['cpu=3168'], 'users': ['root']}}

	if partition in reservations:
		return render_template('reservations.html', partition=partition, reservations=[reservations[partition],reservations[partition],reservations[partition],reservations[partition],reservations[partition]])
	
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


