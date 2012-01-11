#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
from contextlib     import closing
from m_cmgr_tools import last_os_sep_deleted, instances_sorted, is_hostname_valid
from m_cmgr_identify_value import IdentifiedValue, only_current_conf, only_locale
from m_cmgr_filesystem_access import ContextualFileSystemAccess


class CloudManagerResolver( object ):

	def __init__( self, instance = None ):
		'''Initiliase un objet CloudManagerResolver
		avec :
			instance = l'instance exécutant le script si instance n'existe pas
			instance avec la valeur passé en paramètre'''	
		if not instance:
			instance = self.running_instance
		self._instance = instance

        ##################################
        # Gestion des variables globales #
        ##################################

	@last_os_sep_deleted
	def get_root_datas_dir( self ):
		return os.environ[ 'CLOUDMGR_INSTANCE_VAULT' ]
	root_datas_dir 	= property( get_root_datas_dir )


	#########################
	# Gestion des instances #
	#########################

	@property
	@last_os_sep_deleted
	def instance( self ):
		return self._instance

	@last_os_sep_deleted
	def get_running_instance( self ):
		return os.environ[ 'CLOUDMGR_INSTANCE' ]
	running_instance = property( get_running_instance )	


        def is_running_instance( self ):
                return self.instance == self.running_instance
        is_running_instance = property( is_running_instance )


        @last_os_sep_deleted
        @instances_sorted
        def get_all_instances( self ):
                return os.listdir( self.root_datas_dir )
        all_instances = property( get_all_instances )


        def instances_localized( func ):

                def wrapped( self, *args, **kwargs ):

                        new_result = []

                        result = func( self, *args, **kwargs )

                        new_result = reduce(
                                        list.__add__,
                                        [
                                                reduce(
                                                        list.__add__,
                                                        [
                                                                [
                                                                        IdentifiedValue(
                                                                                instance        = self.instance,
                                                                                value           = instance,
                                                                                run_on_server   = server,
                                                                                for_conf        = instance,
                                                                        )
                                                                ]
                                                        for server in result
                                                        ]
                                                ) for instance in result
                                        ]
                        )

                        return new_result

                return wrapped


        @instances_localized
        def get_all_instances_localized( self ):
                return self.all_instances
        all_instances_localized = property( get_all_instances_localized )


	###########################################
	# Gestion des hosts générés (active_host) #
	###########################################

	@last_os_sep_deleted
	def get_active_hosts_dir( self ):
		return 'hosts/active'
	active_hosts_dir = property( get_active_hosts_dir )


	@last_os_sep_deleted
        def get_active_hosts_dirpath( self ):
                return self.root_datas_dir + os.sep + self.instance + os.sep + self.active_hosts_dir
        active_hosts_dirpath = property( get_active_hosts_dirpath )


        @last_os_sep_deleted
        def get_active_hosts_dirpath_for_running_instance( self ):
                return self.root_datas_dir + os.sep + self.running_instance + os.sep + self.active_hosts_dir
        active_hosts_dirpath_for_running_instance = property( get_active_hosts_dirpath_for_running_instance )


        @last_os_sep_deleted
        def get_all_active_hosts_dirpath( self ):
                return [ CloudManagerResolver( instance ).active_hosts_dirpath for instance in self.all_instances ]
        all_active_hosts_dirpath = property( get_all_active_hosts_dirpath )


        @last_os_sep_deleted
        def get_all_active_hosts_dirpath_localized( self ):
                return [        IdentifiedValue(
                                        value = CloudManagerResolver(
                                                instance_localized.value
                                        ).active_hosts_dirpath,
                                        instance = instance_localized
                                ) for instance_localized in self.all_instances_localized
                ]
        all_active_hosts_dirpath_localized = property( get_all_active_hosts_dirpath_localized )


        def get_all_active_hosts_dirfd( self ):
                return [        IdentifiedValue(
                                        value = { 'fd': ContextualFileSystemAccess( active_host_dirpath_localized ), 'active_hosts_dirpath': active_host_dirpath_localized.value },
                                        instance = active_host_dirpath_localized
                                ) for active_host_dirpath_localized in self.all_active_hosts_dirpath_localized
                ]
        all_active_hosts_dirfd = property( get_all_active_hosts_dirfd )


        @is_hostname_valid
        def get_active_host_filepath( self, *args, **kwargs ):
                hostname = kwargs[ 'hostname' ]
                return self.active_hosts_dirpath + os.sep + hostname + '.host'


        def get_all_saved_active_host_filepath_localized( self, *args, **kwargs ):
                return [        IdentifiedValue(
                                        value = CloudManagerResolver(
                                                instance_localized.value
                                        ).get_active_host_filepath( *args, **kwargs ),
                                        instance = instance_localized
                                ) for instance_localized in self.all_instances_localized
                ]


        @only_current_conf( True )
        def get_all_saving_active_host_filepath_localized( self, *args, **kwargs ):
                return self.get_all_saved_active_host_filepath_localized( self, *args, **kwargs )


        def get_all_saving_active_host_filefd( self, *args, **kwargs ):
                return [        IdentifiedValue(
                                        value = { 'fd': ContextualFileSystemAccess( saved_active_host_filepath_localized ), 'active_host_filepath': saved_active_host_filepath_localized.value },
                                        instance = saved_active_host_filepath_localized
                                ) for saved_active_host_filepath_localized in self.get_all_saving_active_host_filepath_localized( *args, **kwargs )
                ]


	##########################################
	# Gestion des hosts commun (common_host) #
	##########################################

        @last_os_sep_deleted
        def get_common_hosts_dir( self ):
                return 'hosts/common'
        common_hosts_dir = property( get_common_hosts_dir )

        @last_os_sep_deleted
        def get_common_hosts_dirpath( self ):
                return self.root_datas_dir + os.sep + self.instance + os.sep + self.common_hosts_dir
        common_hosts_dirpath = property( get_common_hosts_dirpath )

        @last_os_sep_deleted
        def get_common_hosts_dirpath_for_running_instance( self ):
                return self.root_datas_dir + os.sep + self.running_instance + os.sep + self.common_hosts_dir
        common_hosts_dirpath_for_running_instance = property( get_common_hosts_dirpath_for_running_instance )


	##############################################
	# Gestion des leases sauvegardées ( leases ) #
	##############################################

	@last_os_sep_deleted
	def get_saved_leases_dir( self ):
		return 'leases'
	saved_leases_dir = property( get_saved_leases_dir )	

        @last_os_sep_deleted
        def get_saved_leases_dirpath( self ):
                return self.root_datas_dir + os.sep + self.instance + os.sep + self.saved_leases_dir
        saved_leases_dirpath = property( get_saved_leases_dirpath )

        @last_os_sep_deleted
        def get_saved_leases_dirpath_for_running_instance( self ):
                return self.root_datas_dir + os.sep + self.running_instance + os.sep + self.saved_leases_dir
        saved_leases_dirpath_for_running_instance = property( get_saved_leases_dirpath_for_running_instance )


        @last_os_sep_deleted
	def get_all_saved_leases_dirpath( self ):
		return [ CloudManagerResolver( instance ).saved_leases_dirpath for instance in self.all_instances ]
	all_saved_leases_dirpath = property( get_all_saved_leases_dirpath )


        @last_os_sep_deleted
        def get_all_saved_leases_dirpath_localized( self ):
                return [ 	IdentifiedValue( 
					value = CloudManagerResolver( 
						instance_localized.value 
					).saved_leases_dirpath, 
					instance = instance_localized
				) for instance_localized in self.all_instances_localized
		]
        all_saved_leases_dirpath_localized = property( get_all_saved_leases_dirpath_localized )


	def get_all_saved_leases_dirfd( self ):
                return [        IdentifiedValue(
					value = { 'fd': ContextualFileSystemAccess( saved_leases_dirpath_localized ), 'saved_leases_dirpath': saved_leases_dirpath_localized.value },
                                        instance = saved_leases_dirpath_localized
                                ) for saved_leases_dirpath_localized in self.all_saved_leases_dirpath_localized
                ]
	all_saved_leases_dirfd = property( get_all_saved_leases_dirfd )


        @is_hostname_valid
        def get_saved_lease_filepath( self, *args, **kwargs ):
                hostname = kwargs[ 'hostname' ]
                return self.saved_leases_dirpath + os.sep + hostname + '.host'


	def get_all_saved_lease_filepath_localized( self, *args, **kwargs ):
                return [        IdentifiedValue(
                                        value = CloudManagerResolver(
                                                instance_localized.value
                                        ).get_saved_lease_filepath( *args, **kwargs ),
                                        instance = instance_localized
                                ) for instance_localized in self.all_instances_localized
                ]


	@only_current_conf( True )
	def get_all_saving_lease_filepath_localized( self, *args, **kwargs ):
		return self.get_all_saved_lease_filepath_localized( self, *args, **kwargs )


        def get_all_saving_lease_filefd( self, *args, **kwargs ):
                return [        IdentifiedValue(
                                        value = { 'fd': ContextualFileSystemAccess( saved_leases_filepath_localized ), 'saved_leases_filepath': saved_leases_filepath_localized.value },
                                        instance = saved_leases_filepath_localized
                                ) for saved_leases_filepath_localized in self.get_all_saving_lease_filepath_localized( *args, **kwargs )
                ]


	###################
	# Gestion du DHCP #
	###################

        @last_os_sep_deleted
        def get_dhcp_dirpath( self ):
                return os.environ[ 'CLOUDMGR_DHCP' ]
        dhcp_dirpath  = property( get_dhcp_dirpath )


        @is_hostname_valid
        def get_dhcp_filepath( self, *args, **kwargs ):
                hostname = kwargs[ 'hostname' ]
                return self.dhcp_dirpath + os.sep + hostname + '.conf'


	@only_current_conf( True )
        def get_all_dhcp_dirpath_localized( self ):
                return [        IdentifiedValue(
                                        value = CloudManagerResolver(
                                                instance_localized.value
                                        ).dhcp_dirpath,
                                        instance = instance_localized
                                ) for instance_localized in self.all_instances_localized
                ]
        all_dhcp_dirpath_localized = property( get_all_dhcp_dirpath_localized )


        def get_all_dhcp_dirfd( self ):
                return [        IdentifiedValue(
                                        value = { 'fd': ContextualFileSystemAccess( dhcp_dirpath_localized ), 'dhcp_dirpath': dhcp_dirpath_localized.value },
                                        instance = dhcp_dirpath_localized
                                ) for dhcp_dirpath_localized in self.all_dhcp_dirpath_localized
                ]
        all_dhcp_dirfd = property( get_all_dhcp_dirfd )



