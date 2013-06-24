#!/usr/bin/env python
#-*-coding:utf-8-*-
#Time-stamp: <Mon Jun 24 19:24:19 JST 2013>

import weechat as w
import re
import time
from pyquery import PyQuery as pq


SCRIPT_NAME    = "search"
SCRIPT_AUTHOR  = "rosalind8"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC    = "search ustream"

def stick(ip):
    url = "http://sticker.mine.nu/scope?q={}".format(ip)
    d = pq(url, parser='html')

    lst = d.find('tr')
    ret_list = []
    ml=lst[2:11] if len(lst)>11 else lst[2:]
    for tr in ml:
        l = pq(tr).find('td')

        number = pq(l[0]).text()
        login_time = re.search(r"localTime\((\d+)\);",pq(l[1]).text()).group(1)
        login_names_list = [pq(n).text() for n in pq(l[2]).find('a')]
        login_channels = pq(l[4]).text()
        ret_list.append(dict(number=number,
                             login_time=time.strftime("%m/%d %H:%M:%S",
                                                      time.localtime(int(login_time))),
                             login_nick=login_names_list,
                             login_channels=login_channels))
    return ret_list

def search_whois_cb(data, signal, hashtable):
    ht = hashtable['output']    # string
    ret = re.search(r"(\S+) \* :(.+)$", ht, re.M)
    if ret:
        masked_ip = ret.group(1)
        w.prnt_date_tags("", 0, "no_log", "RESULT about {}{}".format(w.color("*lightblue"),masked_ip))
        lst = stick(masked_ip)
        for dic in lst:
            w.prnt_date_tags("", 0,
                             "no_log",
                             "\n  ".join(["{}#{}: {}".format(w.color("_lightgreen"),
                                                             dic['number'],
                                                             dic['login_time']),
                                          "names: {}{}{} / {} / {}".format(w.color("*lightred"),
                                                           dic['login_nick'][0],
                                                           w.color("chat"),
                                                           dic['login_nick'][1],
                                                           dic['login_nick'][2]),
                                          "channels: {}".format(dic['login_channels'])
                                      ]))
    # else:
    #     w.prnt_date_tags("", 0, "no_log", "error: Not Found MASKED_IP")
    return w.WEECHAT_RC_OK

def search_cb(data,buffer,args):
    w.hook_hsignal("irc_redirection_search_whois", "search_whois_cb", "")
    w.hook_hsignal_send("irc_redirect_command",
                        { "server": w.buffer_get_string(buffer,"name").split(".")[0], # <- server name
                          "pattern": "whois",
                          "signal": "search",
                          "string": "" })
    w.command(w.current_buffer(), "/whois {}".format(args))
    return w.WEECHAT_RC_OK

if __name__ == '__main__':
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                  SCRIPT_LICENSE, SCRIPT_DESC, "", ""):

        w.hook_command("search", SCRIPT_DESC,
                       "[nick]", "",
                       "%(nicks)", "search_cb", "")
