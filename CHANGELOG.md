Change Log
----------




### 0.7
-----------

#### Enhancements:

1. Adds policies for model initialization and expansion
	**low**: The simplest
	**med**: The default
	**high**: This can take much longer
2. Adds experiments folder, scripts, and config files
	These are related to batch runs and reproducible research.
3. Adds fitness_function.py
	This allows the fitness calculation for prioritization to be pluggable. Motivation for this was to normalize the values across all models.
4. Adds timer facilities
	This enables each phase to be timed and can include messages.
5. Adds logging facilities
	This enables output to be piped to several, configurable log files.
6. Python 3 support



#### Bug Fixes:

1. Printing models which are a single floating
	The root cause is the model.subs(...) where an expression simplifies to a single float value. The model.pretty passed to the format string should have been a string. This resulted in an exception that would end the search.



------------------

------------------

### pre-0.7 

unrecorded...
