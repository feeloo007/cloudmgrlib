#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
from m_cmgr_identify_value 	import IdentifiedValue

def last_os_sep_deleted( func ):

       	def wrapped( self, *args, **kwargs ):

		def f_last_os_sep_deleted( s ):
        		return s.rstrip( os.sep )

		d_last_os_sep_deleted	= {}
		f_on_str                = lambda e: f_last_os_sep_deleted( e )
		f_on_list               = lambda l: map( lambda e: d_last_os_sep_deleted[ e.__class__ ]( e ), l )
		f_on_lo                 = lambda e: IdentifiedValue( instance = e, value = f_last_os_sep_deleted( e.value ) )
		d_last_os_sep_deleted   = { str: f_on_str, list: f_on_list, IdentifiedValue: f_on_lo }

		result = func( self, *args, **kwargs )
		return d_last_os_sep_deleted[ result.__class__ ]( result )

	return wrapped


def instances_sorted( func ):

	def wrapped( self, *args, **kwargs ):

		return sorted( func( self, *args, **kwargs ) )	

	return wrapped



hostname_pattern = '^(?P<APP_CODE>[a-zA-Z][0-9][0-9])-(?P<ENV>PR|PP|R7|FO|DV|QC)-(?P<COMPOSANT>TOMCAT|HTTPD|MYSQL)-(?P<NUM_COMPOSANT>[0-9][0-9][0-9][0-9])-(?P<ZONE>VILLE|DMZ)$'
#hostname_pattern = ''
#hostname_pattern += '^(?P<APP_CODE>[a-zA-Z][0-9][0-9])'
#hostname_pattern += '^(?P<APP_CODE>[a-zA-Z][0-9][0-9])'

#app_code_pattern = '^(?P<APP_CODE>[a-zA-Z][0-9][0-9])'

#l_env_ref = [ 'PR', 'R7', 'PP', 'FO', 'DV' ]

def is_hostname_valid( func ):

	def wrapped( self, *args, **kwargs ):

		m = re.match( hostname_pattern, kwargs[ 'hostname' ] )

		if m:
			kwargs[ 'matched_hostname' ] = m
			return func( self, *args, **kwargs )
		else:
			raise Exception

	return wrapped 



def test_module():

	class TestHostnameValid( object ):
		@is_hostname_valid
		def test_hostname( self, *args, **kwargs ):
			print kwargs[ 'hostname' ]
			print kwargs[ 'matched_hostname' ]

	thv = TestHostnameValid()
	thv.test_hostname( hostname = 'A01-QC-HTTPD-0001-VILLE' )

if __name__ == "__main__":
        test_module()
