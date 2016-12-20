import errno
import socket


def getError(e):
    try:
        raise e
    
    except socket.timeout as e:
        return errno.ETIMEDOUT
    
    except socket.error as e:
        return e.errno
    
    except Exception as e:
        raise e