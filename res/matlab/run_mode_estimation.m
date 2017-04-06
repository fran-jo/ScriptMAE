clc; close all; clear;
dataRef= h5read('mode_estimation_resources.h5', '/signal_data/NTNU_PMU:Va');
do= dataRef(1,:);
Y= do.';
order= 2;
[mode_freq_ref, mode_damp_ref]=mode_est_basic_fcn(Y, order);
dataSim= h5read('mode_estimation_resources.h5', '/signal_data/BUS3');
do= dataSim(1,:);
Y= do.';
[mode_freq_sim, mode_damp_sim]=mode_est_basic_fcn(Y, order);
hdf5write('mode_estimation_results.h5','/NTNU_PMU:Va/freq', mode_freq_ref,'/NTNU_PMU:Va/damp', mode_damp_ref,'/BUS3/freq', mode_freq_sim,'/BUS3/damp', mode_damp_sim);
exit
