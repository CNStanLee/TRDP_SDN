% --------------------------------- %
% Lab4 Part 2
% --------------------------------- %
clear;
close all;
clc;
% --------------------------------- %
% create signal
% --------------------------------- %

d_vect = 0.5 .* ones(1, 4);
note_vect = [25, 107, 25, 107];
fs = 8000;
start_vect = 0 : 1 : 4;
music1 = createMusic(d_vect, note_vect, fs, start_vect);
[Y, f] = my_FFT(music1, fs);
figure(3);
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of music");

%sound(music1, fs);

% --------------------------------- %
% create ideal filter
% --------------------------------- %
% 
FL = length(f);
HLP = zeros(FL, 1);


fsize = FL / fs;
HLP(FL / 2 - 250 * fsize : FL / 2 + 250 * fsize, 1) = 1;
HHP(:, 1) = ~ HLP(:, 1);

%HLP(FL / 2 - 1000 : FL / 2 + 1000, 1) = 1;
%HHP = zeros(length(f), 1);
%HHP(:, 1) = ~ HLP(:, 1);

figure;
plot(f, HLP);
figure;
plot(f, HHP);

% --------------------------------- %
% apply ideal HLP filter
% --------------------------------- %

Y_HLP = Y .* HLP;

figure;
plot(f, abs(Y_HLP));
xlabel("frequency f");
ylabel("Y HLP");
title("DFT of HLP music");

y_hlp = my_FFTinv(Y_HLP);
%sound(abs(y_hlp), fs);

% --------------------------------- %
% apply ideal HHP filter
% --------------------------------- %

Y_HHP = Y .* HHP;

figure;
plot(f, abs(Y_HHP));
xlabel("frequency f");
ylabel("Y HHP");
title("DFT of HHP music");

y_hhp = my_FFTinv(Y_HHP);
%sound(abs(y_hhp), fs);

%% 1.2.2 Separate wto ources

clear;
close all;
clc;

% --------------------------------- %
% create signal x1
% --------------------------------- %

d_vect = ones(1, 10);
note_vect = 51: 1 : 60;
fs = 8000;
start_vect = 0 : 1 : 9;
x1 = createMusic(d_vect, note_vect, fs, start_vect);
[Y, f] = my_FFT(x1, fs);
Yx1 = Y;

t = 0 : 1 / fs : 10 - 1 / fs; 
figure;
plot(t, x1);

figure;
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of x1");

%sound(x1, fs);

% --------------------------------- %
% create signal x2
% --------------------------------- %

d_vect = ones(1, 10);
note_vect = 72: 1 : 81;
fs = 8000;
start_vect = 0 : 1 : 9;
x2 = createMusic(d_vect, note_vect, fs, start_vect);
[Y, f] = my_FFT(x2, fs);
Yx2 = Y;

t = 0 : 1 / fs : 10 - 1 / fs; 
figure;
plot(t, x2);

figure;
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of x2");

%sound(music1, fs);

% --------------------------------- %
% create signal x1 + x2
% --------------------------------- %

x = x1 + x2;
[Y, f] = my_FFT(x, fs);

t = 0 : 1 / fs : 10 - 1 / fs; 
figure;
plot(t, x);

figure;
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of x");

% --------------------------------- %
% create ideal filter
% --------------------------------- %
% 
FL = length(f);
HLP = zeros(FL, 1);
HLP(FL / 2 - 4000 : FL / 2 + 4000, 1) = 1;
%HHP = zeros(length(f), 1);
HHP(:, 1) = ~ HLP(:, 1);


% --------------------------------- %
% reconstruct y1 and y2 with the filter
% --------------------------------- %

Y_HLP = Y .* HLP;
Yy1 = Y_HLP;
Y_HHP = Y .* HHP;
Yy2 = Y_HHP;

figure;
plot(f, abs(Y_HLP));
xlabel("frequency f");
ylabel("Y");
title("DFT of y1");
figure;
plot(f, abs(Y_HHP));
xlabel("frequency f");
ylabel("Y");
title("DFT of y2");

y1 = my_FFTinv(Y_HLP);
y2 = my_FFTinv(Y_HHP);

figure;
plot(t, y1);

figure;
plot(t, y2);

%sound(abs(y1), fs);
%%
% --------------------------------- %
% calculate Euclidean distance 
% --------------------------------- %

d1 = sqrt(sum((y1 - x1).^2)); % Euclidean distance
d2 = sqrt(sum((y2 - x2).^2)); % Euclidean distance

fprintf("d1 = %4f\r", d1);

fprintf("d2 = %4f\r", d2);

%%

figure;

subplot(4, 1, 1);
plot(f, Yx1);
xlabel("frequency f");
ylabel("Y");
title("DFT of x1");

subplot(4, 1, 2);
plot(f, Yx2);
xlabel("frequency f");
ylabel("Y");
title("DFT of x2");

subplot(4, 1, 3);
plot(f, Yy1);
xlabel("frequency f");
ylabel("Y");
title("DFT of y1");

subplot(4, 1, 4);
plot(f, Yy2);
xlabel("frequency f");
ylabel("Y");
title("DFT of y2");

sgtitle("Compare x1, x2, y1, y2");


%%

clear;
close all;
clc;

[y, fs] = audioread("melody2.wav");
[Y, f] = my_FFT(y, fs);

t = 0 : 1 / fs : 22 - 1 / fs; 

figure;
plot(t, y);
xlabel("time t");
ylabel("A");
title("music2");


figure;
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of music2");

% sound(y(1 : (fs * 20), 1), fs);

% really love this song :)

% --------------------------------- %
% filter
% --------------------------------- %

FL = length(f);
HLP = zeros(FL, 1);
fsize = FL / fs;
HLP(FL / 2 - 70 * fsize : FL / 2 + 70 * fsize, 1) = 1;
HHP(:, 1) = ~ HLP(:, 1);

Y_HLP = Y .* HLP;
Y_HHP = Y .* HHP;

figure;
plot(f, Y_HLP);
xlabel("frequency f");
ylabel("Y");
title("DFT of Y HLP");

y_hlp = my_FFTinv(Y_HLP);
sound(abs(y_hlp), fs);

%% 1.3
clear;
close all;
clc;



