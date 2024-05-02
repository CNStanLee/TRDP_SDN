% Load the audio file
%file_path = 'piano-C5.wav';
%file_path = 'flute-C5.wav';
%file_path = 'trumpet-C5.wav';
file_path = 'violin-C5.wav';
[y, fs] = audioread(file_path);


% Set parameters for the spectrogram
%desired_window_duration = 0.04; % 40 ms
desired_window_duration = 1.4; % full note

window_length = 2^nextpow2(round(desired_window_duration * fs)); % Round up to the nearest power of two
overlap = round(window_length / 2); % Set the overlap to be half the window length
nfft = window_length; % Number of FFT points, equal to window length for no zero-padding

% Create the spectrogram
[S, F, T] = spectrogram(y, window_length, overlap, nfft, fs);

% Plot the spectrogram in grayscale with white background
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);

set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time (seconds)');
ylabel('Frequency (Hz)');
title('Spectrogram of Violin Full Note');


% Add a colorbar to show intensity
colorbar;
