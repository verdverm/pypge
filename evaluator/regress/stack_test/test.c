#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "../levmar-2.6/levmar.h"
#include "../stack.h"

double low = -2;
double hgh =  2;
double step = 0.1;
int len = -1;



int sF1[] = {2,0,2,1,25,23,22,2,2,25,26,23,23,22};
int sF1_len = 14;
int sF1_c0[] = {3,1};  // ConstantF ~ 1 
int sF1_c0_len = 2;
int sF1_c1[] = {25};		// x
int sF1_c1_len = 1;
int sF1_c2[] = {25,26,23};  // x*y
int sF1_c2_len = 3;
double F1 (double *in) {
	return 1.0 + 2.0*in[0] + 3.0*in[0]*in[1];
}


// int sF1[] = {2,0,25,23,25,23,25,23,2,1,25,23,22,2,2,25,25,23,23,22};
// int sF1_len = 20;
// int sF1_c0[] = {25,25,23,25,23};  // x*x*x
// int sF1_c0_len = 5;
// int sF1_c1[] = {25};		// x
// int sF1_c1_len = 1;
// int sF1_c2[] = {25,26,23};  // x*y
// int sF1_c2_len = 3;
// double F1 (double in) {
// 	return 1.0*in*in*in + 2.0*in + 3.0*in*in;
// }


double* makeInput(int l, int h, double s) {
	double rng = h-l+s;
	len = (rng/s)+1;

	double* input = (double*) malloc(sizeof(double)*len);
	int i = 0;
	double curr = l;
	while( curr < h ) {
		input[i] = curr;
		curr += s;
		i++;
	}
	return input;
}
double* makeOutput( double* input, int len ) {
	double* out = (double*)malloc(sizeof(double)*len);

	int i;
	for( i=0; i<len; i++ )
		out[i] = F1(&input[i]);
	return out;
}

double* makeInput2d(int l, int h, double s) {
	double rng = h-l+s;
	len = (rng/s)+1;

	double* input = (double*) malloc(sizeof(double)*len*2);
	int i = 0;
	double curr = l;
	while( curr < h ) {
		input[i*2] = curr;
		input[i*2+1] = curr;
		curr += s;
		i++;
	}
	return input;
}
double* makeOutput2d( double* input, int len ) {
	double* out = (double*)malloc(sizeof(double)*len);

	int i;
	for( i=0; i<len; i++ )
		out[i] = F1(&input[i*2]);
	return out;
}


int main(int argc, char const *argv[])
{
	double* input = makeInput2d(low,hgh,step);
	double* output = makeOutput2d(input,len);
	
	int i;
	for( i=0; i<len; i++) {
		printf( "%d %f -> %f\n", i,input[i],output[i]); 
	}


	StackData sdata;
	sdata.x_len = len;
	sdata.x_dim = 2;
	sdata.x_data = input;
	sdata.expr.serial = sF1;
	sdata.expr.s_len = sF1_len;

	sdata.d_len = 3;
	sdata.derivs = (StackExpr*)malloc(sizeof(StackExpr)*sdata.d_len);
	sdata.derivs[0].serial = sF1_c0;
	sdata.derivs[0].s_len = sF1_c0_len;
	sdata.derivs[1].serial = sF1_c1;
	sdata.derivs[1].s_len = sF1_c1_len;
	sdata.derivs[2].serial = sF1_c2;
	sdata.derivs[2].s_len = sF1_c2_len;



	double *cs = (double*) malloc(sizeof(double)*3);




	cs[0] = 1;
	cs[1] = 1;
	cs[2] = 1;
	stack_levmar_der(output,cs,3,len,&sdata);
	// test_levmar_der(output,cs,3,len,input);
	printf( "deriv = %f %f %f\n", cs[0], cs[1], cs[2]);

	cs[0] = 1;
	cs[1] = 1;
	cs[2] = 1;
	stack_levmar_dif(output,cs,3,len,&sdata);
	// test_levmar_dif(output,cs,3,len,input);
	printf( "diff  = %f %f %f\n", cs[0], cs[1], cs[2]);

	free( sdata.derivs );
	free( cs );
	free( input );
	free( output );

	return 0;


}



	// cs[0] = 1;
	// cs[1] = 2;
	// cs[2] = 3;
	// for( i=0; i<1; i++) {
	// 	double out = pF1(input[i],cs);
	// 	// double out = dF1_c2(input[i],cs);
	// 	printf( "basic: %d %f -> %f  ~ %f\n", i,input[i],out,output[i]); 
	// 	double out2 = test_stack_eval(0,cs,&input[i],d_stack,sdata.expr);
	// 	// double out2 = test_stack_eval(0,cs,&input[i],d_stack,sdata.derivs[2]);
	// 	printf( "stack: %d %f -> %f  ~ %f\n\n", i,input[i],out2,output[i]); 
	// }
	// return 0;
