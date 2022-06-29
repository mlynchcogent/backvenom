#!/usr/bin/env python3
class ErrorStartingListener(Exception):
    """Raised when listener is alredy started"""
    pass

class InvalidPayload(Exception):
    """Raised when not valid payload (x-D)"""
    pass

class InvalidPort(Exception):
    """Raised when not valid port"""
    pass
