# Tableaux Method for Propositional Logic Deduction
## Overview
This project provides a Python implementation of the Tableaux method for propositional logic deduction. 
The Tableaux method is a proof procedure used to determine the satisfiability of propositional logic formulas. 
The implementation allows you to input a propositional logic formula and determine its satisfiability.

## Features
- Input a propositional logic formula in a user-friendly format.
- Automatically determine whether the formula is satisfiable.
- Generate a tableau tree to visualize the deduction process.

## Example
Input: " ~(((p → q) ∧ ( (p → q) → r)) → (p → r))"

Output: The formula is not satisfiable
        
Representation of the tableaux tree:

```python
['~(((p → q) ∧ ((p ∧ q) → r)) → (p → r))']
	['((p → q) ∧ ((p ∧ q) → r))', '~(p → r)']
		['(p → q)', '((p ∧ q) → r)']
			['p', '~r']
				['~p']
					['X']
				['q']
					['~(p ∧ q)']
						['~p']
							['X']
						['~q']
							['X']
					['r']
						['X']
