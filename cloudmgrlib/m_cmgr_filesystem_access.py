#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from contextlib     import closing
from fabric.network import connect
import os
import traceback

	

class ContextualFileSystemAccess( object ):

	def __init__( self, identified_value ):

		self._identified_value = identified_value
		self._ssh = None
		self._sftp = None

	def __enter__( self ):
		if self._identified_value.is_locale:
			modified_os = os
			modified_os.open = open
			return modified_os
		else:
		       	self._ssh  = connect( 'cloudmgr', self._identified_value.run_on_server, 22 )
               		self._sftp = self._ssh.open_sftp()
			return self._sftp

	def __exit__( self, t, v, tr ):
		if self._sftp: 
			self._sftp.close()
			self._sftp = None
		if self._ssh: 
			self._ssh.close()
			self._ssh = None
