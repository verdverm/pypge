#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "levmar-2.6/levmar.h"
#include "stack.h"


#define STACK_BUF_LEN 128


typedef struct {
	double data[STACK_BUF_LEN];
	int pos;
} D_Stack;

typedef struct {
	int data[STACK_BUF_LEN];
	int pos;
} I_Stack;

// typedef struct {
// 	double *data;
// 	int pos;
// } D_StackD;

// typedef struct {
// 	int *data;
// 	int pos;
// } I_StackD;

I_Stack* new_istack();
int push_istack(I_Stack* stack, int i);
void pop_istack(I_Stack* stack);
int  top_istack(I_Stack* stack);
int  len_istack(I_Stack* stack);
int  get_istack(I_Stack* stack, int pos);
int  is_empty_istack(I_Stack* stack);
void clear_istack(I_Stack* stack);
void free_istack(I_Stack* stack);

D_Stack* new_dstack();
int push_dstack(D_Stack* stack, double f);
void pop_dstack(D_Stack* stack);
double  top_dstack(D_Stack* stack);
int  len_dstack(D_Stack* stack);
double  get_dstack(D_Stack* stack, int pos);
int  is_empty_dstack(D_Stack* stack);
void clear_dstack(D_Stack* stack);
void free_dstack(D_Stack* stack);

I_Stack* new_istack() { 
	I_Stack* stack = (I_Stack*) malloc(sizeof(I_Stack));
	stack->pos = -1;
	return stack;
}
int push_istack(I_Stack* stack, int i) { 
	if (stack->pos +1 >= STACK_BUF_LEN)
		return 0;
	stack->pos++;
	stack->data[stack->pos] = i;
	return 1;
}
void pop_istack(I_Stack* stack) { 
	if (stack->pos >= 0) stack->pos--;
}
int  top_istack(I_Stack* stack) { 
	return stack->data[stack->pos];
}
int  len_istack(I_Stack* stack) { 
	return stack->pos + 1;
}
int  get_istack(I_Stack* stack, int pos) { 
	return stack->data[pos];
}
int  is_empty_istack(I_Stack* stack) { 
	return (stack->pos < 0) ? 1 : 0;
}
void clear_istack(I_Stack* stack) { 
	stack->pos = -1;
}
void free_istack(I_Stack* stack) { 
	free(stack);
}

D_Stack* new_dstack() { 
	D_Stack* stack = (D_Stack*) malloc(sizeof(D_Stack));
	stack->pos = -1;
	return stack;
}
int push_dstack(D_Stack* stack, double f) { 
	if (stack->pos +1 >= STACK_BUF_LEN)
		abort();
		// return 0;
	stack->pos++;
	stack->data[stack->pos] = f;
	return 1;
}
void pop_dstack(D_Stack* stack) { 
	if (stack->pos >= 0) stack->pos--;
}
double  top_dstack(D_Stack* stack) { 
	return stack->data[stack->pos];
}
int  len_dstack(D_Stack* stack) { 
	return stack->pos + 1;
}
double  get_dstack(D_Stack* stack, int pos) { 
	return stack->data[pos];
}
int  is_empty_dstack(D_Stack* stack) { 
	return (stack->pos < 0) ? 1 : 0;
}
void clear_dstack(D_Stack* stack) { 
	stack->pos = -1;
}
void free_dstack(D_Stack* stack) { 
	free(stack);
}








double stack_eval(double t, double *c_in, double *x_in, D_Stack *d_stack, StackEqn eqn );

void stack_func( double *p, double *x, int m, int n, void *data) {
	StackData *sdata = (StackData*)data;

	int x_dim = sdata->x_dim;
	double* x_data = sdata->x_data;
	D_Stack d_stack;
	// d_stack.clear();

	// printf( "HELLO from stack_func\n");


	int i;
	for( i=0; i < n; i++ ) {
		// printf( "%d %d %d\n",i,x_dim,sdata->x_len);
		x[i] = stack_eval(0,p,&(x_data[i*x_dim]),&d_stack,sdata->eqn);
	}

}

