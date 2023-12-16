%% import data
data = load('data.txt');

len = size(data);
len = len(1);

%% x-position plot
figure(1)
t = 1:1:len;
plot(t, data(:,1));

%% x-velocty plot
figure(2)
plot(t, data(:, 3));