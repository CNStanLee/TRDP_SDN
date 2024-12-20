function [Data, Timestamp] = pcapDataRead(Packets, IP_src, IP_dst)

ipstr = str2double(split(IP_src, '.'));
ipdst = str2double(split(IP_dst, '.'));
% 
% data_len = length(Packets);

Data = {}; % 初始化为空 cell 数组
j = 1;
for i = 1:numel(Packets)
    ipstr_read = Packets(i).Packet(29:32);
    ipdst_read = Packets(i).Packet(33:36);

    if (all(ipstr_read == ipstr)) && (all(ipdst_read == ipdst))
        Data{j} = Packets(i).Packet(); % 使用 cell 数组
        Timestamp(j) = (Packets(i).Timestamp - Packets(1).Timestamp)/1000000;
        j = j+1;
    end
end


