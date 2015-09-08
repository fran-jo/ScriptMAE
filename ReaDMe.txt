PhasorMeasH5.py with API to read/write 1 signal.
	Get
	Set (complex or polar)
	calc phasor from complex
	create (create the .h5 file with group/attribute)
	open (open the .h5 file)
	save (save signal data into dataset and save file .h5 with attributes/dataset)
	load (open the .h5 file and load group/attribute/dataset)
	
	program arguments for abc2phasor.py
	./res/
	SimulationOutputs.h5
	./res/SMIB1L_Group1_Nordic44.mat
	
	program arguments for loadabch5.py
	./res/
	SimulationOutputs.h5
	
	program arguments for loadcsv.py
	./res/File_5.csv
	,
	
.mat files we use ModelicaRes

Model resources for ERA test 
	PMUdata_Bus1VA2VALoad9PQ.csv, this file or relevant CSV file can be access for ERA
	
Requirements for Mode Estimation algorithm:
	mes.jar file is included in ROOT_PROJECT/lib, this folder is added to the classpath of the project
		(for testing, passing as input to the script
		
	mode_est_basic_fcn.m should be located under ROOT_PROJECT/res (if it dosen't work sometimes matlab 
		needs to set the matlab working directory)
		
	Matlab command "data = h5read('PMUdata_Bus1VA2VALoad9PQ.h5','/df/block0_values');" is sent via uSeRTeST.txt 
		(previous name was file.txt), sent to matlab through using matlabcontrol

