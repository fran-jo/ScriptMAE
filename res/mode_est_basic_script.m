d = fdesign.lowpass(2/25, 2.5/25, 0.1, 50 );
Hlp=design(d);
signal=filter(Hlp, signal);
signal=downsample(signal,10);

dt=0.2;
Len=length(signal);
u1=zeros(Len,1);
data=iddata(signal,u1,dt);

na=order;
nb=0;
nc=order;
nk=1; %delay
tic

sys_est = armax(data,[na nb nc nk]);

[Wn,zeta]= damp(sys_est);
[zeta,I]=sort(zeta);
Wn=Wn(I);
[mode_damp, I]=unique(zeta);
mode_freq=Wn(I);
idx=find(mode_freq<6);

mode_freq=mode_freq(idx);
mode_damp=mode_damp(idx);