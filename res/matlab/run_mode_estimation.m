clc; close all; clear;
dataRef= h5read('mode_estimation_resources.h5', '/signal_data/LTH:LAB6');
do= dataRef(1,:);
Y= do.';
order= 4;
[mode_freq_ref, mode_damp_ref]=mode_est_basic_fcn(Y, order);
dataSim= h5read('mode_estimation_resources.h5', '/signal_data/B3');
do= dataSim(1,:);
Y= do.';
[mode_freq_sim, mode_damp_sim]=mode_est_basic_fcn(Y, order);
hdf5write('mode_estimation_results.h5','/LTH:LAB6/freq', mode_freq_ref,'/LTH:LAB6/damp', mode_damp_ref,'/B3/freq', mode_freq_sim,'/B3/damp', mode_damp_sim);
exit
