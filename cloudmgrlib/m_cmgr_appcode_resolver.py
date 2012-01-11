#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from m_cmgr_resolver 	import CloudManagerResolver
from m_cmgr_tools	import is_hostname_valid
import re

class CloudManagerAppcodeResolver( object ):
	def __init__( self ):
		self._cmr = CloudManagerResolver()

	@is_hostname_valid
	def get_appcode_from_hostname(  self, *args, **kwargs ):
        	return kwargs[ 'matched_hostname' ].group( 'APP_CODE' )

	def get_all_known_appcodes( self ):
		l_appcodes = []
		d_appcodes = {}
		l_possible_hostnames = []
		for fd in self._cmr.all_dhcp_dirfd:
                        with fd.value[ 'fd' ] as afs:
				l_possible_hostnames.extend( [ s.rstrip( '.conf' ) for s in afs.listdir( fd.value[ 'dhcp_dirpath' ] ) ] )

		for hostname in l_possible_hostnames:
			try:
				l_appcodes.append( self.get_appcode_from_hostname( hostname = hostname ) )
			except:
				# Filtre les noms ne correspondant pas au template
				# des noms de serveurs
				#print '%s hostname invalide' % ( hostname )
				pass

		for e in l_appcodes:
			d_appcodes[ e ] = d_appcodes.get( e, 0 ) + 1	

		return d_appcodes
	all_known_appcodes = property( get_all_known_appcodes )




	def get_pattern_appcode( self ):
		return '(?P<APP_CODE>[a-zA-Z][0-9][0-9])'
        pattern_appcode = property( get_pattern_appcode )

       
	def is_appcode_valid( self, appcode ):
		return re.match( self.pattern_appcode, appcode )



def is_appcode_valid( func ):

        def wrapped( self, appcode ):

                if CloudManagerAppcodeResolver().is_appcode_valid( appcode ):
                        return func( self, appcode )
                else:
                        raise Exception

        return wrapped
