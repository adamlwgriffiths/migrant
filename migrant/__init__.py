from __future__ import print_function
import re
import os
import importlib
import inspect


__module = 'migrations'


def get_module():
    return __module


def set_module(module):
    global __module
    __module = module


class Migrant(object):
    __migrations = []

    version = None

    def __init__(self, *args, **kwargs):
        super(Migrant, self).__init__(*args, **kwargs)
        self.migrate(self)

    @classmethod
    def migration_pattern(cls):
        return re.compile(r'^{clsname}_[^\.]+.py$'.format(clsname=cls.__name__), flags=re.I)

    @classmethod
    def load_migrations(cls):
        module = get_module()
        pattern = cls.migration_pattern()

        path = module.replace('.', '/')
        files = os.listdir(path)
        files = filter(pattern.match, files)
        files = sorted(files)
        cls.__migration_files = files

        strip_extension = lambda x: os.path.splitext(x)[0]
        make_module = lambda x: '.'.join([module, x])

        migrations = [
            importlib.import_module(make_module(strip_extension(f))).Migration()
            for f in files
        ]

        # sort by version
        migrations = sorted(migrations, key=lambda x: x.version)
        cls.__migrations = migrations

    @classmethod
    def migrate(cls, obj):
        # load migrations
        if not cls.__migrations:
            cls.load_migrations()

        # apply migrations in order
        for migration in cls.__migrations:
            if migration.can_migrate(obj):
                obj = migration.migrate(obj)
        return obj


class BaseMigration(object):
    classname = None
    version = None

    def can_migrate(self, obj):
        # check if the object has a classname override
        if self.classname:
            if isinstance(self.classname, type):
                if self.classname != obj.__class__:
                    return False
            else:
                if self.classname != obj.__class__.__name__:
                    return False

        if self.version <= obj.version:
            return False

        return True

    def migrate(self, obj):
        print('Applying migration version: "{}", migration: "{}"'.format(self.version, inspect.getmodule(self).__name__))
        obj.version = self.version
        return obj
