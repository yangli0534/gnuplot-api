
%format long
clc
clear all;
close all;

config = lteTestModel('3.1', '5MHz');  % Test Model 1.1, 5MHz bandwidth
config.TotSubframes = 100;             % Generate 100 subframes
[timeDomainSig, txGrid, txInfo] = lteTestModelTool(config);


% % Calculate the spectral content in the LTE signal
% spectrumPlotTx = dsp.SpectrumAnalyzer;
% spectrumPlotTx.SampleRate = config.SamplingRate;
% spectrumPlotTx.SpectrumType = 'Power density';
% spectrumPlotTx.PowerUnits =  'dBm';
% spectrumPlotTx.RBWSource = 'Property';
% spectrumPlotTx.RBW = 15e3;
% spectrumPlotTx.FrequencySpan = 'Span and center frequency';
% spectrumPlotTx.Span = 7.68e6;
% spectrumPlotTx.CenterFrequency = 0;
% spectrumPlotTx.Window = 'Rectangular';
% spectrumPlotTx.SpectralAverages = 10;
% spectrumPlotTx.YLimits = [-100 -60];
% spectrumPlotTx.YLabel = 'PSD';
% spectrumPlotTx.Title = 'Test Model E-TM1.1, 5 MHz Signal Spectrum';
% spectrumPlotTx.ShowLegend = false;
% spectrumPlotTx(waveform);
%  

%hPlotDLResourceGrid(txInfo, txGrid);
% Compute spectrogram
[y,f,t,p] = spectrogram(timeDomainSig, 512, 0, 512, txInfo.SamplingRate);

% Re-arrange frequency axis and spectrogram to put zero frequency in the
% middle of the axis i.e. represent as a complex baseband waveform
f = (f-txInfo.SamplingRate/2)/1e6;
p = fftshift(10*log10(abs(p)));

% Plot spectrogram
figure;
surf(t*1000,f,p,'EdgeColor','none');
xlabel('Time (ms)');
ylabel('Frequency (MHz)');
zlabel('Power (dB)');
title(sprintf('Spectrogram of Test Model E-TM%s, %s',txInfo.TMN, txInfo.BW));
%% Generate an Over-the-Air Signal Using an RF Signal Generator
% The Instrument Control Toolbox is used to download and play the test
% model waveform created by the LTE Toolbox, |waveform|, using the Keysight
% Technologies N5172B signal generator. This creates an RF LTE signal with
% a center frequency of 1GHz. Note 1GHz was selected as an example
% frequency and is not intended to be a recognized LTE channel.

% Download the baseband IQ waveform to the instrument. Generate the RF 
% signal at a center frequency of 1GHz and output power of 0dBm.
power = -20;       % Output power
loopCount = Inf; % Number of times to loop
    
% % Configure the signal generator, download the waveform and loop
% rf = rfsiggen('TCPIP0::172.16.1.41::inst0::INSTR');
% download(rf,waveform.',config.SamplingRate); 
% start(rf,3e9,power,loopCount);
% 
% %stop(rf);
% disconnect(rf);
% clear rf;

% gen waveform file
timeDomainSig = timeDomainSig';
maximum = max( [ real( timeDomainSig) imag( timeDomainSig ) ] );
timeDomainSig = 0.7 * timeDomainSig / maximum;

timeDomainSig = [real(timeDomainSig);imag(timeDomainSig)]; % get the real and imaginary parts
timeDomainSig = timeDomainSig(:)';    % transpose and interleave the waveform

filename = strcat('LTE_',txInfo.DuplexMode,'_', txInfo.BW, '_TM',txInfo.TMN,'_fs',num2str(txInfo.SamplingRate),'_NDLRB',num2str(txInfo.NDLRB),'.txt')
fid = fopen(filename, 'w');
fprintf(fid, '%d\n', txInfo.SamplingRate);
for i = 1:length(timeDomainSig)
    fprintf(fid, '%d\n', timeDomainSig(i));
end
fclose(fid);
