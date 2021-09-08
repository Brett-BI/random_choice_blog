import json

def DefaultConverter(obj):
    import datetime

    if isinstance(obj, datetime.datetime):
        return obj.isoformat()