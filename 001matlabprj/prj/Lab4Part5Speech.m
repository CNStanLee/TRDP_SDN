% --------------------------------- %
% Lab4 Part 5 Speech
% --------------------------------- %
clear;
clc;
close all;
% --------------------------------- %
% load audio file
% --------------------------------- %

file_path = 'OSR_us_000_0010_8k.wav';
[y, fs] = audioread(file_path);

y = y(1*fs - 1 : 33*fs - 1,:);

y1 = y(:, 1);
%y2 = y(:, 2);

t = 0 : 1 / fs : (length(y1) -1)/ fs;

figure;
plot(t, y1);
%hold on;
%plot(t, y2);



% --------------------------------- %
% SFFT
% --------------------------------- %

desired_window_duration = 0.06; % 40 ms
window_length = 2^nextpow2(round(desired_window_duration * fs)); % Round up to the nearest power of two
overlap = round(window_length / 2); % Set the overlap to be half the window length
nfft = window_length; % Number of FFT points, equal to window length for no zero-padding


% Create the spectrogram
[S, F, T] = spectrogram(y1, window_length, overlap, nfft, fs);

% Plot the spectrogram in grayscale with white background
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);

set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time (seconds)');
ylabel('Frequency (Hz)');
title('Spectrogram of Flute Note');

% Add a colorbar to show intensity
colorbar;


%%


note = createNote(40, 98, fs, 0);
y_note = y1 + note(1 : 256001);

desired_window_duration = 0.04; % 40 ms
window_length = 2^nextpow2(round(desired_window_duration * fs)); % Round up to the nearest power of two
overlap = round(window_length / 2); % Set the overlap to be half the window length
nfft = window_length; % Number of FFT points, equal to window length for no zero-padding


% Create the spectrogram
[S, F, T] = spectrogram(y_note, window_length, overlap, nfft, fs);

% Plot the spectrogram in grayscale with white background
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);

set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time (seconds)');
ylabel('Frequency (Hz)');
title('Spectrogram of Flute Note');

% Add a colorbar to show intensity
colorbar;