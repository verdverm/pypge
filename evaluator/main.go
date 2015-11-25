package main

import (
	"encoding/json"
	"flag"
	// "fmt"
	"log"
	"math"
	"net/http"
	"runtime"

	"github.com/gorilla/websocket"

	"github.com/verdverm/pypge/evaluator/eqn"
	"github.com/verdverm/pypge/evaluator/regress"
)

var addr = flag.String("addr", "0.0.0.0:8080", "http service address")
var cpus = flag.Int("cpus", 4, "number of cpus to use")

var (
	InputPeek  [][]float64
	OutputPeek []float64
	InputData  [][]float64
	OutputData []float64

	// OUTGOING chan Ret

	// EQNIN chan EqnMsg
)

func init() {
	last := runtime.GOMAXPROCS(*cpus)
	log.Println("Setting CPUS to", *cpus, "was", last)

	// OUTGOING = make(chan Ret, 4096)
	// // go responder(c, outgoing)

	// EQNIN := make(chan EqnMsg, 4096)
	// for i := 0; i < *cpus; i++ {
	// 	log.Print("Starting processor", i)
	// 	go eqnProcessor(EQNIN, OUTGOING, i)
	// }

}

var upgrader = websocket.Upgrader{} // use default options

type Msg struct {
	Kind    string
	Payload interface{}
}

type Ret struct {
	Kind    string
	Payload interface{}
}

type WorkerMsg struct {
	Kind    string
	Payload int
}

type InputMsg struct {
	Kind    string
	Payload [][]float64
}

type OutputMsg struct {
	Kind    string
	Payload []float64
}

type EqnMsg struct {
	Kind    string
	Payload EqnPayload
}

type EqnPayload struct {
	Pos      int       `json:pos`
	Id       int       `json:id`
	Guess    []float64 `json:guess`
	Eserial  []int     `json:eserial`
	Eqnstr   string    `json:eqnstr`
	Jserials [][]int   `json:jserials`
	Jacstrs  []string  `json:jacstrs`
}

type EqnRet struct {
	Pos   int       `json:pos`
	Id    int       `json:id`
	Coeff []float64 `json:coeff`
	Nfev  int       `json:nfev`
	Njac  int       `json:njac`

	Score  float64 `json:score`
	R2     float64 `json:r2`
	Evar   float64 `json:evar`
	Adj_r2 float64 `json:adj_r2`
	Aic    float64 `json:aic`
	Bic    float64 `json:bic`
	Chisqr float64 `json:chisqr`
	Redchi float64 `json:redchi`
}

func eval(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()

	outgoing := make(chan Ret, 4096)
	go responder(c, outgoing)

	eqnin := make(chan EqnMsg, 4096)
	//for i := 0; i < *cpus; i++ {
	//	log.Print("Starting processor", i)
	//	go eqnProcessor(eqnin, outgoing, i)
	//}

	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			break
		}

		msg, err := unpack(message)
		if err != nil {
			err = c.WriteMessage(mt, []byte("ERROR"))
		}

		handleMessage(msg, message, outgoing, eqnin)
	}
}

func responder(c *websocket.Conn, outgoing chan Ret) {

	for {
		r := <-outgoing

		if r.Kind == "Break" {
			break
		}

		rmsg, err := json.Marshal(r)
		// log.Println("SENDING: ", r)
		err = c.WriteMessage(websocket.TextMessage, rmsg)
		if err != nil {
			log.Println("write:", err)
			break
		}
	}

}

func unpack(message []byte) (Msg, error) {
	var m Msg
	err := json.Unmarshal(message, &m)
	if err != nil {
		log.Printf("ERROR Unpack: ", err)
		return m, err
	}

	return m, nil
}

