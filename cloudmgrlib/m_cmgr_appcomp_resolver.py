#!/usr/bin/env python
# -*- coding: UTF-8 -*-
class CloudManagerAppCompResolver( object ):
	def __init__( self ):
		self._l_appcomps = [ 
					{ 'appcomp_name': 'HTTPD', 	'appcomp_desc': u'Apache', 'aeras': [ 'DMZ', 'VILLE' ], 'order': 1 },
					{ 'appcomp_name': 'TOMCAT', 	'appcomp_desc': u'Tomcat', 'aeras': [ 'VILLE' ], 'order': 2 },
					{ 'appcomp_name': 'MYSQL', 	'appcomp_desc': u'MySQL' , 'aeras': [ 'VILLE' ], 'order': 3 }, 
		]	
						
	def get_all_appcomps( self ):
		return [ appcomp[ 'appcomp_name' ] for appcomp in sorted( self._l_appcomps, key = lambda e: e[ 'order' ], reverse = False ) ]
	all_appcomps = property( get_all_appcomps )

        def get_appcomp_desc( self, appcomp_name ):
                return [ appcomp[ 'appcomp_desc' ] for appcomp in self._l_appcomps if appcomp[ 'appcomp_name' ] == appcomp_name ][ 0 ]

        def get_all_appcomps_for_aera( self, aera ):
                return [ appcomp[ 'appcomp_name' ] for appcomp in self._l_appcomps if aera in appcomp[ 'aeras' ] ]

        def get_order_for_appcomps( self ):
                return dict( [ ( appcomp[ 'appcomp_name' ], appcomp[ 'order' ] ) for appcomp in sorted( self._l_appcomps, key = lambda e: e[ 'order' ], reverse = False ) ] )
        order_for_appcomps = property( get_order_for_appcomps )

