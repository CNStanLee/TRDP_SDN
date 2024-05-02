clear ;
close(gcf);
close(gcf);

%% 获取wireshark数据
pcapFile = 'x15.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.4.10';
IP(1).ip_dst = '239.255.2.0';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
%% 干扰数据 

att_factor = 0.06;
att = zeros(1,50);
j=1;
for i=500:1:599
    temp = x1(i) - att_factor*x1(i)*rand(1);
    if  temp>= 0
        att(j) = temp;
    else
        att(j) = x1(i);
    end
    j=j+1;
end
x1 = [x1(1:499), att(1:100), x1(600:length(x1))];

j=1;
for i=1000:1:1099
    temp = x1(i) - att_factor*x1(i)*rand(1);
    if  temp>= 0
        att(j) = temp;
    else
        att(j) = x1(i);
    end
    j=j+1;
end
x1 = [x1(1:999), att(1:100), x1(1200:length(x1))];
abnormal_data = x1;
%% print data