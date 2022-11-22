# -*- coding: utf-8 -*-

import uuid
import base64

def uuid2slug(uuid_hex):
    return uuid.UUID(uuid_hex).bytes.encode('base64').rstrip('=\n').replace('/', '_')

def slug2uuid(slug):
    return str(uuid.UUID(bytes=(slug + '==').replace('_', '/').decode('base64')))

def uuid_short():
    return uuid.uuid4().bytes.encode('base64').rstrip('=\n').replace('/', '_')

def safe_uuid_short():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip('=\n')
