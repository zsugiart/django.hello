# In myproject/rpc_app/rpc_methods.py
from modernrpc.core import rpc_method
from django.db import models
from .models import *

# used for system config purpose,
# RPC is not good for decoding objects back

@rpc_method
def hello():
    """
    Say hello to the server.
    """
    return "hello"
