#!/usr/bin/env python
# -*- coding: UTF-8 -*-

d_localisation = { True: 'LOCALE', False: 'REMOTE' }
d_version = { True: 'CURRENT', False: 'OTHER' }

class IdentifiedValue( object ): 
	# if type( l_hostsmap ) <> list:

        def __init__( self, instance = None, value = None, run_on_server = None, for_conf = None ):

		self._value		= value

		if type( instance ) == str:
			self._instance 		= instance
			self._run_on_server	= run_on_server
			self._for_conf		= for_conf
		else:
			self._instance 		= instance._instance
			self._run_on_server	= instance._run_on_server
			self._for_conf		= instance._for_conf
			

	@property
	def is_locale( self ):
		return self._instance == self._run_on_server

	@property
	def is_current_conf( self ):
		return self._instance == self._for_conf

	@property
	def value( self ):
		return self._value

	@property
	def run_on_server( self ):
		return self._run_on_server

        @property
        def for_conf( self ):
                return self._for_conf

	@property
	def instance( self ):
		return self._instance

	def __repr__( self ):
		return '%s @%s[%s] @%s[%s]' % ( self.value, d_version[ self.is_current_conf ], self.for_conf , d_localisation [ self.is_locale ], self.run_on_server )


def only_current_conf( is_current_conf ):
	def wrapper( func ):
		def wrapped( self, *args, **kwargs ):
			return [ e for e in func( self, *args, **kwargs ) if e.is_current_conf == is_current_conf ]
		return wrapped
	return wrapper

def only_locale( is_locale ):
	def wrapper( func ):
		def wrapped( self, *args, **kwargs ):
			return [ e for e in func( self, *args, **kwargs ) if e.is_locale == is_locale ]
		return wrapped
	return wrapper

