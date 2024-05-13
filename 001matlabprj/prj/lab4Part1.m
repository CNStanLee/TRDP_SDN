% --------------------------------- %
% Lab4 Part 1
% --------------------------------- %
clear;
close all;
clc;
%% 1.1.1
clear;
close all;
clc;
% --------------------------------- %
% 1 Parameter Define
% --------------------------------- %
fs = 8000;
note = 69;
d = 2;
start = 0;
% --------------------------------- %
% 2 Create a note
% --------------------------------- %
y = createNote(d, note, fs, start);
[Y, f] = my_FFT(y, fs);
figure(1);
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("Y vs f");
% --------------------------------- %
% 3 Observe note
% --------------------------------- %
note = 42;
y = createNote(d, note, fs, start);
[Y, f] = my_FFT(y, fs);
figure(2);
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("Y vs f");

f0 = 440*2^((110-69)/12);
fprintf("frequency of note 110 = %.2f\n", f0);
%% 1.1.2

clear;
close all;
clc;
% --------------------------------- %
% 1 Create Melody
% --------------------------------- %

d_vect = 0.5 .* ones(1, 4);
note_vect = [59, 80, 67, 90];
fs = 8000;
start_vect = 0 : 1 : 4;
music1 = createMusic(d_vect, note_vect, fs, start_vect);
[Y, f] = my_FFT(music1, fs);
figure(3);
plot(f, abs(Y));
xlabel("frequency f");
ylabel("Y");
title("DFT of music");




