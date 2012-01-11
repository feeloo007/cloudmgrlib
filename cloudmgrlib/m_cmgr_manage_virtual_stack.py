#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import with_statement
import os
from fabric.api			import hosts, run, env
from m_cmgr_manage_dhcp		import CloudManagerManageDHCPForWrite
from m_cmgr_cloudmap_resolver   import CloudManagerCloudMapResolver
import random

d_templates = { 
			'VILLE':
					{
						'HTTPD': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
						'TOMCAT': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
						'MYSQL': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
					},
			'DMZ':
					{
						'HTTPD': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
						'TOMCAT': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
						'MYSQL': 	'/Users/feeloo007/dev/U64.cloud.HTTPD.template.paris.mdp',
					},
}

vm_dirpath = '/Users/feeloo007/dev'

def create_next_dhcp_file_for( appcode = None, env = None , appcomp = None, aera = None ):
      # Réservation du nom de serveur
      next_hostname = CloudManagerCloudMapResolver().get_next_hostname_for( appcode = appcode, env = env, appcomp = appcomp, aera = aera )
      with CloudManagerManageDHCPForWrite( next_hostname ) as cmdhcp:
         cmdhcp.write( '' )
      return next_hostname


env.host_string =  'feeloo007@192.168.142.1'
def create_vm( hostname = None, appcomp = None, aera = None ):
	run( 'cp -r %s.vmwarevm %s.vmwarevm' % ( d_templates[ aera ][ appcomp ], vm_dirpath + os.sep + hostname) )
	hw_address = '"00:50:56:%X:%X:%X"' % ( random.randint( 0, 255 ), random.randint( 0, 255 ), random.randint( 0, 255 ) )
	run( 'sed -i -E \'s/ethernet0.address = (.*)/ethernet0.address = %s/\' \'%s\'' % ( hw_address, vm_dirpath + os.sep + hostname + '.vmwarevm' + os.sep + 'Ubuntu 64 bits.vmx' ) )
        return hw_address


def test_module():
	create_vm( 'A01-QC-HTTPD-0003-VILLE','HTTPD', 'VILLE' )


if __name__ == "__main__":
        test_module()