void stack_jacfunc( double *p, double *jac, int m, int n, void *data) {
	StackData *sdata = (StackData*)data;

	int x_dim = sdata->x_dim;
	double* x_data = sdata->x_data;
	D_Stack d_stack;
	// d_stack.clear();

	int i,j;
	for( i=0; i < n; i++ ) {
		for( j=0; j < m; j++ ) {
			jac[i*m+j] = stack_eval(0,p,&(x_data[i*x_dim]),&d_stack,sdata->derivs[j]);
		}
	}

}


void stack_levmar_der( double* ygiven, double* p, const int m, const int n, void* data ) {
  double opts[LM_OPTS_SZ], info[LM_INFO_SZ];

  // optimization control parameters; passing to levmar NULL instead of opts reverts to defaults
  opts[0]=LM_INIT_MU; opts[1]=1E-15; opts[2]=1E-15; opts[3]=1E-20;
  opts[4]=LM_DIFF_DELTA; // relevant only if the finite difference Jacobian version is used

  // invoke the optimization function
  dlevmar_der(stack_func, stack_jacfunc, p, ygiven, m, n, 1000, opts, info, NULL, NULL, data); // with analytic Jacobian
}

void stack_levmar_dif( double* ygiven, double* p, const int m, const int n, void* data ) {
  double opts[LM_OPTS_SZ], info[LM_INFO_SZ];

  // printf( "HELLO from stack_levmar_dif\n");
	StackData *sdata = (StackData*)data;

	int x_dim = sdata->x_dim;
	int x_len = sdata->x_len;
	// printf( "x_len: %d   x_dim: %d\n",x_len,x_dim);

  // optimization control parameters; passing to levmar NULL instead of opts reverts to defaults
  opts[0]=LM_INIT_MU; opts[1]=1E-15; opts[2]=1E-15; opts[3]=1E-20;
  opts[4]=LM_DIFF_DELTA; // relevant only if the finite difference Jacobian version is used

  // invoke the optimization function
  dlevmar_dif(stack_func, p, ygiven, m, n, 1000, opts, info, NULL, NULL, data); // without Jacobian
}


/*
ExprTypes:
---------------
NULL:      0
STARTLEAF: 1
CONSTANT:  2
TIME:      4
SYSTEM:    5
VAR:       6
LASTLEAF:  7
STARTFUNC: 8
NEG:       9
ABS:       10
SQRT:      11
SIN:       12
COS:       13
TAN:       14
EXP:       15
LASTFUNC:  17
POWI:      18
POWF:      19
POWE:      20
DIV:       21
ADD:       22
MUL:       23
EXPR_MAX:  24
STARTVAR:  25
*/


// #define print_stack_eval 1

