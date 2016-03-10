clc; close all; clear;
dataRef= h5read('mode_estimation_resources.h5', '/signal_data/KTHLAB:EMLAB');
do= dataRef(1,:);
Y= do.';
order= 8;
[mode_freq_ref, mode_damp_ref]=mode_est_basic_fcn(Y, order);
dataSim= h5read('mode_estimation_resources.h5', '/signal_data/pmu1');
do= dataSim(1,:);
Y= do.';
[mode_freq_sim, mode_damp_sim]=mode_est_basic_fcn(Y, order);
hdf5write('mode_estimation_results.h5','/KTHLAB:EMLAB/freq', mode_freq_ref,'/KTHLAB:EMLAB/damp', mode_damp_ref,'/pmu1/freq', mode_freq_sim,'/pmu1/damp', mode_damp_sim);
exit
