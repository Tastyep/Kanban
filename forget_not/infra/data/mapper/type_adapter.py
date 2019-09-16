import uuid


def register_adapters(sql):
    sql.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sql.register_adapter(uuid.UUID, lambda u: u.bytes_le)
