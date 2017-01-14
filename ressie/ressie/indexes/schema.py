from whoosh.fields import SchemaClass, TEXT


class AttackSchema(SchemaClass):
    path = TEXT(stored=True)
    title = TEXT(stored=True)
    attack = TEXT(stored=True)
