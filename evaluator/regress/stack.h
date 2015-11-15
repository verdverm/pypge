#ifndef PGE_STACK_H
#define PGE_STACK_H


typedef struct {
	int *serial;
	int  s_len;
} StackEqn;

typedef struct {
	int  x_len;
	int  x_dim;
	double *x_data;  // dim 0 == time

	StackEqn  eqn;
	StackEqn *derivs;
	int  d_len;
} StackData;


void stack_levmar_der(double* ygiven, double* p, int m, int n, void* data );
void stack_levmar_dif(double* ygiven, double* p, int m, int n, void* data );


#endif