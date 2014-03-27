# -*- coding: utf-8 -*-
#
# (DC)² - DataCenter Deployment Control
# Copyright (C) 2010, 2011, 2012, 2013, 2014 Stephan Adig <sh@sourcecode.de>
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

import logging


LOG_INFO = 1
LOG_DEBUG = 10


class AppLogger(object):
    def __init__(self, logger=None):
        if logger is None:
            self._logger = self._init_logging()
        else:
            self._logger = logger

    def _init_logging(self):
        # FIXME: ASAP
        logger = logging.getLogger('DEFAULT_APP_LOGGER')
        logger.setLevel(LOGLEVEL)

        fh = logging.FileHandler(LOGFILE)
        fh.setLevel(LOGLEVEL)
        formatter = logging.Formatter(LOGFORMAT)
        fh.setFormatter(formatter)

        logger.addHandler(fh)
        return logger

    def log(self, severity=LOG_DEBUG, logmsg=''):
        if severity == LOG_DEBUG:
            self._logger.debug(logmsg)
        if severity == LOG_INFO:
            self._logger.info(logmsg)
