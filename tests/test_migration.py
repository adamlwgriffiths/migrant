import unittest
import re
try:
    import jaweson
    from jaweson import json
except:
    pass
import migrant
from migrant import Migrant


class TestSerialiser(unittest.TestCase):
    def setUp(self):
        migrant.set_module('tests.migrations')

    def test_custom_migration_name(self):
        class TestMigrant(Migrant):
            @classmethod
            def migration_pattern(cls):
                return re.compile(r'^random_[^\.]+\.py$', flags=re.I)

        t = TestMigrant()
        t.migrate(t)
        assert t.l == [1]

        # migrating again, should not do anything
        # can check be ensuring the new list is still [1]
        t.migrate(t)

        assert t.l == [1]

    @unittest.skipIf('jaweson' not in globals(), 'Jawson not available')
    def test_jaweson_migration(self):
        class A(jaweson.Serialisable, Migrant):
            def __init__(self):
                self.a = 1

        a = A()
        assert a.a is 1
        assert not hasattr(a, 'b')
        a = json.loads(json.dumps(a))
        assert a.a is 1
        assert not hasattr(a, 'b')

        a = a.migrate(a)
        assert a.a is 1
        assert hasattr(a, 'b')
        assert a.b is 2

        a = json.loads(json.dumps(a))
        assert a.a is 1
        assert hasattr(a, 'b')
        assert a.b is 2
