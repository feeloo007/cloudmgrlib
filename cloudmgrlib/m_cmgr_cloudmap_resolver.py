#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from m_cmgr_resolver 	import CloudManagerResolver
from m_cmgr_tools	import is_hostname_valid

class CloudManagerCloudMapResolver( object ):
	def __init__( self ):
		self._cmr 		= CloudManagerResolver()
                self._cached_cloudmap 	= {}
                self._ref_count 	= 0

        def __enter__( self ):
                if not self._cached_cloudmap:
                	self._cached_cloudmap 	= self.cloudmap.copy()
                self._ref_count 		= self._ref_count + 1
                return self

        def __exit__( self, t, v, tr ):
                self._ref_count 	= self._ref_count - 1
                if self._ref_count == 0:
                	self._cached_cloudmap = {}

        def get_cloudmap( self ):
		l_d_dhcp = []
                cloudmap = {}

                if self._cached_cloudmap and self._ref_count > 0:
			return self._cached_cloudmap   

                for fd_dhcp in self._cmr.all_dhcp_dirfd:
                        with fd_dhcp.value[ 'fd' ] as afs_dhcp:
                                for f_dhcp in afs_dhcp.listdir( fd_dhcp.value[ 'dhcp_dirpath' ] ):

                                        @is_hostname_valid
					def load_in_cloudmap( cloudmap, *args, **kwargs ):
						hostname = kwargs[ 'hostname' ]
						matched_hostname = kwargs[ 'matched_hostname' ]

						aera 		= matched_hostname.group( 'ZONE' )
						appcode 	= matched_hostname.group( 'APP_CODE' )
						env	 	= matched_hostname.group( 'ENV' )
						appcomp	= matched_hostname.group( 'COMPOSANT' )
						num_component	= matched_hostname.group( 'NUM_COMPOSANT' )

                                        	if f_dhcp not in [ d.get( 'f_dhcp' ) for d in l_d_dhcp ]:
							l_d_dhcp.append( { 'hostname': hostname, 'f_dhcp': f_dhcp, 'status_file_uniq': True } )
						else:
							[ d for d in l_d_dhcp if d['f_dhcp' ] == f_dhcp ][ 0 ][ 'status_file_uniq' ] = False

						cloudmap.setdefault( 
							aera, 
							{ appcode: { env: { appcomp: { num_component: { } } } } }
						).setdefault( 
							appcode,
							{ env: { appcomp: { num_component: { } } } }
						).setdefault(
							env,
							{ appcomp: { num_component: { } } }
						).setdefault(
							appcomp,
							{ num_component: { } }
						).setdefault( 
							num_component,
							{}
						)[ 'status_file_uniq' ] = [ d[ 'status_file_uniq' ] for d in l_d_dhcp if d[ 'f_dhcp' ] == f_dhcp ][ 0 ]


					try:
						load_in_cloudmap( cloudmap, hostname = f_dhcp.rstrip( '.conf' ) )
					except Exception, e:
						# Filtre les fichiers qui ne matche pas is_hostname_valid
						pass
						#print e
					finally:
						pass
		return cloudmap
        cloudmap = property( get_cloudmap )


	def get_next_hostname_for( self, aera = None , appcode = None, env = None, appcomp = None ):
                prefix_hostname = '%s-%s-%s' % ( appcode, env, appcomp )
		suffix_hostname = '%s' % ( aera )

		return '%s-%04d-%s' % ( 
			prefix_hostname,
			int ( max( self.cloudmap.get(
				aera,
				{ '0000': { 'status_file_uniq': True } }
			).get(
				appcode,
				{ '0000': { 'status_file_uniq': True } }
			).get(
				env,
				{ '0000': { 'status_file_uniq': True } }
			).get(
				appcomp,
				{ '0000': { 'status_file_uniq': True } }
			).keys() ) ) + 1,
			suffix_hostname
		)

        def eval_hostname( self, aera = None , appcode = None, env = None, appcomp = None, num_component = None ):
                return '%s-%s-%s-%s-%s' % ( appcode, env, appcomp, num_component, aera )


def with_cloudmap_resolver( o ):
   """ Décorator recevant en paramètre un objet devant posséder un attribut cloudmap_resolver. 
       L'appel à la fonction fct est habillé d'un d'un 
       with o.cloudmap_resolver as cloudmap_resolver
       La variable ainsi obtenue, est passée à la fonction en l'ajoutant à kwargs sous le nom
       with_cloudmap_resolver
   """

   def wrapper( fct ):
   

      def wrapped( *args, **kwargs ):  

         assert( hasattr( o, 'cloudmap_resolver' ) ), u'%s %s doit posséder un attribut cloudmap_resolver' % ( __name__, o )

         with o.cloudmap_resolver as cloudmap_resolver:

            kwargs.setdefault( 'with_cloudmap_resolver', cloudmap_resolver )

            result = fct( *args, **kwargs )

            return result

      return wrapped

   return wrapper

def with_cloudmap_resolver_for_render( fct ):
   """ Version spécifique du décorator précédent à utiliser sur les méthodes render de nagare """

   def wrapped( self, *args, **kwargs ):      

      assert( hasattr( self, 'cloudmap_resolver' ) ), u'%s %s doit posséder un attribut cloudmap_resolver' % ( __name__, self )

      with self.cloudmap_resolver as cloudmap_resolver:

         kwargs.setdefault( 'with_cloudmap_resolver', cloudmap_resolver )

         result = fct( self, *args, **kwargs )

         return result

   return wrapped

def test_module():

	cmcr =  CloudManagerCloudMapResolver()

	print cmcr.cloudmap
	print cmcr._cached_cloudmap
	print cmcr.get_next_hostname_for( appcode = 'A01', env='QC', appcomp='HTTPD', aera='VILLE' )
	print cmcr.get_next_hostname_for( appcode = 'A02', env='QC', appcomp='HTTPD', aera='VILLE' )
	print cmcr.get_next_hostname_for( appcode = 'A06', env='QC', appcomp='HTTPD', aera='VILLE' )

        with cmcr as c1:
		print cmcr.cloudmap
		print cmcr._cached_cloudmap
        	print 'c1 %s' % CloudManagerCloudMapResolver.get_next_hostname_for( c1, appcode = 'A01', env='QC', appcomp='HTTPD', aera='VILLE' )
                with cmcr as c2:
			print cmcr.cloudmap
			print cmcr._cached_cloudmap
        		print 'c2 %s' % CloudManagerCloudMapResolver.get_next_hostname_for( c2, appcode = 'A01', env='QC', appcomp='HTTPD', aera='VILLE' )
        	print 'c1 %s' % CloudManagerCloudMapResolver.get_next_hostname_for( c1, appcode = 'A01', env='QC', appcomp='HTTPD', aera='VILLE' )
		print cmcr.cloudmap
		print cmcr._cached_cloudmap
	print cmcr.cloudmap
	print cmcr._cached_cloudmap

if __name__ == "__main__":
        test_module()
