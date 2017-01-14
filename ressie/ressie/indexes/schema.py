from whoosh.fields import SchemaClass, TEXT


class AttackSchema(SchemaClass):
    attack = TEXT(stored=True)
