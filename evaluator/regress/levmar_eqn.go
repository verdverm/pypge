package regress

// #cgo CFLAGS: -ggdb -fPIC -m64 -pthread
// #cgo LDFLAGS: /home/tony/gocode/src/github.com/verdverm/pypge/evaluator/regress/levmar-2.6/liblevmar.a -lf2c -llapack -lblas -lm
// #include "levmar_h.h"
import "C"

import (
	// "fmt"
	"github.com/verdverm/pypge/evaluator/eqn"
	"reflect"
	"unsafe"
)

type callback_eqn_data struct {
	Input  [][]float64
	Output []float64

	Eqn   eqn.Eqn
	Jac   []eqn.Eqn
	Coeff []float64
}

func levmarEqn(e eqn.Eqn, jac []eqn.Eqn, guess []float64, in [][]float64, out []float64) (coeff, info []float64) {
	var cd callback_eqn_data
	coeff = make([]float64, len(guess))
	copy(coeff, guess)

	cd.Input = in
	cd.Output = out
	cd.Eqn = e
	cd.Coeff = coeff
	cd.Jac = jac

	// c/levmar inputs
	c_coeff := make([]C.double, len(guess))
	for i, g := range guess {
		c_coeff[i] = C.double(g)
	}

	y := make([]C.double, len(out))
	for i, pnt := range out {
		y[i] = C.double(pnt)
	}
	ca := (*C.double)(unsafe.Pointer(&c_coeff[0]))
	mi := C.int(len(c_coeff))

	ya := (*C.double)(unsafe.Pointer(&y[0]))
	ni := C.int(len(out))

	c_info := make([]C.double, LM_INFO_SZ)
	ia := (*C.double)(unsafe.Pointer(&c_info[0]))

	// C.levmar_eqn_dif(ya, ca, mi, ni, unsafe.Pointer(&cd))
	C.levmar_eqn_der(ya, ca, mi, ni, ia, unsafe.Pointer(&cd))

	for i, _ := range c_coeff {
		coeff[i] = float64(c_coeff[i])
	}

	info = make([]float64, LM_INFO_SZ)
	for i, _ := range c_info {
		info[i] = float64(c_info[i])
	}
	return coeff, info
}

func callbackEqn_func(p, x *C.double, e unsafe.Pointer) {
	cd := *(*callback_eqn_data)(e)

	in_len := len(cd.Input)
	co_len := len(cd.Coeff)
	x_size := in_len

	var p_go []C.double
	p_head := (*reflect.SliceHeader)((unsafe.Pointer(&p_go)))
	p_head.Cap = co_len
	p_head.Len = co_len
	p_head.Data = uintptr(unsafe.Pointer(p))
	for i, _ := range p_go {
		cd.Coeff[i] = float64(p_go[i])
	}

	var x_go []C.double
	x_head := (*reflect.SliceHeader)((unsafe.Pointer(&x_go)))
	x_head.Cap = x_size
	x_head.Len = x_size
	x_head.Data = uintptr(unsafe.Pointer(x))

	var out float64
	for i, input := range cd.Input {
		out = cd.Eqn.Eval(0, input, cd.Coeff, nil)
		x_go[i] = C.double(out)
	}
}

func callbackEqn_jacfunc(p, x *C.double, e unsafe.Pointer) {
	cd := *(*callback_eqn_data)(e)

	in_len := len(cd.Input)
	co_len := len(cd.Coeff)
	x_size := in_len * co_len

	var p_go []C.double
	p_head := (*reflect.SliceHeader)((unsafe.Pointer(&p_go)))
	p_head.Cap = co_len
	p_head.Len = co_len
	p_head.Data = uintptr(unsafe.Pointer(p))
	for i, _ := range p_go {
		cd.Coeff[i] = float64(p_go[i])
	}

	var x_go []C.double
	x_head := (*reflect.SliceHeader)((unsafe.Pointer(&x_go)))
	x_head.Cap = x_size
	x_head.Len = x_size
	x_head.Data = uintptr(unsafe.Pointer(x))

	var out float64
	for i1, input := range cd.Input {
		for i2, jac := range cd.Jac {
			i := i1*co_len + i2
			out = jac.Eval(0, input, cd.Coeff, nil)
			x_go[i] = C.double(out)
		}
	}

}
