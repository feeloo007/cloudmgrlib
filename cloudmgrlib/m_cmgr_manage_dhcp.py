#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from contextlib     		import closing
from m_cmgr_resolver 		import CloudManagerResolver

class CloudManagerManageDHCPForWrite( object ):

	def __init__( self, hostname ):
		self._cmr		= CloudManagerResolver()
		self._hostname 		= hostname
		self._dhcp_filepath 	= self._cmr.get_dhcp_filepath( hostname = self._hostname )
		self._f 		= None

	def __enter__( self ):
		self._f = open( self._dhcp_filepath, 'w' )
		return self._f

	def __exit__( self, t, v, tr ):
		self._f.close()
		self._f = None


def test_module():
	with CloudManagerManageDHCPForWrite( 'A01-QC-HTTPD-0002-VILLE' ) as cmdhcp:
		cmdhcp.write( '' )

if __name__ == "__main__":
        test_module()
