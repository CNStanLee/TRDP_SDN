% get the data from the wireshark
% sim2 is a normal data

% sim7 is the data that use strategy 1
% attack ip 10.0.3.120
% data type: not struct

% sim8 is the data that use strategy 3
% attack ip 10.0.2.160
% data type: not struct

% sim9 is the data that use strategy 3
% attack ip 10.0.3.160
% under atk ip 10.0.3.40
% data type: not struct

%% sim 2 normal data
clear ;
close(gcf);
close(gcf);
clc;
pcapFile = 'sim2.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.4.100';
IP(1).ip_dst = '239.255.17.1';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead2(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
save('sim2_normal_data.mat', 'normal_data');

%% sim 7 s1
clear ;
close(gcf);
close(gcf);
clc;
pcapFile = 'sim7.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.3.120';
IP(1).ip_dst = '239.255.13.1';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
save('sim7_s1', 'normal_data');
%% sim 8 s2
clear ;
close(gcf);
close(gcf);
clc;
pcapFile = 'sim8.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.2.160';
IP(1).ip_dst = '239.255.11.1';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
save('sim8_s2', 'normal_data');

%% sim 9 s3 atk
clear ;
close(gcf);
close(gcf);
clc;
pcapFile = 'sim9_dos_atk.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.3.160';
IP(1).ip_dst = '239.255.14.1';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead2(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
save('sim9_dos_atk', 'normal_data');

%% sim 9 under atk
clear ;
close(gcf);
close(gcf);
clc;
pcapFile = 'sim9_under_atk.pcap';
pcapReaderObj  = pcapReader(pcapFile); % 使用pcapfile库读取数据
decodedPackets = readAll(pcapReaderObj);



IP = struct('ip_str','ip_dst','Data','Timestamp');
IP(1).ip_str = '10.0.3.40';
IP(1).ip_dst = '239.255.12.1';

[IP(1).Data, IP(1).Timestamp] = pcapDataRead2(decodedPackets,IP(1).ip_str,IP(1).ip_dst);
x1 = 1.*diff(IP(1).Timestamp);
min_x = min(x1);
max_x = max(x1);

% x1 = flowcalculation(decodedPackets);   % 计算流量
normal_data = x1;
save('sim9_under_atk', 'normal_data');

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


%% 计算ms_stft

% 1. 波形基函数：这里使用Morlet小波作为示例
omega0 = 6; % 中心频率（角频率）
wavelet = @(t) pi^(-0.25) * exp(1i*omega0*t) .* exp(-0.5*t.^2); % Morlet小波定义
% wavelet = @(n,t) pi^(-0.25) * exp(1i*omega0*n) .* exp(-0.5*t.^2); % Morlet小波定义

% 2. 分析参数
% scale_vector = [1, 2, 4, 8]; % 多尺度参数a的选择
scale_vector = 2.^(-(0:3));
window_length = 20; % 窗口长度L
overlap_fraction = 0.95; % 窗口重叠比例

% 3. 初始化STFT结果
num_scales = length(scale_vector);
ms_stft_result = zeros(num_scales, floor((length(x1) - window_length) / (window_length * (1 - overlap_fraction)) + 1));


% 4. 计算ms_stft
ms_stft_result = ms_stft(x1,window_length,overlap_fraction,omega0,scale_vector);
ms_stft_normal = ms_stft(normal_data,window_length,overlap_fraction,omega0,scale_vector);

%% 

figure;  % 新建一个图形窗口

for i = 1:4  % 遍历每个特征
    subplot(2, 2, i);  % 在图形窗口中创建子图，布局为 2 行 2 列
    ms_stft = abs(ms_stft_result(i,:));  % 获取第 i 个特征的 MS-STFT 结果

    % 显示 MS-STFT 图像
    imagesc(ms_stft);

    % 添加颜色条
    colorbar;

    % 设置坐标标签
    xlabel('Time Points');
    ylabel('Scales');

    % 选择合适的颜色映射，如 hot 或 cool 等
    colormap('hot');

    % 根据需要调整图像的缩放和平移
    axis tight;
end

%% check normal data stft

figure;  % 新建一个图形窗口

for i = 1:4  % 遍历每个特征
    subplot(2, 2, i);  % 在图形窗口中创建子图，布局为 2 行 2 列
    ms_stft = abs(ms_stft_normal(i,:));  % 获取第 i 个特征的 MS-STFT 结果

    % 显示 MS-STFT 图像
    imagesc(ms_stft);

    % 添加颜色条
    colorbar;

    % 设置坐标标签
    xlabel('Time Points');
    ylabel('Scales');

    % 选择合适的颜色映射，如 hot 或 cool 等
    colormap('hot');

    % 根据需要调整图像的缩放和平移
    axis tight;
end


sta = zeros(1,5);

for i=1:4
     % max_m(i) = max(max(real(ms_stft_result(i,1:480))),max(real(ms_stft_result(i,650:length(ms_stft_result(i,:))))));
     % min_m(i) = min(min(real(ms_stft_result(i,1:480))),min(real(ms_stft_result(i,650:length(ms_stft_result(i,:))))));
    
     max_m(i) = max(real(ms_stft_result(i,1:100)));
     min_m(i) = min(real(ms_stft_result(i,1:100)));
    for j=1:length(ms_stft_result(i,:))
        if real(ms_stft_result(i,j)) > max_m(i) || real(ms_stft_result(i,j)) < min_m(i)
            sta(i) = sta(i) + 1;
        end
    end

end


sta_x = 0;
for i=1:length(x1)
    if x1(i) > max_x || x1(i)<min_x
        sta(5) = sta(5) + 1;
    end
end
sta



k = 1:5:length(ms_stft_result(1,:));
figure;
subplot(2,1,1)
% plot(k,real(ms_stft_result(1,k)));
plot(k, log10(abs(ms_stft_result(1,k))) );
subplot(2,1,2)
plot(k,x1(k));



% for i=1:4
%     AAA = real(ms_stft_result(i,:));
%     subplot(2,2,i);
% 
%     plot(k,AAA(k));
% end
% 
% figure;
% plot(k,x(k));

% 进行后续的频域分析，如特征提取、阈值判断或与正常行为模型对比等，以识别潜在的攻击
% ...（此处省略具体实现细节，根据实际需求设计）

% 最终，通过分析MS-STFT结果，可以识别出异常的周期性模式，即潜在的网络攻击
