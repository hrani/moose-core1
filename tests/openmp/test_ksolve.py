import moose
import moose.utils as mu
import numpy as np
#import matplotlib.pyplot as plt
import time

#to know the path from where the files are taken
print( '[INFO] Using moose from %s' % moose.__file__ )


#Tables for storing the concentration of each species
tables_ = { }


#The following function creates a compartment which can have voxels and in each voxel computations can be done
def create_cylinder( name ):
#creating a model, just a model, created a file path
    moose.Neutral( '/model' )
#Making the model cylindrical, setting the properties of the model...like here its a cylinder
    c = moose.CylMesh( '/model/%s' % name )
#Setting the length of the cyliinder
    c.x1 = 1
#Setting the number of voxels
    c.diffLength = c.x1 / (1000 )
#radius of the cylinder at both the faces, in here its kept same at both the faces
    c.r0 = c.r1 = 1e-3
    print( 'Volume of cylinder %s is %g' % (c.name,  c.volume) )
    return c

#In the following function we are defining which solvee to use
def setup_solver( c ):
#Its important step
    s = moose.Stoich( '/model/stoich')
#we declared k to be denoting ksolve
    k = moose.Ksolve( '/model/ksolve' )
#solver for the s is ksolve
    s.ksolve = k
#On which compartment does s has to work
    s.compartment = c
#Where is the compartment and there we add the path of the c compartment
    s.path = '%s/##' % c.path 


#Defining wha should be happening in the compartment and therefore in the voxels, the reactions are defined 
#There are different species in a pool
def make_model( ):
    cyl = create_cylinder( 'a' )
    # it stores the pool species
    pools = { }
    for i in range( 2 ):
        a = 'A%d' % i
        c = 'C%d' % i
        pa = moose.Pool( '/model/a/%s' % a )
        pc = moose.Pool( '/model/a/%s' % c )
        ta = moose.Table2( '/model/a/tab%s' %  a)
        tc = moose.Table2( '/model/a/tab%s' %  c)
        moose.connect( ta, 'requestOut', pa, 'getN' )
        moose.connect( tc, 'requestOut', pc, 'getN' )
        pools[ a ] = pa
        pools[ c ] = pc
        pa.concInit = 1.0
        pc.concInit = 0.1
        tables_[ a ] = ta
        tables_[ c ] = tc
        r = moose.Reac( '/model/a/r%d' % i )
        moose.connect( r, 'sub', pa, 'reac' )
        moose.connect( r, 'prd', pc, 'reac' )
        r.Kf = 1
        r.Kb = 0.1

    setup_solver( cyl )
    moose.reinit( )   # Build the system

    t1 = time.clock()
    moose.start( 10 ) # Run the system
    print(' Time takes %f' % (time.clock() - t1))
    print( tables_[ 'A0' ].vector )
    k = moose.element( '/model/ksolve' )


def main( ):
    make_model( )

#running the function!
if __name__ == '__main__':
    main()