def test_module():
	
	for cmr in [ CloudManagerResolver(), CloudManagerResolver( 'CLOUDMGR001' ), CloudManagerResolver( 'CLOUDMGR002' ) ]:
		print '###################################'
		print '# TEST SUR LES VARIABLES.GLOBALES #'
		print '###################################'
		print cmr.root_datas_dir
		print
		print '#####################################'
		print '# TEST SUR LES VARIABLES D\'INSTANCE #'
		print '#####################################'
		print cmr.instance
		print cmr.running_instance
		print cmr.is_running_instance
		print cmr.all_instances
		print cmr.all_instances_localized
		print 
		print '#######################################'
		print '# TEST SUR LES VARIABLES D\'HOTE ACTIF #'
		print '#######################################'
		print cmr.active_hosts_dir
		print cmr.active_hosts_dirpath
		print cmr.active_hosts_dirpath_for_running_instance
		print cmr.all_active_hosts_dirpath
		print cmr.all_active_hosts_dirpath_localized
                print cmr.all_active_hosts_dirfd
                for fd in cmr.all_active_hosts_dirfd:
                        print '%s' % ( fd )
                        with fd.value[ 'fd' ] as afs:
                                print afs.listdir( fd.value[ 'active_hosts_dirpath' ] )
		print cmr.get_active_host_filepath( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.get_all_saved_active_host_filepath_localized( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.get_all_saving_active_host_filepath_localized( hostname = 'A04-QC-HTTPD-0001-VILLE' )
                print cmr.get_all_saving_active_host_filefd( hostname = 'A04-QC-HTTPD-0001-VILLE' )
                for fd in cmr.get_all_saving_active_host_filefd( hostname = 'A04-QC-HTTPD-0001-VILLE' ):
                        print '%s' % ( fd )
                        with fd.value[ 'fd' ] as afs:
                                with closing( afs.open( fd.value[ 'active_host_filepath' ], 'w' ) ) as f:
                                        pass
                                afs.remove( fd.value[ 'active_host_filepath' ] )
		print
		print '########################################'
		print '# TEST SUR LES VARIABLES D\'HOTE COMMUN #'
		print '########################################'
		print cmr.common_hosts_dir
		print cmr.common_hosts_dirpath
		print cmr.common_hosts_dirpath_for_running_instance
		print
		print '###################################'
		print '# TEST SUR LES VARIABLES DE LEASE #'
		print '###################################'
		print cmr.saved_leases_dir
		print cmr.saved_leases_dirpath
		print cmr.saved_leases_dirpath_for_running_instance
		print cmr.all_saved_leases_dirpath
		print cmr.all_saved_leases_dirpath_localized
		print cmr.all_saved_leases_dirfd
		for fd in cmr.all_saved_leases_dirfd:
			print '%s' % ( fd )
			with fd.value[ 'fd' ] as afs:
				print afs.listdir( fd.value[ 'saved_leases_dirpath' ] )
		print cmr.get_saved_lease_filepath( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.get_all_saved_lease_filepath_localized( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.get_all_saving_lease_filepath_localized( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.get_all_saving_lease_filefd( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		for fd in cmr.get_all_saving_lease_filefd( hostname = 'A04-QC-HTTPD-0001-VILLE' ):
			print '%s' % ( fd )
			with fd.value[ 'fd' ] as afs:
				with closing( afs.open( fd.value[ 'saved_leases_filepath' ], 'w' ) ) as f:
					pass
				afs.remove( fd.value[ 'saved_leases_filepath' ] )
		print
		print '###############################'
		print '# TEST SUR LES VARIABLES DHCP #'
		print '###############################'
		print cmr.dhcp_dirpath
		print cmr.get_dhcp_filepath( hostname = 'A04-QC-HTTPD-0001-VILLE' )
		print cmr.all_dhcp_dirpath_localized
		for fd in cmr.all_dhcp_dirfd:
			print '%s' % ( fd )
			with fd.value[ 'fd' ] as afs:
				print afs.listdir( fd.value[ 'dhcp_dirpath' ] )
		try:
			print cmr.get_dhcp_filepath( hostname = 'A04-KC-HTTPD-0001-VILLE' )
		except:
			print 'Exception attendue'
		print

if __name__ == "__main__":
	test_module()
