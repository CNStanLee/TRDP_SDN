% --------------------------------- %
% Lab4 Part 4 Queen
% --------------------------------- %
clear;
clc;
close all;
% --------------------------------- %
% Load audio file
% --------------------------------- %
file_path = 'QueenAnotherOneBitesTheDust.mp3';
[y, fs] = audioread(file_path);

y = y(148*fs - 1 : 151*fs - 1,:);

y1 = y(:, 1);
y2 = y(:, 2);

t = 0 : 1 / fs : (length(y1) -1)/ fs;

figure;
plot(t, y1);
hold on;
plot(t, y2);



% --------------------------------- %
% SFFT
% --------------------------------- %

desired_window_duration = 0.04; % 40 ms
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

%% optional
clear;
clc;
close all;
% --------------------------------- %
% Load audio file
% --------------------------------- %
file_path = 'QueenAnotherOneBitesTheDust.mp3';
[y, fs] = audioread(file_path);

y = y(1*fs - 1 : 8*fs - 1,:);

y1 = y(:, 1);
y2 = y(:, 2);

t = 0 : 1 / fs : (length(y1) -1)/ fs;

figure;
plot(t, y1);
hold on;
plot(t, y2);



% --------------------------------- %
% SFFT
% --------------------------------- %

desired_window_duration = 0.04; % 40 ms
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


