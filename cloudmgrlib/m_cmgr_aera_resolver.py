#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from operator	import attrgetter

class CloudManagerAeraResolver( object ):
	def __init__( self ):
		self._l_aeras = [ 
					{ 'aera_name': 'DMZ', 	'aera_desc': u'Réseau Internet', 'order': 1 },
					{ 'aera_name': 'VILLE', 'aera_desc': u'Réseau Ville', 'order': 2 },
		]	
						
	def get_all_aeras( self ):
		return [ aera[ 'aera_name' ] for aera in sorted( self._l_aeras, key = lambda e: e[ 'order' ], reverse = False ) ]
	all_aeras = property( get_all_aeras )

        def get_aera_desc( self, aera_name ):
                return [ aera[ 'aera_desc' ] for aera in self._l_aeras if aera[ 'aera_name' ] == aera_name ][ 0 ]

        def get_order_for_aeras( self ):
		return dict( [ ( aera[ 'aera_name' ], aera[ 'order' ] ) for aera in sorted( self._l_aeras, key = lambda e: e[ 'order' ], reverse = False ) ] )
	order_for_aeras = property( get_order_for_aeras )
