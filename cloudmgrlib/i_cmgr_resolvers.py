from __future__			import with_statement
from m_cmgr_resolver		import CloudManagerResolver
from m_cmgr_appcode_resolver    import CloudManagerAppcodeResolver
from m_cmgr_appcomp_resolver    import CloudManagerAppCompResolver
from m_cmgr_env_resolver        import CloudManagerEnvResolver
from m_cmgr_aera_resolver       import CloudManagerAeraResolver
from m_cmgr_cloudmap_resolver	import CloudManagerCloudMapResolver

class ICloudMgrResolvers( object ):
    def __init__( self, resolvers = None ):

        if hasattr( resolvers, '_resolver' ):
            self._resolver = resolvers._resolver
        else:
            self._resolver = CloudManagerResolver() 

        if hasattr( resolvers, '_appcode_resolver' ):
            self._appcode_resolver = resolvers._appcode_resolver
        else:
            self._appcode_resolver = CloudManagerAppcodeResolver() 

        if hasattr( resolvers, '_appcomp_resolver' ):
            self._appcomp_resolver = resolvers._appcomp_resolver
        else:
            self._appcomp_resolver = CloudManagerAppCompResolver() 

        if hasattr( resolvers, '_env_resolver' ):
            self._env_resolver = resolvers._env_resolver
        else:
            self._env_resolver = CloudManagerEnvResolver() 

        if hasattr( resolvers, '_aera_resolver' ):
            self._aera_resolver = resolvers._aera_resolver
        else:
            self._aera_resolver = CloudManagerAeraResolver() 

        if hasattr( resolvers, '_cloudmap_resolver' ):
            self._cloudmap_resolver = resolvers.cloudmap_resolver
        else:
            self._cloudmap_resolver = CloudManagerCloudMapResolver() 

    def get_resolver( self ):
        return self._resolver
    resolver = property( get_resolver )

    def get_appcode_resolver( self ):
        return self._appcode_resolver
    appcode_resolver = property( get_appcode_resolver )

    def get_appcomp_resolver( self ):
        return self._appcomp_resolver
    appcomp_resolver = property( get_appcomp_resolver )

    def get_env_resolver( self ):
        return self._env_resolver
    env_resolver = property( get_env_resolver )

    def get_aera_resolver( self ):
        return self._aera_resolver
    aera_resolver = property( get_aera_resolver )

    def get_cloudmap_resolver( self ):
        return self._cloudmap_resolver
    cloudmap_resolver = property( get_cloudmap_resolver )