double stack_eval(double t, double *c_in, double *x_in, D_Stack *d_stack, StackEqn eqn ) {

	// I_Stack *serial = new_istack();
	// I_Stack istack;
	// I_Stack *serial = &istack;

	clear_dstack(d_stack);
	int* serial = eqn.serial;

	
	#ifdef print_stack_eval
	printf("Serial: |%d|", eqn.s_len);
	#endif
	int s;
	for( s=0; s < eqn.s_len; s++ ) {
	// #ifdef print_stack_eval
	// 	printf( "%d ", eqn.serial[s]);
	// #endif
	// 	push_istack(serial,eqn.serial[eqn.s_len-s-1]);
	// }
	// #ifdef print_stack_eval
	// printf("\n");
	// #endif
	
	// clear_dstack(d_stack);

	// // fill i_stack with cmds and d_stack with leaves
	// while ( !is_empty_istack(serial) ) {
	// 	// printf( "processing serial\n");
		// int val = top_istack(serial);
		// pop_istack(serial);

		int val = serial[s];

	#ifdef print_stack_eval
		int dlen = len_dstack(d_stack);
		int slen = len_istack(serial);
		printf( "S: %d    val:  %d   \n", slen, val );
		printf( "serial(%d): [ ", slen); 
		for( i=0; i < slen; i++ )
			printf( "%d ", get_istack(serial,i) );
		printf(" ]\n");
		printf( "d_stack(%d): [ ", dlen); 
		for( i=0; i < dlen; i++ )
			printf( "%.2f ", get_dstack(d_stack,i) );
		printf(" ]\n");
	#endif

		switch (val) {
			
			// CONSTANT:  2
			case 2: {
				s++;
				int p = serial[s];
				// int p = top_istack(serial);
				// pop_istack(serial);
				push_dstack(d_stack,c_in[p]);
			}
				break; 

			// HACK***
			// CONSTANTF:  3
			case 3: {
				s++;
				int p = serial[s];
				// int p = top_istack(serial);
				// pop_istack(serial);
				push_dstack(d_stack,p);
			}
				break; 
			// TIME:      4
			case 4:
				push_dstack(d_stack,t);
				break;
			// SYSTEM:    5
			// case 5:
				// s++;
				// push_dstack(d_stack,sys_in[serial[s]]);
			// VAR:       6   should already be transformed, but just in case
			case 6: {
				s++;
				int p = serial[s];
				// int p = top_istack(serial);
				// pop_istack(serial);
				push_dstack(d_stack,x_in[p]);
				break;
			}
			// NEG:       9
			case 9: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, -top);
			}
				break;
			// ABS:       10
			case 10: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, fabs(top));
			}
				break;
			// SQRT:      11
			case 11: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, sqrt(top));
			}
				break;
			// SIN:       12
			case 12: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, sin(top));
			}
				break;
			// COS:       13
			case 13: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, cos(top));
			}
				break;
			// TAN:       14
			case 14: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, tan(top));
			}
				break;
			// EXP:       15
			case 15: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, exp(top));
			}
				break;
			// LOG:       16
			case 16: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				push_dstack(d_stack, log(top));
			}
				break;

						// POWI:      18
			case 18: {
				double top = top_dstack(d_stack);
				pop_dstack(d_stack);
				s++;
				int pwr = serial[s];
				// int pwr = top_istack(serial);
				// pop_istack(serial);
				push_dstack(d_stack, pow(top,pwr));
			}
				break;
			// POWE:      20
			case 20: {
					double top = top_dstack(d_stack);
					pop_dstack(d_stack);
					double pwr = top_dstack(d_stack);
					pop_dstack(d_stack);
					push_dstack(d_stack, pow(top,pwr));
				}
				break;
			// DIV:       21
			case 21: {
					double denom = top_dstack(d_stack);
					pop_dstack(d_stack);
					double numer = top_dstack(d_stack);
					pop_dstack(d_stack);
					push_dstack(d_stack, numer / denom);
				}
				break;
			// ADD:       22
			case 22: {
					double lhs = top_dstack(d_stack);
					pop_dstack(d_stack);
					double rhs = top_dstack(d_stack);
					pop_dstack(d_stack);
					push_dstack(d_stack, lhs + rhs);
					// printf( "%f + %f = %f\n", lhs, rhs, top_dstack(d_stack));
				}
				break;
			// MUL:       23
			case 23: {
					double lhs = top_dstack(d_stack);
					pop_dstack(d_stack);
					double rhs = top_dstack(d_stack);
					pop_dstack(d_stack);
					push_dstack(d_stack, lhs * rhs);
					// printf( "%f * %f = %f\n", lhs, rhs, top_dstack(d_stack));
				}
				break;




			case 0:
			default:
				// STARTVAR:  25
				if (val >= 25) {
					push_dstack(d_stack,x_in[val-25]); // x_dim_of_var = val - STARTVAR
				} else {
					printf("pushing unknown cmd %d\n", val);
					int s;
					for( s=0; s < eqn.s_len; s++ ) {
						printf( "%d ", eqn.serial[s]);
					}
					printf( "\n");
					abort();
				}
		}

	#ifdef print_stack_eval
		dlen = len_dstack(d_stack);
		printf( "S: %d val: %d\n", s, val);
		printf( "d_stack(%d): [ ", dlen); 
		for( i=0; i < dlen; i++ )
			printf( "%.2f ", get_dstack(d_stack,i) );
		printf(" ]\n\n");
	#endif
	}

	// free(serial);
	return top_dstack(d_stack);

}


