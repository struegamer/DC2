# -*- coding: utf-8 -*-
#################################################################################
#
#    (DC)² - DataCenter Deployment Control
#    Copyright (C) 2010, 2011, 2012  Stephan Adig <sh@sourcecode.de>
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

def write_pre_post_rules(rule=None, rules=None):
    if rule is not None and rule != "":
        if rules is not None and rules != "":
            rules_array = rules.split("\n")
            for rp in rules_array:
                print "\t%s %s" % (rule, rp)


def write_standard_settings(interface=None):
    if interface is not None:
        if interface.has_key("ip") and interface["ip"] is not None and interface["ip"] != "":
            print "\taddress %s" % interface["ip"]
        if interface.has_key("netmask") and interface["netmask"] is not None and interface["netmask"] != "":
            if 'is_ipv6' in interface and interface['is_ipv6']:
                print "\tprefix %s" % interface["netmask"]
            else:
                print "\tnetmask %s" % interface["netmask"]
        if interface.has_key("gateway") and interface["gateway"] is not None and interface["gateway"] != "":
            print "\tgateway %s" % interface["gateway"]
        if interface.has_key("pre_up") and interface["pre_up"] is not None and interface["pre_up"] != "":
            write_pre_post_rules("pre-up", interface["pre_up"])
        if interface.has_key("post_up") and interface["post_up"] is not None and interface["post_up"] != "":
            write_pre_post_rules("post-up", interface["post_up"])
        if interface.has_key("pre_down") and interface["pre_down"] is not None and interface["pre_down"] != "":
            write_pre_post_rules("pre-down", interface["pre_down"])
        if interface.has_key("post_down") and interface["post_down"] is not None and interface["post_down"] != "":
            write_pre_post_rules("post-down", interface["post_down"])

def write_host_network_configuration(host=None, rpcurl=None):
    if host is not None:
        if host.has_key("interfaces"):
            print "#"
            print "# This file is managed by DataCenter Deployment Control"
            print "#"
            already_auto = {}
            for interface in host["interfaces"]:
                if interface.has_key("type"):
                    print
                    if not already_auto.has_key(interface["name"]):
                        print "auto %s" % interface["name"]
                        already_auto[interface["name"]] = True
                    if 'is_ipv6' in interface and interface["is_ipv6"]:
                        print "iface %s inet6 %s" % (interface["name"], interface["inet"])
                    else:
                        print "iface %s inet %s" % (interface["name"], interface["inet"])
                    if interface.has_key("inet") and interface["inet"] == "static":
                        write_standard_settings(interface)
                    if interface.has_key("inet") and interface["inet"] == "manual":
                        pass
                    if interface["type"] == "bond_2" or interface["type"] == "bond_1":
                        if interface["type"] == "bond_1":
                            print "\tbond-mode 1"
                        elif interface["type"] == "bond_2":
                            print "\tbond-mode 2"
                        print "\tbond-slaves none"
                        print "\tbond-miimon 100"
                        if interface.has_key("slaves"):
                            slave_ints = interface["slaves"].strip()
                            slave_int_arr = slave_ints.split(" ")
                            for slave in slave_int_arr:
                                print
                                print "auto %s" % slave
                                print "iface %s inet manual" % slave
                                print "\tbond-master %s" % interface["name"]
                                print "\tbond-primary %s" % interface["slaves"].strip()
                    if interface["type"] == "vlan":
                        # TODO: Implement
                        pass
