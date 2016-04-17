"""
confi.gs cidrfield migration operations.
"""
from django.db.migrations.operations.base import Operation


class AddCidrIndex(Operation):
    """
    django migration operation to define an inet_ops GiST index for a field.
    """

    reversible = True

    def __init__(self, table, field):
        self.table = table
        self.field = field

    def database_forwards(self, app_label, schema_editor, from_state,
                          to_state):
        schema_editor.execute(
            "CREATE INDEX %(table)s_%(field)s_cidr ON %(table)s \
             USING gist (inet(%(field)s) inet_ops)" % {'table': self.table,
                                                       'field': self.field}
        )

    def database_backwards(self, app_label, schema_editor, from_state,
                           to_state):
        schema_editor.execute(
            "DROP INDEX %(table)s_%(field)s_cidr" % {'table': self.table,
                                                     'field': self.field}
        )

    def describe(self):
        return "Creates index on cidr field %s in table %s" % \
               (self.field, self.table)

    def state_forwards(self, app_label, state):
        pass
