clear;
clc;
close all;
% expected result
expected_output0 = -0.09556817;
expected_output1 = -0.13245907;
% the output of the finn core
original_output0 = 0;
original_output1 = -127; % input with all 127


% parameters
multiply_factor = 0.0002904795983340591;
add_bias = -0.09556816518306732;
% results
cal_res0 = (original_output0 * multiply_factor) + add_bias;
disp(cal_res0);
cal_res1 = (original_output1 * multiply_factor) + add_bias;
disp(cal_res1);


%%
clear;
clc;
close all;
cof = [0, 5, -7, -6, -3, 2, 0, 7, -1, 2];
input = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1];
%input = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

output = cof * input';

%%
% x + y = -393220
% 2x + y = -851976

x = 393220 - 851976;
y = -393220 - x;

z = 3*x + y;


% 3x + y = -1310732
%%
% x = -458756
% input 10*1
% x = f(input)
clear;
clc;
close all;

cof = [0, 5, -7, -6, -3, 2, 0, 7, -1, 2];

input_array1 = [127,127,127,127,127,127,127,127,127,127];
res1 = sim(input_array1);

input_array2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] .* 64;
res2 = sim(input_array2);

input_array3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] .* 32;
res3 = sim(input_array3);

input_array4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
res4 = sim(input_array4);

res5 = cof * input_array1';
res6 = cof * input_array2';
res7 = cof * input_array3';

function res = sim(input_array)
    k = 458756;
    bias = 65536;
    cof = [0, 5, -7, -6, -3, 2, 0, 7, -1, 2];
    res = cof * input_array' * k + bias;
end
