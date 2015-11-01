from __future__ import print_function

from pypge import evaluate
from pypge import algebra

## We ~can~ parallelize the following stages
#
#  + evaluation
#  ? expansion
#  ? algebra
#
#  '+' means it showed improvement
#  '-' means it showed loss
#  '?' means we don't know yet
#

# was getting a consistent deadlock, or infinite loop here, in SymPy 7.6, upgraded locally to 7.6.1  (conda vs pip)
# File "/Users/tony/anaconda/lib/python2.7/site-packages/sympy/polys/densearith.py", line 770, in dup_mul
#   for j in xrange(max(0, i - dg), min(df, i) + 1):


## PEEK EVALUATION MULTIPROCESSING
def unwrap_self_peek_model_queue(pge_instance):
	pos, modl = -1, None
	while True:
		try:
			val = pge_instance.peek_in_queue.get()
			if val is None:
				print("Val None Breaking Peek Processor")
				break;
			pos = val[0]
			modl = val[1]

			passed = evaluate.PGE.peek_model(pge_instance, modl)
			if not passed:
				pge_instance.peek_out_queue.put( (pos, modl.error, modl.exception) )
			else:
				vals = [ (k,v) for (k,v) in modl.params.valuesdict().items() ]
				ret_data = {
					'score': modl.score,
					'r2': modl.r2,
					'evar': modl.evar,
					'aic': modl.aic,
					'bic': modl.bic,
					'chisqr': modl.chisqr,
					'redchi': modl.redchi,
					'params': vals,
					'nfev': modl.fit_result.nfev
				}
				pge_instance.peek_out_queue.put( (pos, None, ret_data) )

		except Exception as e:
			print("peek breaking!", e, "\n  ", pos, modl.expr, val)
			break


## FULL EVALUATION MULTIPROCESSING
def unwrap_self_eval_model_queue(pge_instance):
	while True:
		try:
			val = pge_instance.eval_in_queue.get()
			if val is None:
				print("Val None Breaking Eval Processor")
				break;
			pos = val[0]
			modl = val[1]

			passed = False
			passed = evaluate.PGE.eval_model(pge_instance, modl)
			if not passed:
				pge_instance.eval_out_queue.put( (pos, modl.error, modl.exception) )

			else:
				vals = [ (k,v) for (k,v) in modl.params.valuesdict().items() ]
				# vals = modl.params.valuesdict()
				ret_data = {
					'score': modl.score,
					'r2': modl.r2,
					'evar': modl.evar,
					'aic': modl.aic,
					'bic': modl.bic,
					'chisqr': modl.chisqr,
					'redchi': modl.redchi,
					'params': vals,
					'nfev': modl.fit_result.nfev
				}
			
				pge_instance.eval_out_queue.put( (pos, None, ret_data) )

		except Exception as e:
			print("eval breaking!", e, "\n  ", pos, modl.expr, passed, modl.params.valuesdict())
			break


## ALGEBRA MULTIPROCESSING
def unwrap_self_alge_model_queue(pge_instance):
	while True:
		try:
			val = pge_instance.alge_in_queue.get()
			if val is None:
				print("Val None Breaking Algebra Processor")
				break;
			pos = val[0]
			modl = val[1]
			meth = val[2]


			alged, err = algebra.manip_model(modl, meth)
			if err is not None:
				pge_instance.alge_out_queue.put( (pos, err, None, None) )
			else:


				pge_instance.alge_out_queue.put( (pos, None, meth, alged) )
		except Exception as e:
			print("alge breaking!", e, "\n  ", pos, modl.expr)
			break
