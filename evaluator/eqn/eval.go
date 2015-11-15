package eqn

import (
	"math"
)

func (*Time) Eval(t float64, x, c, s []float64) float64 { return t }

func (v *Var) Eval(t float64, x, c, s []float64) float64 { return x[v.P] }

func (dv *DVar) Eval(t float64, x, c, s []float64) float64 { return x[dv.I] }

func (cnst *Constant) Eval(t float64, x, c, s []float64) float64 { return c[cnst.P] }

func (cnst *ConstantF) Eval(t float64, x, c, s []float64) float64 { return cnst.F }

func (sys *System) Eval(t float64, x, c, s []float64) float64 { return s[sys.P] }

func (u *Neg) Eval(t float64, x, c, s []float64) float64 {
	return -1. * u.C.Eval(t, x, c, s)
}

func (u *Abs) Eval(t float64, x, c, s []float64) float64 {
	return math.Abs(u.C.Eval(t, x, c, s))
}

func (u *Sqrt) Eval(t float64, x, c, s []float64) float64 {
	return math.Sqrt(u.C.Eval(t, x, c, s))
}

func (u *Sin) Eval(t float64, x, c, s []float64) float64 {
	return math.Sin(u.C.Eval(t, x, c, s))
}

func (u *Cos) Eval(t float64, x, c, s []float64) float64 {
	return math.Cos(u.C.Eval(t, x, c, s))
}

func (u *Tan) Eval(t float64, x, c, s []float64) float64 {
	return math.Tan(u.C.Eval(t, x, c, s))
}

func (u *Exp) Eval(t float64, x, c, s []float64) float64 {
	return math.Exp(u.C.Eval(t, x, c, s))
}

func (u *Log) Eval(t float64, x, c, s []float64) float64 {
	return math.Log1p(u.C.Eval(t, x, c, s))
}

func (u *PowI) Eval(t float64, x, c, s []float64) float64 {
	return math.Pow(u.Base.Eval(t, x, c, s), float64(u.Power))
}

func (u *PowF) Eval(t float64, x, c, s []float64) float64 {
	return math.Pow(u.Base.Eval(t, x, c, s), u.Power)
}

func (n *PowE) Eval(t float64, x, c, s []float64) float64 {
	return math.Pow(n.Base.Eval(t, x, c, s), n.Power.Eval(t, x, c, s))
}

func (n *Div) Eval(t float64, x, c, s []float64) float64 {
	return n.Numer.Eval(t, x, c, s) / n.Denom.Eval(t, x, c, s)
}

func (n *Add) Eval(t float64, x, c, s []float64) float64 {
	ret := 0.0
	for _, C := range n.CS {
		if C == nil {
			continue
		}
		ret += C.Eval(t, x, c, s)
	}
	return ret
}

func (n *Mul) Eval(t float64, x, c, s []float64) float64 {
	ret := 1.0
	for _, C := range n.CS {
		if C == nil {
			continue
		}
		ret *= C.Eval(t, x, c, s)
	}
	return ret
}

// x_out is the return here, pass in so we don't have to allocate each time
func RK4(e []Eqn, c [][]float64, s []float64, ti, tj float64, x_in, x_tmp, x_out []float64) {
	var k [32][4]float64 // that 32 seems pretty arbitrary... XXX TODO
	L := len(e)
	h := tj - ti
	for i := 0; i < L; i++ {
		k[i][0] = e[i].Eval(ti, x_in, c[i], s)
	}
	for i := 0; i < L; i++ {
		x_tmp[i] = x_in[i] + (h * k[i][0] / 2.0)
	}
	for i := 0; i < L; i++ {
		k[i][1] = e[i].Eval(ti, x_tmp, c[i], s)
	}
	for i := 0; i < L; i++ {
		x_tmp[i] = x_in[i] + (h * k[i][1] / 2.0)
	}
	for i := 0; i < L; i++ {
		k[i][2] = e[i].Eval(ti, x_tmp, c[i], s)
	}
	for i := 0; i < L; i++ {
		x_tmp[i] = x_in[i] + (h * k[i][2])
	}
	for i := 0; i < L; i++ {
		k[i][3] = e[i].Eval(ti, x_tmp, c[i], s)
	}
	for i := 0; i < L; i++ {
		x_out[i] = ((k[i][0] + 2.0*k[i][1] + 2.0*k[i][2] + k[i][3]) * (h / 6.0))
	}

	return
}

func PRK4(xn int, e Eqn, c, s []float64, ti, tj float64, x_in, x_out, x_tmp []float64) float64 {
	var k [4]float64
	L := len(x_in)
	h := tj - ti
	for i := 0; i < L; i++ {
		mid := (0.5 * (x_out[i] - x_in[i]))
		x_tmp[i] = x_in[i] + mid
	}
	k[0] = e.Eval(ti, x_in, c, s)
	x_tmp[xn] = x_in[xn] + (h * k[0] / 2.0)
	k[1] = e.Eval(ti, x_tmp, c, s)
	x_tmp[xn] = x_in[xn] + (h * k[1] / 2.0)
	k[2] = e.Eval(ti, x_tmp, c, s)
	x_tmp[xn] = x_in[xn] + (h * k[2])
	k[3] = e.Eval(ti, x_tmp, c, s)
	return ((k[0] + 2.0*k[1] + 2.0*k[2] + k[3]) * (h / 6.0))
}

// func PrintPRK4(xn int, e Eqn, ti, to float64, x_in, x_out, x_tmp, c, s []float64) float64 {
// 	var k [4]float64
// 	L := len(x_in)
// 	h := to - ti
// 	for i := 0; i < L; i++ {
// 		x_tmp[i] = x_in[i] + (0.5 * (x_out[i] - x_in[i]))
// 	}
// 	fmt.Printf("in:   %v\n", x_in)
// 	fmt.Printf("out:  %v\n", x_out)

// 	fmt.Printf("tmp:  %v\n", x_tmp)
// 	k[0] = e.Eval(ti, x_in, c, s)
// 	x_tmp[xn] = x_in[xn] + (h * k[0] / 2.0)
// 	fmt.Printf("tmp:  %v\n", x_tmp)
// 	k[1] = e.Eval(ti, x_tmp, c, s)
// 	x_tmp[xn] = x_in[xn] + (h * k[1] / 2.0)
// 	fmt.Printf("tmp:  %v\n", x_tmp)
// 	k[2] = e.Eval(ti, x_tmp, c, s)
// 	x_tmp[xn] = x_in[xn] + (h * k[2])
// 	fmt.Printf("tmp:  %v\n", x_tmp)
// 	k[3] = e.Eval(ti, x_tmp, c, s)
// 	fmt.Printf("k:    %v\n", k)
// 	ans := ((k[0] + 2.0*k[1] + 2.0*k[2] + k[3]) * (h / 6.0))
// 	fmt.Printf("ans:  %.4f   =>   %.4f\n\n", ans, x_out[xn]-x_in[xn])
// 	return ans
// }
