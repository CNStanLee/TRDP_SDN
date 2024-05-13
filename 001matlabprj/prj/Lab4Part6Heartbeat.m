% --------------------------------- %
% Lab4 Part 5 Speech
% --------------------------------- %
clear;
clc;
close all;
% --------------------------------- %
% Load dataset
% --------------------------------- %

T = readtable ('ptbdb_normal.csv') ;

Tarray = table2array ( T ) ;
normalPatient = Tarray (6 ,1: end) ;

T = readtable ('ptbdb_abnormal.csv') ;
Tarray = table2array ( T ) ;
abnormalPatient = Tarray (6 ,1: end) ;

t = 1 : 1 : length(normalPatient);

figure;

subplot(2,1,1);
plot(t, normalPatient);
title("normal patient");
xlabel("t");
ylabel("Amp");


subplot(2,1,2);
plot(t, abnormalPatient);
title("abnormal patient");
xlabel("t");
ylabel("Amp");


sgtitle("ptbddb");



% --------------------------------- %
% SFFT
% --------------------------------- %

fs = 1;

desired_window_duration = 2; % 40 ms
window_length = 2^nextpow2(round(desired_window_duration * fs)); % Round up to the nearest power of two
overlap = round(window_length / 2); % Set the overlap to be half the window length
nfft = window_length; % Number of FFT points, equal to window length for no zero-padding


% Create the spectrogram
[S, F, T] = spectrogram(normalPatient, window_length, overlap, nfft, fs);
%[S, F, T] = spectrogram(normalPatient);
figure;

% Plot the spectrogram in grayscale with white background
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);

set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time');
ylabel('Frequency (Hz)');
title('Spectrogram normal');

% Add a colorbar to show intensity
colorbar;
% --------------------------------- %
% SFFT
% --------------------------------- %

fs = 1;

desired_window_duration = 2; % 40 ms
window_length = 2^nextpow2(round(desired_window_duration * fs)); % Round up to the nearest power of two
overlap = round(window_length / 2); % Set the overlap to be half the window length
nfft = window_length; % Number of FFT points, equal to window length for no zero-padding


% Create the spectrogram
[S, F, T] = spectrogram(abnormalPatient, window_length, overlap, nfft, fs);
%[S, F, T] = spectrogram(abnormalPatient);

figure;

% Plot the spectrogram in grayscale with white background
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);

set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time');
ylabel('Frequency (Hz)');
title('Spectrogram abnormal');

% Add a colorbar to show intensity
colorbar;




