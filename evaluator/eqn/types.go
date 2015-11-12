package eqn

type Eqn interface {
	Clone() Eqn

	Eval(t float64, x, c, s []float64) float64

	String() string
	PrettyPrint(dnames, snames []string, cvals []float64) string
	Latex(dnames, snames []string, cvals []float64) string
	Javascript(dnames, snames []string, cvals []float64) string
}

var (
	ZERO = NewConstantF(0.0)
	ONE  = NewConstantF(1.0)
)

type Leaf struct {
	Eqn
}

type Unary struct {
	Eqn
	C Eqn
}

type Binary struct {
	Eqn
	C1, C2 Eqn
}

type N_ary struct {
	Eqn
	CS []Eqn
}

// Leaf Nodes
type Time struct {
	Leaf
}

func NewTime() *Time {
	t := new(Time)
	return t
}
func (t *Time) Clone() Eqn { return NewTime() }

type Var struct {
	Leaf
	P int
}

func NewVar(i int) *Var {
	v := new(Var)
	v.P = i
	return v
}
func (v *Var) Clone() Eqn { return NewVar(v.P) }

type DVar struct {
	Leaf
	N int // dX_i
	//       ----
	D int // dX_j
	I int // index into the data to find this ratio (used in eval)
}

func NewDVar(n, d int) *DVar {
	dv := new(DVar)
	dv.N = n
	dv.D = d
	return dv
}
func (dv *DVar) Clone() Eqn { return NewDVar(dv.N, dv.D) }

type Constant struct {
	Leaf
	P int
}

func NewConstant(i int) *Constant {
	c := new(Constant)
	c.P = i
	return c
}
func (c *Constant) Clone() Eqn { return NewConstant(c.P) }

type ConstantF struct {
	Leaf
	F float64
}

func NewConstantF(f float64) *ConstantF {
	c := new(ConstantF)
	c.F = f
	return c
}
func (c *ConstantF) Clone() Eqn { return NewConstantF(c.F) }

type System struct {
	Leaf
	P int
}

func NewSystem(i int) *System {
	s := new(System)
	s.P = i
	return s
}
func (s *System) Clone() Eqn { return NewSystem(s.P) }

// Unary Operators
type Neg struct {
	Unary
}

func NewNeg(e Eqn) *Neg {
	n := new(Neg)
	n.C = e
	return n
}
func (u *Neg) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewNeg(C)
}

type Abs struct {
	Unary
}

func NewAbs(e Eqn) *Abs {
	n := new(Abs)
	n.C = e
	return n
}
func (u *Abs) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewAbs(C)
}

type Sqrt struct {
	Unary
}

func NewSqrt(e Eqn) *Sqrt {
	n := new(Sqrt)
	n.C = e
	return n
}
func (u *Sqrt) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewSqrt(C)
}

type Sin struct {
	Unary
}

func NewSin(e Eqn) *Sin {
	n := new(Sin)
	n.C = e
	return n
}
func (u *Sin) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewSin(C)
}

type Cos struct {
	Unary
}

func NewCos(e Eqn) *Cos {
	n := new(Cos)
	n.C = e
	return n
}
func (u *Cos) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewCos(C)
}

type Tan struct {
	Unary
}

func NewTan(e Eqn) *Tan {
	n := new(Tan)
	n.C = e
	return n
}
func (u *Tan) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewTan(C)
}

type Exp struct {
	Unary
}

func NewExp(e Eqn) *Exp {
	n := new(Exp)
	n.C = e
	return n
}
func (u *Exp) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewExp(C)
}

type Log struct {
	Unary
}

func NewLog(e Eqn) *Log {
	n := new(Log)
	n.C = e
	return n
}
func (u *Log) Clone() Eqn {
	var C Eqn
	if u.C != nil {
		C = u.C.Clone()
	}
	return NewLog(C)
}

// Hmmm... Operators
type PowI struct {
	Eqn
	// Unary
	Base  Eqn
	Power int
}

func NewPowI(e Eqn, i int) *PowI {
	n := new(PowI)
	if e != nil {
		n.Base = e.Clone()
	}
	n.Power = i
	return n
}
func (u *PowI) Clone() Eqn { return NewPowI(u.Base, u.Power) }

type PowF struct {
	Eqn
	// Unary
	Base  Eqn
	Power float64
}

func NewPowF(b Eqn, f float64) *PowF {
	n := new(PowF)
	n.Base = b
	n.Power = f
	return n
}
func (u *PowF) Clone() Eqn {
	var base Eqn
	if u.Base != nil {
		base = u.Base.Clone()
	}
	return NewPowF(base, u.Power)
}

type PowE struct {
	Eqn
	// Binary
	Base  Eqn
	Power Eqn
}

func NewPowE(b, p Eqn) *PowE {
	n := new(PowE)
	n.Base = b
	n.Power = p
	return n
}
func (n *PowE) Clone() Eqn {
	var base, pow Eqn
	if n.Base != nil {
		base = n.Base.Clone()
	}
	if n.Power != nil {
		pow = n.Power.Clone()
	}
	return NewPowE(base, pow)
}

type Div struct {
	Eqn
	// Binary
	Numer Eqn
	Denom Eqn
}

func NewDiv(n, d Eqn) *Div {
	D := new(Div)
	D.Numer = n
	D.Denom = d
	return D
}
func (n *Div) Clone() Eqn {
	var N, D Eqn
	if n.Numer != nil {
		N = n.Numer.Clone()
	}
	if n.Denom != nil {
		D = n.Denom.Clone()
	}
	return NewDiv(N, D)
}

// N-ary Operators
type Add struct {
	N_ary
}

func NewAdd() *Add {
	a := new(Add)
	a.CS = make([]Eqn, 0)
	return a
}

func (n *Add) Clone() Eqn {
	a := new(Add)
	a.CS = make([]Eqn, len(n.CS))
	for i, C := range n.CS {
		if C != nil {
			a.CS[i] = C.Clone()
		}
	}
	return a
}
func (a *Add) Insert(e Eqn) {
	a.CS = append(a.CS, e)
}

type Mul struct {
	N_ary
}

func NewMul() *Mul {
	m := new(Mul)
	m.CS = make([]Eqn, 0)
	return m
}
func (n *Mul) Clone() Eqn {
	a := NewMul()
	a.CS = make([]Eqn, len(n.CS))
	for i, C := range n.CS {
		if C != nil {
			a.CS[i] = C.Clone()
		}
	}
	return a
}
func (a *Mul) Insert(e Eqn) {
	a.CS = append(a.CS, e)
}
