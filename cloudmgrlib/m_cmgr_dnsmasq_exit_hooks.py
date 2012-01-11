#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import 	sys
import 	os
from contextlib     		import closing
from m_cmgr_resolver 		import CloudManagerResolver
from m_cmgr_manage_leases	import CloudManagerManagedLeaseForWrite
from m_cmgr_manage_active_hosts	import CloudManagerManagedActiveHostsForWrite
 
cloudmgr_tags 	= os.environ.get( 'DNSMASQ_TAGS', '').split( ' ' )[0]
domainname 	= os.environ.get( 'DNSMASQ_DOMAIN', None )

def action_add( *args ):
	# Analyse des paramètres
	hardaddr 	= args[0]
	ip 		= args[1]
	hostname 	= args[2]
	lease_expires 	= os.environ[ 'DNSMASQ_LEASE_EXPIRES' ]
	cmr		= CloudManagerResolver()

	with CloudManagerManagedLeaseForWrite( hostname ) as cml:
		cml.write( '%s %s %s %s *\n' % ( lease_expires, hardaddr, ip, hostname ) )

	with CloudManagerManagedActiveHostsForWrite( hostname ) as cmah:
	        if not domainname:
                	cmah.write( '%s\t\t%s\t# %s\n' % ( ip, hostname, cloudmgr_tags ) )
         	else:
                	cmah.write( '%s\t\t%s.%s %s\t# %s\n' % ( ip, hostname, domainname, hostname, cloudmgr_tags ) )

def action_del( *args ):
        pass

def action_old( *args ):
        pass

# Ouverture du fichier de trace

d_action = {
		'add': action_add,
		'del': action_del,
		'old': action_old,
}

d_action[ sys.argv[ 1 ] ]( *sys.argv[2::] )

sys.exit( 0 )
