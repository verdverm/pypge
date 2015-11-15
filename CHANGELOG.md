Change Log
----------




### 0.7
-----------

#### Enhancements:

1. Major!! speed improvements
    - remote evaluator written in Go
    - pulled memoization into search class
1. Adds policies for model initialization and expansion
	- **low**: The simplest
	- **med**: The default
	- **high**: This can take much longer
1. New Expansion operators
    - AddTerm at Toplevel
    - Shrink addition operator
1. Multi-tiered expansion
    - Progressive expansion of models
    - Each tier configurable independently
1. Adds fitness_function.py
	- This allows the fitness calculation for prioritization to be pluggable. 
	- Motivation for this was to normalize the values across all models.
	- Weighted fitness components
	- Also added penalized size, jacobian size
1. Adds experiments folder, scripts, and config files
	- These are related to batch runs and reproducible research.
1. Adds timer facilities
	- This enables each phase to be timed and can include messages.
1. Adds logging facilities
	- This enables output to be piped to several, configurable log files.
1. Python 3 support
1. Missing some, I'm sure...



#### Bug Fixes:

1. Printing models which are a single floating
	The root cause is the model.subs(...) where an expression simplifies to a single float value. The model.pretty passed to the format string should have been a string. This resulted in an exception that would end the search.



------------------

------------------

### pre-0.7 

unrecorded...
