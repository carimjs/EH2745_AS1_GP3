format short g
clc
%%Assignment 1

%Written by : Cristhian Carim Jimenez

%% Base Values
S_base=1000; %unit [MVA]

%Values of Zone 1/BUS 1
V_base1=380; %unit [kV]
Z_base1= (V_base1^2)/S_base; %Unit Ohm
Y_base1 = 1/Z_base1; %unit Siemens (S)

%Values of Zone 6
V_base6=110; %unit [kV]
Z_base6= (V_base6^2)/S_base; %Unit Ohm
Y_base6 = 1/Z_base6;

%Values of Zone 3
V_base3=225; %unit [kV]
Z_base3= (V_base3^2)/S_base ;%unit [Ohm]
Y_base3 = 1/Z_base3;  %unit [S]

%% Parameters
%line parameters
Z_line1=1.935000 + i*34.200000;
Y_line1=0.0000675000+i*0.0000424115;

Z_line2=5.203000 +i*71.000000;
Y_line2=0.0001200000+i*0.0000200119;

%Transformer Parameters
Z_T1=(2.707692+i*14.518904);
Z_T2=(0.822800+i*11.138883);
Z_T3=(0.104711+i*5.843419);
%Shunt
Y_sh1=i*0.024793;
Y_sh2=7*10^(-6)+i*0.000346;
%% PER UNIT VALUES

%Transformers
Z_T1pu=Z_T1%/Z_base1;
Z_T2pu=Z_T2%/Z_base3; % el transformador 2 fue referido al lado del bus#3 225 kv
Z_T3pu=Z_T3%/Z_base6;

%Lines
Z_line_bc1pu=Z_line1%/Z_base3;
Y_line_bc1pu=Y_line1%/Y_base3;

Z_line_bc2pu=Z_line2%/Z_base3;
Y_line_bc2pu=Y_line2%/Y_base3;

%Shunt
Y_sh1_pu=0.3*i%Y_sh1/Y_base1;
Y_sh2_pu=0.001+i*0.05%Y_sh2/Y_base6;
%% Y matrix
Y11=(1/Z_T1pu)%+Y_sh1_pu;
Y66=(1/Z_T1pu)+(1/Z_T2pu)+(1/Z_T3pu)%+Y_sh2_pu;
Y33=(1/Z_T2pu)+0.5*Y_line_bc1pu+(1/Z_line_bc1pu)+(1/Z_line_bc2pu)+0.5*Y_line_bc2pu;
Y44=(1/Z_T3pu);
Y22=0.5*Y_line_bc1pu+(1/Z_line_bc1pu)+(1/Z_line_bc2pu)+0.5*Y_line_bc2pu;

Y16=-(1/Z_T1pu);
Y63=-(1/Z_T2pu);
Y23=-((1/Z_line_bc1pu)+(1/Z_line_bc2pu));
Y64=-(1/Z_T3pu);


Y_matrix=[Y11 0 0 0 Y16 ;
         0 Y22 Y23 0 0 ;
          0 Y23 Y33 0 Y63 ;
          0 0 0 Y44 Y64 ;
          Y16 0 Y63 Y64 Y66]