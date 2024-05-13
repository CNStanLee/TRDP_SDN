function  ms_stft_result = ms_stft(feature, window_length, overlap_fraction, omega0, scale_vector)


% 定义所需参数
% 1. 波形基函数：这里使用Morlet小波作为示例
% omega0 = 6; % 中心频率（角频率）
wavelet = @(t) pi^(-0.25) * exp(1i*omega0*t) .* exp(-0.5*t.^2); % Morlet小波定义

% 2. 分析参数
% scale_vector = [1, 2, 4, 8]; % 多尺度参数a的选择
% scale_vector = 2.^(-(0:3));

% window_length = 20; % 窗口长度L
% overlap_fraction = 0.95; % 窗口重叠比例

% 3. 初始化STFT结果
num_scales = length(scale_vector);
ms_stft_result = zeros(num_scales, floor((length(feature) - window_length) / (window_length * (1 - overlap_fraction)) + 1));

% Morlet = morlet(-1,1,window_length);

% 对于每个尺度a，计算MS-STFT
for a_idx = 1:num_scales
    a = scale_vector(a_idx);
    Morlet = a^(-0.5)*wavelet(1/a.*(-window_length/2:window_length/2-1));
    
    for n = 1:(length(feature) - window_length) / (window_length * (1 - overlap_fraction)) + 1
        % 确定当前窗口位置
        start_idx = (n - 1) * window_length * (1 - overlap_fraction) + 1;
        end_idx = start_idx + window_length - 1;

        % 计算窗口内的数据
        window_x = feature(round(start_idx):round(end_idx));

        % 计算MS-STFT系数
        ms_stft_coefficient = sum(window_x  .* conj(Morlet),2);

        % ms_stft_coefficient = sum(window_x .* conj(a^(-0.5)*wavelet(1/a .* (0:window_length-1))), 2);

        % 存储MS-STFT结果
        ms_stft_result(a_idx, n) = ms_stft_coefficient;
    end
end