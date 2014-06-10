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

from OpenSSL import crypto

TYPE_DSA = crypto.TYPE_DSA
TYPE_RSA = crypto.TYPE_RSA

KEY_CIPHERS = (
             "des",
             "des3",
             "aes128",
             "aes192",
             "aes256"
             )
CSR_DIGESTS = (
             "md5",
             "sha1",
             "md2",
             "mdc2",
             "md4"
             )
DIGESTS = (
         'md5',
         'md4',
         'md2',
         'sha1',
         'sha',
         'sha224',
         'sha256',
         'sha384',
         'sha512',
         'mdc2',
         'ripemd160'
)

SUBJECTS = (
          'CN',
          'C',
          'ST',
          'L',
          'O',
          'OU',
          )

REVOKE_REASONS = (
                'unspecified',
                'keyCompromise',
                'CACompromise',
                'affiliationChanged',
                'superseded',
                'cessationOfOperation',
                'certificateHold',
                'removeFromCRL',
)