func handleMessage(msg Msg, orig []byte, outgoing chan Ret, eqnchan chan EqnMsg) {

	var ret Ret
	ret.Kind = msg.Kind

	switch msg.Kind {
	case "WorkerCnt":
		var wmsg WorkerMsg
		err := json.Unmarshal([]byte(orig), &wmsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {
			count := wmsg.Payload
			*cpus = count
			last := runtime.GOMAXPROCS(count)
			log.Println("Setting default CPUS to", count, "was", last)
			ret.Payload = "OK"
			for i := 0; i < *cpus; i++ {
				log.Print("Starting processor", i)
				go eqnProcessor(eqnchan, outgoing, i)
			}
		}

	case "InputPeek":
		var imsg InputMsg
		err := json.Unmarshal([]byte(orig), &imsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {
			InputPeek = imsg.Payload
			log.Println("GOT INPUT DATA: ", len(InputPeek))
			ret.Payload = "OK"
		}

	case "OutputPeek":
		var omsg OutputMsg
		err := json.Unmarshal([]byte(orig), &omsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {
			OutputPeek = omsg.Payload
			// log.Println("GOT OUTPUT DATA: ", len(OutputPeek))
			ret.Payload = "OK"
		}

	case "InputData":
		var imsg InputMsg
		err := json.Unmarshal([]byte(orig), &imsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {
			InputData = imsg.Payload
			// log.Println("GOT INPUT DATA: ", len(InputData), len(InputData[0]))
			ret.Payload = "OK"
		}

	case "OutputData":
		var omsg OutputMsg
		err := json.Unmarshal([]byte(orig), &omsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {
			OutputData = omsg.Payload
			// log.Println("GOT OUTPUT DATA: ", len(OutputData))
			ret.Payload = "OK"
		}

	case "PeekEqn", "EvalEqn":
		var emsg EqnMsg
		err := json.Unmarshal([]byte(orig), &emsg)
		if err != nil {
			log.Printf("ERROR Unmarshal: ", err)
			ret.Payload = err.Error()
		} else {

			// PROCESS AN EQUATION !!!
			eqnchan <- emsg
			return
		}
	}

	log.Println("sending: ", ret)
	outgoing <- ret
	// return ret
}

func eqnProcessor(incoming chan EqnMsg, outgoing chan Ret, id int) {
	for {

		emsg := <-incoming
		if emsg.Kind == "Break" {
			break
		}

		payload := emsg.Payload

		eret := handleEqnMessage(payload, emsg.Kind)
		var ret Ret
		ret.Kind = emsg.Kind
		ret.Payload = eret

		log.Println(id, eret.Pos, eret.Id)

		outgoing <- ret
	}
}

func handleEqnMessage(msg EqnPayload, kind string) EqnRet {
	// log.Printf("EqnMsg:  %+v\n", msg)

	var r EqnRet
	r.Pos = msg.Pos
	r.Id = msg.Id

	e, _ := parse(msg.Eserial)
	// e, serial := parse(msg.Eserial)
	// log.Println(e, serial)

	js := make([]eqn.Eqn, len(msg.Jserials))
	for i, jserial := range msg.Jserials {
		js[i], _ = parse(jserial)
		// log.Println("   ", js[i], serial)
	}

	Input := InputData
	Output := OutputData
	if kind == "PeekEqn" {
		Input = InputPeek
		Output = OutputPeek
	}

	coeff, train_err, nfev, njac := fitEqn(e, js, msg.Guess, Input, Output)
	r.Score = train_err
	r.Coeff = coeff
	r.Nfev = nfev
	r.Njac = njac

	r2, evar, adj_r2, aic, bic, chisqr, redchi := scoreEqn(e, coeff, Input, Output)

	r.R2 = r2
	r.Evar = evar
	r.Adj_r2 = adj_r2
	r.Aic = aic
	r.Bic = bic
	r.Chisqr = chisqr
	r.Redchi = redchi

	return r
}

func parse(serial []int) (eqn.Eqn, []int) {
	curr := serial[0]
	serial = serial[1:]
	var typ, child eqn.Eqn
	switch curr {
	case 1:
		typ = eqn.NewConstant(serial[0])
		serial = serial[1:]

	case 2:
		typ = eqn.NewConstantF(float64(serial[0]))
		serial = serial[1:]
	case 5:
		typ = eqn.NewVar(serial[0])
		serial = serial[1:]

	case 8:
		mul := eqn.NewMul()
		nchild := serial[0]
		serial = serial[1:]
		for n := 0; n < nchild; n++ {
			child, serial = parse(serial)
			mul.Insert(child)
		}
		typ = mul
	case 9:
		add := eqn.NewAdd()
		nchild := serial[0]
		serial = serial[1:]
		for n := 0; n < nchild; n++ {
			child, serial = parse(serial)
			add.Insert(child)
		}
		typ = add

	case 10:
		child, serial = parse(serial)
		pow := serial[0]
		if pow == 2 {
			// float signifier, shift one
			serial = serial[1:]
			pow = serial[0]
		}
		typ = eqn.NewPowI(child, pow)
		serial = serial[1:]

	case 12:
		child, serial = parse(serial)
		typ = eqn.NewAbs(child)
	case 13:
		child, serial = parse(serial)
		typ = eqn.NewSqrt(child)
	case 14:
		child, serial = parse(serial)
		typ = eqn.NewLog(child)
	case 15:
		child, serial = parse(serial)
		typ = eqn.NewExp(child)

	case 16:
		child, serial = parse(serial)
		typ = eqn.NewCos(child)
	case 17:
		child, serial = parse(serial)
		typ = eqn.NewSin(child)
	case 18:
		child, serial = parse(serial)
		typ = eqn.NewTan(child)

		// default:
		// 	typ = eqn.ZERO
	}

	// fmt.Println(typ.String(), serial)
	return typ, serial
}

func fitEqn(e eqn.Eqn, jac []eqn.Eqn, Guess []float64, In [][]float64, Out []float64) ([]float64, float64, int, int) {

	coeff, info := regress.LevmarEqn(e, jac, Guess, In, Out)
	train_err := info[1]
	// stats recording
	nfev := int(info[7])
	njac := int(info[8])

	return coeff, train_err, nfev, njac
}

func scoreEqn(e eqn.Eqn, Coeff []float64, In [][]float64, Out []float64) ([]float64, float64, int, int) {
	L = len(Out)
	fL = float64(L)
	fC = float64(len(Coeff))
	output := make([]float64, L)
	residuals := make([]float64, L)

	sum_y := 0.0
	sum_out := 0.0
	for i, input := range In {
		out = e.Eval(0, input, Coeff, nil)
		output[i] = out
		sum_out += out
		sum_y += Out[i]
	}
	ave_out := sum_out / fL
	ave_y := sum_y / fL

	ss_var := 0.0
	ss_tot := 0.0
	ss_reg := 0.0
	ss_res := 0.0

	for i, o_val := range Out {
		ss_var_i := output[i] - ave_out
		ss_var += ss_var_i

		ss_tot_i := Out[i] - ave_y
		ss_tot += ss_tot_i * ss_tot_i

		ss_reg_i := output[i] - ave_y
		ss_reg += ss_reg_i * ss_reg_i

		ss_res_i := output[i] - Out[i]
		ss_res += ss_res_i * ss_res_i
	}
	variance := ss_var / (fL - 1.0)
	r_squared := 1.0 - (ss_res / ss_tot)
	explained_var := ss_reg / ss_tot
	adj_r_squared := r_squared - (1.0-r_squared)*fC/(fL-fC-1.0)

	LL := math.Pow((1.0/math.Sqrt(2.0*math.Pi*variance)), N) * math.Exp(-ss_var/(variance*2.0))
	log_like := math.Log(LL)

	aic := 2.0*fC - 2.0*log_like
	bic := fC*math.Log(fL) - 2.0*log_like

	chi_squared := 0.0
	for i, o_val := range Out {
		chi_i := (output[i] - ave_out) / variance
		chi_squared += chi_i

	}
	reduced_chi_squared := chi_squared / (fL - fC - 1.0)
	return r_squared, explained_var, adj_r_squared, aic, bic, chi_squared, reduced_chi_squared

}

func main() {
	flag.Parse()
	log.SetFlags(0)
	http.HandleFunc("/echo", eval)
	log.Print("Listening at: ", *addr)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
