/*
Author:		Christian Carreras
File:		term.h
Description:	Definition of the Term class.
		The Term class contains a coefficient
		and exponent which is used and implemented
		by the Array class. This class also has the ability
		to multiply, evaluate, input and output a Term as
		well as check if the exponent is equal to an int
		and check if two Terms are greater/less than each other.		
*/
#ifndef TERM_H
#define TERM_H

#include <iostream>

using namespace std;

class Term {

public:

/////////////////
//Constructor
/////////////////
/*
Function:	Constructor
Member Type:	Mutator
Description:	Sets coefficient and exponent to zero
Parameters:	None
Returns		N/A
*/
Term(float coeff = 0, int expn = 0);

/////////
//Sets
/////////
/*
Function:	setTerm
Member Type:	Mutator
Description:	Sets the coefficient and exponent in the term
Parameters:	float	- coefficient to put in the term
		int	- exponent to put in the term
Returns:	true if value is set, false if not
*/
bool setTerm(float coeff, int expn);

/*
Function:	setCoefficient
Member Type:	Mutator
Description:	Sets the coefficient in the term
Parameters:	float	- coefficient to put in the term
Returns:	true if value is set, false if not
*/
bool setCoefficient(float coeff);

/*
Function:	setExponent
Member Type:	Mutator
Description:	Sets the exponent in the term
Parameters:	int	- exponent to put in the term
Returns:	true if value is set, false if not
*/
bool setExponent(int expn);

/////////
//Gets
/////////
/*
Function:	getCoefficient
Member Type:	Inspector
Description:	Returns the coefficient value of the term
Parameters:	none
Returns:	float	- coefficient
*/
float getCoefficient() const;

/*
Function:	getExponent
Member Type:	Inspector
Description:	Returns the exponent value of the term
Parameters:	none
Returns:	int	- exponent
*/
int getExponent() const;

//////////////
//Operators
//////////////
/*
Function:	*= operator
Member Type:	Mutator
Description:	Multiplies term coefficient by a factor
Parameters:	double	- factor to multiply by
Returns:	void
*/
void operator *=(double);

/*
Function:	() operator
Member Type:	Facilitator
Description:	Evaluates the term for the given factor
Parameters:	double	- factor to evaluate the term by
Returns:	double	- the term evaluated
*/
double operator ()(double) const;

/*
Function:	== operator
Member Type:	Facilitator
Description:	Checks if the exponent of a term is equal
		to the given integer
Parameters:	int	- number to check if equal to
Returns:	true if the exponent is equal, false if not
*/
bool operator ==(int) const;

/*
Function:	< operator
Member Type:	Facilitator
Description:	Checks if the Term is less than a given Term
Parameters:	Term&	- Term to check if greater than Term
Returns:	true if the term is less than the other term, false if not
*/
bool operator <(const Term &) const;

private:

float coefficient;
int exponent;

};

////////////////////////
//Associative Operators
////////////////////////
/*
Function:	>> operator
Description:	Takes input and places it inside the term's
		coefficient and exponent.
		Enables cin << Term
Parameters:	ifstream&	- input stream
		Term&		- The Term from user-input
Returns:	ifstream
*/
ifstream &operator>>( ifstream &, Term & );

/*
Function:	<< operator
Description:	Outputs the Term in correct polynomial form
		Enables cout << Term
Parameters:	ostream&	- the output stream
		const Term&	- the Term to ouput
Returns:	ostream
*/
ostream &operator<<( ostream &, const Term & );

#endif