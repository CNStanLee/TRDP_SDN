clear ;
close(gcf);
close(gcf);
clc;
close all;

% get the data from the wireshark
% sim2 is a normal data

% sim7 is the data that use strategy 1
% attack ip 10.0.3.120
% data type: not struct

% sim8 is the data that use strategy 2
% attack ip 10.0.2.160
% data type: not struct

% sim9 is the data that use strategy 3
% attack ip 10.0.3.160
% under atk ip 10.0.3.40
% data type: not struct

pcapFile = 'sim9_under_atk.pcap';
pcapReaderObj  = pcapReader(pcapFile);
decodedPackets = readAll(pcapReaderObj);
length_of_pack = length(decodedPackets);

% get the timestamp features from the packet
time_stamp_series = [];
% check the structure fo the data packet
if isstruct(decodedPackets(1).Packet)
% is struct
    for i = 1 : length_of_pack
        timestamp_value = decodedPackets(i).Timestamp;
        if decodedPackets(i).Packet.eth.Payload(10) == 17 ...
                && decodedPackets(i).Packet.eth.Payload(13) == 10 ...
                && decodedPackets(i).Packet.eth.Payload(14) == 0 ...
                && decodedPackets(i).Packet.eth.Payload(15) == 3 ...
                && decodedPackets(i).Packet.eth.Payload(16) == 40 
            time_stamp_series = [time_stamp_series, timestamp_value];
        end
    end
else
    for i = 1 : length_of_pack
        timestamp_value = decodedPackets(i).Timestamp;
        if decodedPackets(i).Packet(26) == 17 ...
                && decodedPackets(i).Packet(29) == 10 ...
                && decodedPackets(i).Packet(30) == 0 ...
                && decodedPackets(i).Packet(31) == 3 ...
                && decodedPackets(i).Packet(32) == 40 
            time_stamp_series = [time_stamp_series, timestamp_value];
        end
    end
end


% for i = 1 : length_of_pack
%     timestamp_value = decodedPackets(i).Timestamp;
%     time_stamp_series = [time_stamp_series, timestamp_value];
% end


% normalize the time
% delete the offset and rerange time to 0-10000
min_time_stamp = min(time_stamp_series);
max_time_stamp = max(time_stamp_series);
time_stamp_series_norm = time_stamp_series - min_time_stamp;
max_time_norm = max(time_stamp_series_norm);
%time_stamp_series_mapped = (time_stamp_series_norm / max_time_norm) * 9999 + 1;
time_stamp_series_mapped = time_stamp_series_norm/1e6;

% total time(s)
total_sample_time = (max_time_stamp - min_time_stamp)/1e6;
% total sample number
total_sample_num = length(time_stamp_series_mapped);
% sampling frequency 200Hz
ori_sampling_frequency = total_sample_num / total_sample_time;
fs = 100;
time_slot_num = floor(fs * total_sample_time) + 2;
time_interval = 1 / fs;
% calculate the msg num in each time slot
values_count = zeros(1, time_slot_num);

for i = 1:length(time_stamp_series_mapped) - 1
    time_interval_belong = ceil(time_stamp_series_mapped(i) / time_interval) + 1;
    values_count(time_interval_belong) = values_count(time_interval_belong) + 1;
end

figure;
plot(values_count);
xlabel('num of the time block');
ylabel('message number');
title('message number vs time slot');

% fft
xdis = values_count;
nfft = 3^10;        % point num of fft
X = fft(xdis, nfft);   % fast fourier transform
fstep = fs/nfft;    % step size of the Frequency in figure
fvec = fstep * (0 : nfft/2-1); % x of the figure range from 0 to nfft/2 -1
fresp = 2*abs(X(1:nfft/2));     % take 1/2 abs val of X

figure;
plot(fvec, fresp)                % plot the figure 
title('Single-Sided Amplitude Spectrum of x(t)') % title of the figure
xlabel('Frequency (Hz)') % label for x
ylabel('|X(f)|')    % label for y

% utilize filter
filtered = filter(bpf1, values_count);

% fft
xdis = filtered;
nfft = 3^10;        % point num of fft
X = fft(xdis, nfft);   % fast fourier transform
fstep = fs/nfft;    % step size of the Frequency in figure
fvec = fstep * (0 : nfft/2-1); % x of the figure range from 0 to nfft/2 -1
fresp = 2*abs(X(1:nfft/2));     % take 1/2 abs val of X

figure;
plot(fvec, fresp)                % plot the figure 
title('Single-Sided Amplitude Spectrum of x(t)') % title of the figure
xlabel('Frequency (Hz)') % label for x
ylabel('|X(f)|')    % label for y

% use SFFT
desired_window_duration = 2;
window_length = 2^nextpow2(round(desired_window_duration * fs));
overlap = round(window_length / 2);
nfft = window_length * 8;

[S, F, T] = spectrogram(filtered, window_length, overlap, nfft, fs);
figure;
imagesc(T, F, 10*log10(abs(S)), [min(min(10*log10(abs(S)))) max(max(10*log10(abs(S))))]);
set(gca, 'YDir', 'normal'); % This is to ensure that the frequency axis is displayed correctly

% Set the figure background color to white
set(gcf, 'color', 'w');

% Add labels and title
xlabel('Time');
ylabel('Frequency');
title('Spectrogram');

% Add a colorbar to show intensity
colorbar;
colormap(jet);