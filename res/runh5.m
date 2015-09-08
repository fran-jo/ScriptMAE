close all;
clear;
%data = h5read('PMUdata_Bus1VA2VALoad9PQ.h5','/df/block0_values');
do=data(2,:);
Y=do.'
order=18;
[mode_freq, mode_damp,data]=mode_est_basic_fcn(Y, order);
disp('    freq#######damp######')

disp([mode_freq  mode_damp])
disp('data')
%disp([data])

datasett=[mode_freq mode_damp]

hdf5write('mode_est_result.h5','/dampfreq',datasett);
%csvwrite('mode_est_result.csv',datasett);