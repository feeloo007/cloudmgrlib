#!/usr/bin/env python
# -*- coding: UTF-8 -*-
class CloudManagerEnvResolver( object ):
	def __init__( self ):
		self._l_envs = [ 
					{ 'env_name': 'QC', 'env_desc': u'Qualification', 'order': 0 },
					{ 'env_name': 'PR', 'env_desc': u'Production', 'order': 1 },
					{ 'env_name': 'PP', 'env_desc': u'Préproduction', 'order': 5 },
					{ 'env_name': 'R7', 'env_desc': u'Recette', 'order': 3 },
					{ 'env_name': 'FO', 'env_desc': u'Formation', 'order': 4 },
					{ 'env_name': 'DV', 'env_desc': u'Développement', 'order': 2 },
		]	
						
	def get_all_envs( self ):
		return [ env[ 'env_name' ] for env in sorted( self._l_envs, key = lambda e: e[ 'order' ], reverse = False ) ]
	all_envs = property( get_all_envs )

	def get_env_desc( self, env_name ):
		return [ env[ 'env_desc' ] for env in self._l_envs if env[ 'env_name' ] == env_name ][ 0 ]

        def get_order_for_envs( self ):
                return dict( [ ( env[ 'env_name' ], env[ 'order' ] ) for env in sorted( self._l_envs, key = lambda e: e[ 'order' ], reverse = False ) ] )
        order_for_envs = property( get_order_for_envs )
