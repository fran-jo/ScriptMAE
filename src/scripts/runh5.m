close all;
clear;

%load LinearSystem64
data2 = h5read('pandas5.h5','/df/block0_values');

order=18;
y=data2(1,:)
Y=y.'
[mode_freq, mode_damp]=mode_est_basic_fcn(Y, order);
disp('    freq   and  damp')
disp([mode_freq  mode_damp])


