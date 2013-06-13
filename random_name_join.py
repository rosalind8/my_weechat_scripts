#!/usr/bin/env python
#-*-coding:utf-8-*-
#Time-stamp: <Fri Jun 14 05:47:59 JST 2013>

import weechat as w
import re
import random

SCRIPT_NAME    = "random_name_join"
SCRIPT_AUTHOR  = "rosalind8"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC    = "random name join ustream"

FIXED_STRING = "ustreamer-"
NUMBERS_DIGITS = 6
CONNECT_SERVER = "ustream"      # from weechat's irc.conf
random_name = ""

def random_join_cb(data, buffer, args):

    text = open("{}/irc.conf".format(w.info_get("weechat_dir","")),"r").readlines()
    channels = ""
    server_num = 0
    for line in text:
        line = line.strip()

        mo = re.findall(r"^ustream.autojoin = \"(.+)\"$", line)
        if mo:
            channels = mo[0]

        nc = re.findall(r"^ustreame(\d+).addresses", line)
        if nc and server_num < int(nc):
            server_num = int(nc)

    cnt = 1
    for ch in channels.split(","):
        # w.prnt("", str(len(channels.split())))
        w.prnt("", ch)
        random_name = FIXED_STRING + random_numbers()
        if cnt > server_num:
            w.command("","/server add ustream{} chat1.ustream.tv/6667 -temp".format(cnt))
        w.command("","/set irc.server.ustream{}.nicks \"{}\"".format(cnt,random_name))
        w.command("","/set irc.server.ustream{}.username \"{}\"".format(cnt,random_name))
        w.command("","/set irc.server.ustream{}.realname \"{}\"".format(cnt,random_name))
        w.command("","/connect ustream{}".format(cnt))
        w.command("","/wait 1 /join -server ustream{} {}".format(cnt,ch))
        cnt += 1
    return w.WEECHAT_RC_OK

def random_numbers():
    nums = []
    for i in xrange(NUMBERS_DIGITS):
        nums.extend(str(random.randint(0,9)))
    return "".join(nums)

if __name__ == '__main__':
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                  SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        w.hook_command("randomjoin",SCRIPT_DESC,
                       "[test]","",
                       "test","random_join_cb","")
