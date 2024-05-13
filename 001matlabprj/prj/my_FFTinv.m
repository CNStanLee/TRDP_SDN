function [y]=my_FFTinv(Y)
%% This function computes the inverse discrete FOurier transform thanks to the FFT
% input
% Y : discrete Fourier transform
% output
% y : signal in the time domain

Y=ifftshift(Y);
y=ifft(Y);