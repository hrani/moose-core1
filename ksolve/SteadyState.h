/**********************************************************************
** This program is part of 'MOOSE', the
** Messaging Object Oriented Simulation Environment,
** also known as GENESIS 3 base code.
**           copyright (C) 2003-2009 Upinder S. Bhalla. and NCBS
** It is made available under the terms of the
** GNU Lesser General Public License version 2.1
** See the file COPYING.LIB for the full notice.
**********************************************************************/

#ifndef _SteadyState_h
#define _SteadyState_h
class SteadyState
{
#ifdef DO_UNIT_TESTS
	friend void testSteadyState();
#endif
	public:
		SteadyState();
		~SteadyState();
		
		///////////////////////////////////////////////////
		// Field function definitions
		///////////////////////////////////////////////////
		static bool badStoichiometry( Eref e );
		static bool isInitialized( Eref e );
		static unsigned int getRank( Eref e );
		static unsigned int getNiter( Eref e );
		static unsigned int getMaxIter( Eref e );
		static void setMaxIter( const Conn* c, unsigned int value );
		static string getStatus( Eref e );
		static double getConvergenceCriterion( Eref e );
		static void setConvergenceCriterion( const Conn* c, double value );

		///////////////////////////////////////////////////
		// Msg Dest function definitions
		///////////////////////////////////////////////////
		static void settleFunc( const Conn* c );
		static void resettleFunc( const Conn* c );
		void settle( bool forceSetup );
		
		// funcs to handle externally imposed changes in mol N
		static void setMolN( const Conn* c, double y, unsigned int i );
		static void assignStoichFunc( const Conn* c, void* stoich );
		void assignStoichFuncLocal( void* stoich );
		static const double EPSILON;

	private:
		void setupSSmatrix();
		
		///////////////////////////////////////////////////
		// Internal fields.
		///////////////////////////////////////////////////
		unsigned int nIter_;
		unsigned int maxIter_;
		bool badStoichiometry_;
		string status_;
		bool isInitialized_;
		bool isSetup_;
		double convergenceCriterion_;

		gsl_matrix* LU_;
		Stoich* s_;
		unsigned int nVarMols_;
		unsigned int nReacs_;
		unsigned int rank_;
		
};

extern const Cinfo* initSteadyStateCinfo();
#endif // _SteadyState_h
