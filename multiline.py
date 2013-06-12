#-*- coding:utf-8 -*-
"""
出来れば、tkinterの部分をバックグラウンドプロセスとして処理して
"""

import weechat as w
import Tkinter as tk
import re

SCRIPT_NAME    = "multiline"
SCRIPT_AUTHOR  = "oidu7"
SCRIPT_VERSION = "1.0"
SCRIPT_LICENSE = "GPL"
SCRIPT_DESC    = "assist to use multi line comment"

ml_font = 'KGCG-W4_NAA'            # as much as possible, use font supported AA
ml_text = ""
ml_flag = False
ml_t = ml_root = None

def multi_line_text():
    global ml_root, ml_t
    ml_root = tk.Tk()
    ml_root.option_add('*font', (ml_font, 12))
    ml_root.title('multi line text')
    ml_t = tk.Text(ml_root,width=30,height=10,state=tk.NORMAL)
    ml_t.pack(expand=True)
    b = tk.Button(ml_root,text='say (press Space)',command=ml_destroy)
    b.pack(expand=True)
    ml_t.focus_set()
    ml_root.mainloop()

def ml_destroy():
    global ml_text, ml_flag
    ml_text = ml_t.get("1.0",tk.END)
    ml_flag = True
    ml_root.destroy()

def multi_line_cb(data,buffer,args):
    global ml_text,ml_flag
    if args == "test" or args=="":
        multi_line_text()
        if ml_flag:
            ml_text = re.sub("\s+$","",ml_text)
            if args == "test":
                w.prnt_date_tags(w.current_buffer(), 0, "no_log", ml_text.encode('utf-8'))
            elif args == "":
                w.command(w.current_buffer(), ml_text.encode('utf-8'))
            ml_text = ""
            ml_flag = False
    else:
        w.prnt_date_tags(w.current_buffer(), 0, "no_log", "%smultiline: args '%s' is not defined" % (w.prefix('error'),args))

    return w.WEECHAT_RC_OK

if __name__ == '__main__':
    if w.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION,
                  SCRIPT_LICENSE, SCRIPT_DESC, "", ""):
        w.hook_command("ml",SCRIPT_DESC,
                       "[test]","",
                       "test","multi_line_cb","")
