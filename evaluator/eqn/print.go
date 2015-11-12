package eqn

import "fmt"

func (n *Time) String() string                                              { return "T" }
func (t *Time) PrettyPrint(dnames, snames []string, cvals []float64) string { return "T" }
func (t *Time) Latex(dnames, snames []string, cvals []float64) string       { return "T" }
func (t *Time) Javascript(dnames, snames []string, cvals []float64) string  { return "T" }

func (v *Var) String() string { return "X_" + fmt.Sprint(v.P) }
func (v *Var) PrettyPrint(dnames, snames []string, cvals []float64) string {
	if dnames == nil {
		return v.String()
	}
	return dnames[v.P]
}
func (v *Var) Latex(dnames, snames []string, cvals []float64) string {
	return v.PrettyPrint(dnames, snames, cvals)
}
func (v *Var) Javascript(dnames, snames []string, cvals []float64) string {
	return v.PrettyPrint(dnames, snames, cvals)
}

func (dv *DVar) String() string {
	return fmt.Sprintf("dX_%d_%d", dv.N, dv.D)
}
func (dv *DVar) PrettyPrint(dnames, snames []string, cvals []float64) string {
	if dnames == nil {
		return dv.String()
	}
	return fmt.Sprintf("d%s_d%s", dnames[dv.N], dnames[dv.D])
}
func (dv *DVar) Latex(dnames, snames []string, cvals []float64) string {
	return dv.PrettyPrint(dnames, snames, cvals)
}
func (dv *DVar) Javascript(dnames, snames []string, cvals []float64) string {
	return dv.PrettyPrint(dnames, snames, cvals)
}

func (c *Constant) String() string { return "C_" + fmt.Sprint(c.P) }
func (c *Constant) PrettyPrint(dnames, snames []string, cvals []float64) string {
	if cvals == nil {
		return c.String()
	}
	return fmt.Sprintf("%.6f", cvals[c.P])
}
func (c *Constant) Latex(dnames, snames []string, cvals []float64) string {
	return c.PrettyPrint(dnames, snames, cvals)
}
func (c *Constant) Javascript(dnames, snames []string, cvals []float64) string {
	return c.PrettyPrint(dnames, snames, cvals)
}

func (c *ConstantF) String() string { return fmt.Sprintf("%.4e", c.F) }
func (c *ConstantF) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return c.String()
}
func (c *ConstantF) Latex(dnames, snames []string, cvals []float64) string {
	return fmt.Sprintf("%.2f", c.F)
}
func (c *ConstantF) Javascript(dnames, snames []string, cvals []float64) string {
	return fmt.Sprintf("%.2f", c.F)
}

func (s *System) String() string { return "S_" + fmt.Sprint(s.P) }
func (s *System) PrettyPrint(dnames, snames []string, cvals []float64) string {
	if snames == nil {
		return s.String()
	}
	return snames[s.P]
}
func (s *System) Latex(dnames, snames []string, cvals []float64) string {
	return s.PrettyPrint(dnames, snames, cvals)
}
func (s *System) Javascript(dnames, snames []string, cvals []float64) string {
	return s.PrettyPrint(dnames, snames, cvals)
}

