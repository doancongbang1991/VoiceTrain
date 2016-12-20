'''
Created on Dec 18, 2016

@author: BangDoan
'''
import errno
import socket


def get_errno(e):
    try:
        raise e
    
    except socket.timeout as e:
        return errno.ETIMEDOUT
    
    except socket.error as e:
        return e.errno
    
    except Exception as e:
        raise e