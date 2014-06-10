# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011  Stephan Adig <sh@sourcecode.de>
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#################################################################################

import sys
import os
import os.path
import datetime
import logging

from settings import *

try:
    from OpenSSL import crypto
except ImportError, e:
    print e
    sys.exit(1)

import web
from sslexceptions import *
from ssl_constants import *

MODULE_NAME = "ssllib"
MODULE_FILE_NAME = "keys"

module_logger = logging.getLogger("%s.%s.%s" % (APPNAME, MODULE_NAME, MODULE_FILE_NAME))

 
def ssl_key_create(key_type=TYPE_RSA, bits_per_key=2048):
    if key_type != TYPE_DSA and key_type != TYPE_RSA:
        module_logger.debug("ssl_create_key: Wrong Key Type, not TYPE_RSA or TYPE_DSA")
        raise SSLKeyTypeException("Wrong Key Type, not TYPE_RSA or TYPE_DSA")    
    key = crypto.PKey()
    key.generate_key(key_type, bits_per_key)
    return key

def ssl_key_export(key=None, cipher=None, passphrase=None):
    if key is None:
        module_logger.debug("ssl_dump_key: No Key passed to method")
        raise SSLNoKeyException("No Key passed to method")
    
  
    if cipher is not None and cipher.lower() not in KEY_CIPHERS:
        module_logger.debug("ssl_dump_key: Cipher not in valid Cipher list")
        raise SSLInvalidCipherException("Cipher not in valid Cipher list")
    if cipher is not None and cipher.lower() not in KEY_CIPHERS and passphrase is not None and passphrase == "":
        module_logger.debug("ssl_dump_key: Passphrase given but empty")
        raise SSLEmptyPassphraseException("Passphrase given but empty")
    key_dump = ""
    if passphrase is None:
        key_dump = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
    else:
        if cipher in KEY_CIPHERS:
            key_dump = crypto.dump_privatekey(crypto.FILETYPE_PEM, key, cipher, passphrase)
    return key_dump

def ssl_key_import(key_dump=None, passphrase=None):
    if key_dump is None:
        #FIXME: named exception
        raise Exception("bla")
    if passphrase is None:
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_dump)
    else:
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_dump, passphrase)
    return key

    
    
 
