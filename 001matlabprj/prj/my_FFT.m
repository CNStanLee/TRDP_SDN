function [Y,f]=my_FFT(y,Fs)
%% This function computes the discrete Fourier transform thanks to the FFT
% input
% y : original signal
% Fs : sampling frequency
% output
% Y : discrete fourier transform
% f : vector of frequencies

NFFT=length(y);
f=(0:NFFT-1)'*Fs/NFFT;
f(f>=Fs/2)=f(f>=Fs/2)-Fs;
f=fftshift(f);
Y=fftshift(fft(y,NFFT));
