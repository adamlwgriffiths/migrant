from __future__ import print_function
from migrant import BaseMigration


class Migration(BaseMigration):
    version = '2015-09-15'
    classname = 'A'

    def migrate(self, obj):
        obj = super(self.__class__, self).migrate(obj)
        obj.b = 2
        return obj
