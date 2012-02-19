import sys
import os
import os.path
import subprocess
import time

SUPPORTED_DISTROS=["ubuntu","debian"]

def do_mirror(config=None,dist_type=None):
    if config is None:
        return None
    if config.has_key("distributions") and config["distributions"] is not None:
        distributions=config["distributions"]
        if dist_type is not None:
            if dist_type=="all":
                for distro in SUPPORTED_DISTROS:
                    if distributions.has_key(distro):
                        do_mirror_job(config["config"],distributions[distro],distro)
            else:
                do_mirror_job(config["config"],distributions[dist_type],dist_type)

def do_mirror_job(default_config=None, distributions=None,distro_type=None):
    if default_config is None or distributions is None and distro_type is None:
        return None
    if distro_type in ["ubuntu","debian"]:
        do_debian_mirror_job(default_config,distributions,distro_type)

def do_debian_mirror_job(default_config=None, distributions=None, distro_type=None):
    if default_config is None or distributions is None and distro_type is None:
        return None
    if distributions.has_key("releases") and distributions["releases"] is not None:
        for key in distributions["releases"]:
            call_args=[]
            call_args.append("/usr/bin/debmirror")
            call_args.append("--progress")
            call_args.append("--verbose")
            call_args.append("--nosource")
	    release=distributions["releases"][key]
            if release.has_key("sections") and release["sections"] is not None:
                call_args.append("--section=%s" % release["sections"])
            else:
                call_args.append("--section=%s" % distributions["defaults"]["sections"])
            if release.has_key("arch") and release["arch"] is not None:
                call_args.append("--arch=%s" % release["arch"])
            else:
                call_args.append("--arch=%s" % distributions["defaults"]["arch"])
            if release.has_key("host") and release["host"] is not None:
                call_args.append("--host=%s" % release["host"])
            else:
                call_args.append("--host=%s" % distributions["defaults"]["host"])
            if release.has_key("method") and release["method"] is not None:
                call_args.append("--method=%s" % release["method"])
            else:
                call_args.append("--method=%s" % distributions["defaults"]["method"])

            if release.has_key("rootdir") and release["rootdir"] is not None:
                call_args.append("--root=%s" % release["rootdir"])
            else:
                call_args.append("--root=%s" % distributions["defaults"]["rootdir"])

            if release.has_key("stable") and release["stable"] is not None:
                if release["stable"] is True:
                    if distro_type=="ubuntu":
                        call_args.append("--dist=%s,%s-security,%s-updates" % (key,key,key))
                    if distro_type=="debian":
                        call_args.append("--dist=%s,%s-updates" % (key,key))
                else:
                    call_args.append("--dist=%s" % key)
            else:
                if distributions["defaults"]["stable"] is True:
                    if distro_type=="ubuntu":
                        call_args.append("--dist=%s,%s-security,%s-updates" % (key,key,key))
                    if distr_type=="debian":
                        call_args.append("--dist=%s,%s-updates" % (key,key))
                else:
                    call_args.append("--dist=%s" % key)

            if release.has_key("mirror_directory") and release["mirror_directory"] is not None:
                call_args.append(release["mirror_directory"])
            elif distributions["defaults"].has_key("mirror_directory") and distributions["defaults"]["mirror_directory"] is not None:
                call_args.append(distributions["defaults"]["mirror_directory"])
            else:
                call_args.append(default_config["mirror_directory"])
            subprocess.call(call_args)




