close all;
clear;

load LinearSystem64
Len=30000;
dt=0.02;
t=(0:Len-1)*dt;
order=18;

k=203+48;
sys=ss(A,B,C(k,:),D(k,:));

u=randn(Len,size(B,2));
y=lsim(sys,u,t);

[mode_freq, mode_damp]=mode_est_basic_fcn(y, order);

disp('    freq   and  damp')
disp([mode_freq  mode_damp])




