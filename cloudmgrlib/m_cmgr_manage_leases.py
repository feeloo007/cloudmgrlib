#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from contextlib     import closing
from m_cmgr_resolver import CloudManagerResolver

class CloudManagerManagedLeaseForWrite( object ):

	def __init__( self, hostname ):
		self._cmr	= CloudManagerResolver()
		self._hostname 	= hostname
		self._l_fd 	= self._cmr.get_all_saving_lease_filefd( hostname = self._hostname )
		self._l_f 	= []

	def __enter__( self ):

		for fd in self._l_fd:
			afs = fd.value[ 'fd' ].__enter__()
			self._l_f.append( afs.open( fd.value[ 'saved_leases_filepath' ], 'w' ) )
		return self

	def __exit__( self, t, v, tr ):
	
		if t:
			print tr

		for f in self._l_f:
			f.close()
			self._l_f.remove( f )

		for fd in self._l_fd:
			fd.value[ 'fd' ].__exit__( t, v, tr ) 

	def write( self, l ):
		for f in self._l_f:
			f.write( l )


def test_module():

	with CloudManagerManagedLeaseForWrite( 'A05-QC-HTTPD-0001-VILLE' ) as cml:
		cml.write( 'TEST' )	

if __name__ == "__main__":
        test_module()
