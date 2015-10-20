from __future__ import print_function
from migrant import BaseMigration


class Migration(BaseMigration):
    version = '2015-09-15'

    def migrate(self, obj):
        obj = super(self.__class__, self).migrate(obj)
        if not hasattr(obj, 'l'):
            obj.l = []
        return obj
