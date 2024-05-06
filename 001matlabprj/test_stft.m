%% clear all the data
clear ;
close(gcf);
close(gcf);
clc;
%% parse the data from wireshark
pcapFile = 'sim2.pcap';
pcapReaderObj  = pcapReader(pcapFile);
decodedPackets = readAll(pcapReaderObj);

% 初始化变量
uniqueIPs = []; % 存储所有唯一的源IP地址
Fs = 1000; % 采样频率，假设为1000Hz
windowSize = 512; % 窗口大小
overlap = 0.5; % 重叠比例
nfft = 1024; % FFT长度


IP = struct('ip_str','ip_dst','Data','Timestamp');


[IP(1).Data, IP(1).Timestamp] = pcapDataRead(decodedPackets);

%%
% 遍历每个数据包
for i = 1:numel(decodedPackets)
    eth = decodedPackets(i).Packet.eth.SourceAddress;
    sourceAddress = eth.SourceAddress;
    if ~ismember(sourceAddress, uniqueIPs)
        uniqueIPs = [uniqueIPs, sourceAddress];
    end
end