func (u *Neg) String() string {
	if u.C == nil {
		return "-(nil)"
	}
	return "-(" + u.C.String() + ")"
}
func (u *Neg) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "-(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Neg) Latex(dnames, snames []string, cvals []float64) string {
	return "-(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Neg) Javascript(dnames, snames []string, cvals []float64) string {
	return "-(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Abs) String() string {
	if u.C == nil {
		return "abs(nil)"
	}
	return "abs(" + u.C.String() + ")"
}
func (u *Abs) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "abs(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Abs) Latex(dnames, snames []string, cvals []float64) string {
	return "abs(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Abs) Javascript(dnames, snames []string, cvals []float64) string {
	return "abs(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Sqrt) String() string {
	if u.C == nil {
		return "sqrt(nil)"
	}
	return "sqrt(" + u.C.String() + ")"
}
func (u *Sqrt) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "sqrt(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Sqrt) Latex(dnames, snames []string, cvals []float64) string {
	return "\\sqrt{" + u.C.Latex(dnames, snames, cvals) + "}"
}
func (u *Sqrt) Javascript(dnames, snames []string, cvals []float64) string {
	return "sqrt(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Sin) String() string {
	if u.C == nil {
		return "sin(nil)"
	}
	return "sin(" + u.C.String() + ")"
}
func (u *Sin) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "sin(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Sin) Latex(dnames, snames []string, cvals []float64) string {
	return "\\sin(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Sin) Javascript(dnames, snames []string, cvals []float64) string {
	return "Math.sin(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Cos) String() string {
	if u.C == nil {
		return "cos(nil)"
	}
	return "cos(" + u.C.String() + ")"
}
func (u *Cos) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "cos(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Cos) Latex(dnames, snames []string, cvals []float64) string {
	return "\\cos(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Cos) Javascript(dnames, snames []string, cvals []float64) string {
	return "Math.cos(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Tan) String() string {
	if u.C == nil {
		return "tan(nil)"
	}
	return "tan(" + u.C.String() + ")"
}
func (u *Tan) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "tan(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Tan) Latex(dnames, snames []string, cvals []float64) string {
	return "\\tan(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Tan) Javascript(dnames, snames []string, cvals []float64) string {
	return "tan(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Exp) String() string {
	if u.C == nil {
		return "exp(nil)"
	}
	return "exp(" + u.C.String() + ")"
}
func (u *Exp) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "exp(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Exp) Latex(dnames, snames []string, cvals []float64) string {
	return "\\exp(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Exp) Javascript(dnames, snames []string, cvals []float64) string {
	return "exp(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *Log) String() string {
	if u.C == nil {
		return "ln(nil)"
	}
	return "ln(" + u.C.String() + ")"
}
func (u *Log) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "ln(" + u.C.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *Log) Latex(dnames, snames []string, cvals []float64) string {
	return "\\log(" + u.C.Latex(dnames, snames, cvals) + ")"
}
func (u *Log) Javascript(dnames, snames []string, cvals []float64) string {
	return "log(" + u.C.Javascript(dnames, snames, cvals) + ")"
}

func (u *PowI) String() string {
	if u.Base == nil {
		return "(nil)^" + fmt.Sprint(u.Power)
	}
	return "(" + u.Base.String() + ")^(" + fmt.Sprint(u.Power) + ")"
}
func (u *PowI) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.PrettyPrint(dnames, snames, cvals) + ")^" + fmt.Sprint(u.Power)
}
func (u *PowI) Latex(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.Latex(dnames, snames, cvals) + ")^{" + fmt.Sprint(u.Power) + "}"
}
func (u *PowI) Javascript(dnames, snames []string, cvals []float64) string {
	return "Math.pow(" + u.Base.Javascript(dnames, snames, cvals) + "," + fmt.Sprint(u.Power) + ")"
}

func (u *PowF) String() string {
	if u.Base == nil {
		return "(nil)^" + fmt.Sprint(u.Power)
	}
	return "(" + u.Base.String() + ")^" + fmt.Sprint(u.Power)
}
func (u *PowF) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.PrettyPrint(dnames, snames, cvals) + ")^" + fmt.Sprint(u.Power)
}
func (u *PowF) Latex(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.Latex(dnames, snames, cvals) + ")^{" + fmt.Sprint(u.Power) + "}"
}
func (u *PowF) Javascript(dnames, snames []string, cvals []float64) string {
	return "Math.pow(" + u.Base.Javascript(dnames, snames, cvals) + "," + fmt.Sprint(u.Power) + ")"
}

func (n *PowE) String() string {
	var str string
	if n.Base == nil {
		str += "(nil)^"
	} else {
		str += "(" + n.Base.String() + ")^"
	}
	if n.Power == nil {
		str += "(nil)"
	} else {
		str += "(" + n.Power.String() + ")"
	}
	return str
}
func (u *PowE) PrettyPrint(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.PrettyPrint(dnames, snames, cvals) + ")^(" + u.Power.PrettyPrint(dnames, snames, cvals) + ")"
}
func (u *PowE) Latex(dnames, snames []string, cvals []float64) string {
	return "(" + u.Base.Latex(dnames, snames, cvals) + ")^{" + u.Power.Latex(dnames, snames, cvals) + "}"
}
func (u *PowE) Javascript(dnames, snames []string, cvals []float64) string {
	return "Math.pow(" + u.Base.Javascript(dnames, snames, cvals) + "," + u.Power.Javascript(dnames, snames, cvals) + ")"
}

