#!/usr/bin/octave 

printf("Hello, apple!\n")

# lsode_options("integration method", "stiff")
# lsode_options()

# s1_0=5.8;
# s2_0=0.9;
# s3_0=0.2;
# s4_0=0.2;
# n2_0=0.1;
# a3_0=2.4;
# s5_0=0.1;

J0 = 3;           # mM/min
k1 = 100.0;       # /mM*min
k2 = 6.0;         # /mM*min
k3 = 16.0;        # /mM*min
k4 = 100.0;       # /mM*min
k5 = 1.28;        # /min
k6 = 12.0;        # /mM*min
k  = 1.3;         # /min
K  = 13.0;        # /min
q  = 4.0;
K1 = 0.52;        # mM
N  = 1.0;         # mM
A  = 4.0;         # mM
P  = 0.1;

function xdot = g(x,t)
	xdot = zeros(9,1);    # a column vector
	# vdot = zeros(NUMEQNS,1);    # a column vector

	J0 = 3;           # mM/min
	k1 = 100.0;       # /mM*min
	k2 = 6.0;         # /mM*min
	k3 = 16.0;        # /mM*min
	k4 = 100.0;       # /mM*min
	k5 = 1.28;        # /min
	k6 = 12.0;        # /mM*min
	k  = 1.3;         # /min
	K  = 13.0;        # /min
	q  = 4.0;
	K1 = 0.52;        # mM
	N  = 1.0;         # mM
	A  = 4.0;         # mM
	P  = 0.1;

	s1 = x(1);
	s2 = x(2);
	s3 = x(3);
	s4 = x(4);
	n2 = x(5);
	a3 = x(6);
	sX = x(7);

	a2 = A-a3;
	n1 = N-n2;
	Ja = K*(s4-sX);

	fA3=1+(a3/K1)^q;

	v1 = k1*s1*a3/fA3;
	v2 = k2*s2*n1;
	v3 = k3*s3*a2;
	v4 = k4*s4*n2;
	v5 = k5*a3;
	v6 = k6*s2*n2;
	v7 = k*sX;

	xdot(1)= J0 - v1;
	xdot(2)= 2*v1 - v2 - v6;
	xdot(3)= v2 - v3;
	xdot(4)= v3 - v4 - Ja;
	xdot(5)= v2 - v4 - v6;
	xdot(6)= -2*v1 + 2*v3 - v5;
	xdot(7)= P*Ja - v7;
	xdot(8)= a2;
	xdot(9)= n1;
endfunction

s1_0=1.2;
s2_0=0.2;
s3_0=0.05;
s4_0=0.11;
n2_0=0.08;
a3_0=2.5;
s5_0=0.078;
a2_0=A-a3_0;
n1_0=N-n2_0;
g0 = [s1_0, s2_0, s3_0, s4_0, n2_0, a3_0, s5_0, a2_0, n1_0]


# t = linspace (0,10.0,1000);
# y = lsode( "g", g0, t);

# # plot(t,y(:,1),'-',t,y(:,2),'-',t,y(:,3),'-',t,y(:,4),'-',t,y(:,5),'-',t,y(:,6),'-',t,y(:,7),'-')
# plot(t,y(:,1),'.',t,y(:,2),'.',t,y(:,3),'.',t,y(:,4),'.',t,y(:,5),'.',t,y(:,6),'.',t,y(:,7),'.')

# val = input("press any key to continue.");

function gen(numP, iCond, filename)
	printf("Generating %d points f\n", numP)
	t = linspace (0,10.0,numP);
	y = lsode( "g", iCond, t);

	printf("writing to file %s\n", filename)
	fid = fopen(filename, 'wt');
	fprintf(fid,"T\n");
	fprintf(fid,"          S1        S2        S3        S4        N2        A3        S5        A2        N1\n");
	for pnt = y
		fprintf(fid,"%.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f  %.6f\n", t, y);
	end
	fclose(fid);
	# plot(t,y(:,1),'.',t,y(:,2),'.',t,y(:,3),'.',t,y(:,4),'.',t,y(:,5),'.',t,y(:,6),'.',t,y(:,7),'.')
	printf("\n")
endfunction 

# gen(2000,g0,"yeast2000.txt");
# gen(20000,g0,"yeast20000.txt");
# gen(200000,g0,"yeast200000.txt");
gen(1000000,g0,"yeast1000000.txt");


printf("Goodbye!\n")

