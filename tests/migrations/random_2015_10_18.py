from __future__ import print_function
from migrant import BaseMigration


class Migration(BaseMigration):
    version = '2015-10-19'

    def migrate(self, obj):
        obj = super(self.__class__, self).migrate(obj)
        obj.l.append(1)
        return obj
