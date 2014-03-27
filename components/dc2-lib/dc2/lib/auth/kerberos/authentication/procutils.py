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

import os

try:
    from subprocess import CalledProcessError
except ImportError:
    # Python 2.4 doesn't implement CalledProcessError
    class CalledProcessError(Exception):
        """This exception is raised when a process run by check_call() returns
        a non-zero exit status. The exit status will be stored in the
        returncode attribute."""
        def __init__(self, returncode, cmd):
            self.returncode = returncode
            self.cmd = cmd

        def __str__(self):
            return "Command '{0}' returned non-zero exit status {1}".format(
                self.cmd, self.returncode)

import subprocess
import urllib2


def shell_quote(string):
    return "'" + string.replace("'", "'\\''") + "'"


def run(args, stdin=None, raiseonerr=True,
        nolog=(), env=None, capture_output=True):
    """
    Execute a command and return stdin, stdout and the process return code.
    args is a list of arguments for the command
    stdin is used if you want to pass input to the command
    raiseonerr raises an exception if the return code is not zero
    nolog is a tuple of strings that shouldn't be logged, like passwords.
    Each tuple consists of a string to be replaced by XXXXXXXX.

    For example, the command ['/usr/bin/setpasswd', '--password',
        'Secret123', 'someuser']

    We don't want to log the password so nolog would be set to:
    ('Secret123',)

    The resulting log output would be:

    /usr/bin/setpasswd --password XXXXXXXX someuser

    If an value isn't found in the list it is silently ignored.
    """
    p_in = None
    p_out = None
    p_err = None

    if isinstance(nolog, basestring):
        # We expect a tuple (or list, or other iterable) of nolog strings.
        # Passing just a single string is bad: strings are also, so this
        # would result in every individual character of that string being

        # replaced by XXXXXXXX.
        # This is a sanity check to prevent that.
        raise ValueError('nolog must be a tuple of strings.')

    if env is None:
        # copy default env
        # FIXME: NOW
        env = copy.deepcopy(os.environ)
        env["PATH"] = '/bin:/sbin:/usr/kerberos/bin:/usr/kerberos/sbin:'\
            '/usr/bin:/usr/sbin'
    if stdin:
        p_in = subprocess.PIPE
    if capture_output:
        p_out = subprocess.PIPE
        p_err = subprocess.PIPE
    try:
        p = subprocess.Popen(args, stdin=p_in, stdout=p_out, stderr=p_err,
                             close_fds=True, env=env)
        stdout, stderr = p.communicate(stdin)
        stdout, stderr = str(stdout), str(stderr)  # Make pylint happy
    except KeyboardInterrupt:
        p.wait()
        raise

    # The command and its output may include passwords that we don't want
    # to log. Run through the nolog items.
    args = ' '.join(args)
    for value in nolog:
        if not isinstance(value, basestring):
            continue
        quoted = urllib2.quote(value)
        shquoted = shell_quote(value)
        for nolog_value in (shquoted, value, quoted):
            if capture_output:
                stdout = stdout.replace(nolog_value, 'XXXXXXXX')
                stderr = stderr.replace(nolog_value, 'XXXXXXXX')
            args = args.replace(nolog_value, 'XXXXXXXX')
    if p.returncode != 0 and raiseonerr:
        raise CalledProcessError(p.returncode, args)

    return (stdout, stderr, p.returncode)

