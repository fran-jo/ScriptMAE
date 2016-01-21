clc; close all; clear;
data= h5read('C:/Users/fragom/PhD_CIM/PYTHON/SimuGUI/res/matlab/IEEENetworks2.IEEE_9Bus_&dymola_new_Enam.h5', '/IEEENetworks2.IEEE_9Bus/pmu4_values');
do= data(2,:);
Y= do.';
order= 10;
[mode_freq, mode_damp]=mode_est_basic_fcn(Y, order);
hdf5write('mode_estimation.h5','/mode_estimation/freq', mode_freq,'/mode_estimation/damp', mode_damp);
exit