func (n *Div) String() string {
	nstr, dstr := "nil", "nil"
	if n.Numer != nil {
		nstr = n.Numer.String()
	}
	if n.Denom != nil {
		dstr = n.Denom.String()
	}
	return "( " + nstr + " )/( " + dstr + " )"
}
func (n *Div) PrettyPrint(dnames, snames []string, cvals []float64) string {
	nstr, dstr := "nil", "nil"
	if n.Numer != nil {
		nstr = n.Numer.PrettyPrint(dnames, snames, cvals)
	}
	if n.Denom != nil {
		dstr = n.Denom.PrettyPrint(dnames, snames, cvals)
	}
	return "( " + nstr + " )/( " + dstr + " )"
}
func (n *Div) Latex(dnames, snames []string, cvals []float64) string {
	nstr, dstr := "nil", "nil"
	if n.Numer != nil {
		nstr = n.Numer.Latex(dnames, snames, cvals)
	}
	if n.Denom != nil {
		dstr = n.Denom.Latex(dnames, snames, cvals)
	}
	return "\\\\frac{ " + nstr + " }{ " + dstr + " }"
}
func (n *Div) Javascript(dnames, snames []string, cvals []float64) string {
	nstr, dstr := "nil", "nil"
	if n.Numer != nil {
		nstr = n.Numer.Javascript(dnames, snames, cvals)
	}
	if n.Denom != nil {
		dstr = n.Denom.Javascript(dnames, snames, cvals)
	}
	return "( " + nstr + " )/( " + dstr + " )"
}

func (n *Add) String() string {
	str := "( "
	if len(n.CS) == 0 {
		str += "[a] )"
		return str
	}
	if n.CS[0] == nil {
		str += "nil"
	} else {
		str += n.CS[0].String()
	}
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			str += " + nil"
		} else {
			str += " + " + n.CS[i].String()
		}
	}
	str += " )"
	return str
}
func (n *Add) PrettyPrint(dnames, snames []string, cvals []float64) string {
	str := "( " + n.CS[0].PrettyPrint(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += " + " + n.CS[i].PrettyPrint(dnames, snames, cvals)
	}
	str += " )"
	return str
}
func (n *Add) Latex(dnames, snames []string, cvals []float64) string {
	str := "( " + n.CS[0].Latex(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += " + " + n.CS[i].Latex(dnames, snames, cvals)
	}
	str += " )"
	return str
}
func (n *Add) Javascript(dnames, snames []string, cvals []float64) string {
	str := "( " + n.CS[0].Javascript(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += " + " + n.CS[i].Javascript(dnames, snames, cvals)
	}
	str += " )"
	return str
}

func (n *Mul) String() string {
	var str string
	if len(n.CS) == 0 {
		return "[m]"
	}
	if n.CS[0] == nil {
		str += "nil"
	} else {
		str += n.CS[0].String()
	}
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			str += " + nil"
		} else {
			str += "*" + n.CS[i].String()
		}
	}
	return str
}
func (n *Mul) PrettyPrint(dnames, snames []string, cvals []float64) string {
	str := n.CS[0].PrettyPrint(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += "*" + n.CS[i].PrettyPrint(dnames, snames, cvals)
	}
	return str
}
func (n *Mul) Latex(dnames, snames []string, cvals []float64) string {
	str := n.CS[0].Latex(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += "*" + n.CS[i].Latex(dnames, snames, cvals)
	}
	return str
}
func (n *Mul) Javascript(dnames, snames []string, cvals []float64) string {
	str := n.CS[0].Javascript(dnames, snames, cvals)
	for i := 1; i < len(n.CS); i++ {
		if n.CS[i] == nil {
			continue
		}
		str += "*" + n.CS[i].Javascript(dnames, snames, cvals)
	}
	return str
}
