# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint	import pprint

###########################
# Vision des zones
###########################
class SequentialOps( object ):

   def __init__( self, datas, l_le_op ):
      self._datas 	= datas
      self._l_le_op 	= l_le_op

   def operate( self ):
      datas = self._datas
      for le in self._l_le_op:
         datas = le( datas )
      return datas
