"""
drop down color not working in firefox
"""
import logging
import os

if os:
    try:
        os.remove("launcher.log")
    except:
        pass

import sys
if sys:
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(filename="launcher.log",
                        level=logging.DEBUG, format=FORMAT)

    
from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import ofjustpy_extn as ojx
def on_btn_click(dbref, msg):
    print("clicked select ", dbref.stub.key)
    print ("msg.value = ", msg.value)
    #dbref.value = msg.value
    pass


app = jp.build_app()
all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):

        #cgens = [oj.Span_(f"span_{_}", text=f"span_{_}") for _ in range(0,10)]
        # using bunch of color selectors
        cgens = []
        with session_manager.uictx(f"csuictx") as _csctx:
            for idx in range(0, 20):
                cgens.append(oj.ColorSelector_(f"colorselector_{idx}").event_handle(
                    oj.click, on_btn_click) 
                             )
                # cgens.append(oj.Select_(f"myselect_{idx}",
                #    [oj.Option_(f'red_{idx}', text='red', value='red', pcp=[bg/red/100]),
                #     oj.Option_(f'blue_{idx}', text='blue', value='blue', pcp=[bg/blue/100]),
                #     oj.Option_(f'green_{idx}', text='green', value='green', pcp=[bg/green/100]),

                #     ],
                #    value="red",
                #    pcp=[bg/yellow/1]
                #    ).event_handle(oj.click, on_btn_click))

                    

        twocolumn_ = oj.Halign_(ojx.TwoColumnStackV_("twocolumn", cgens=cgens, pcp=[W/full]))

        wp_ = oj.WebPage_("oa",
                          cgens =[twocolumn_],
                          template_file='svelte.html',
                          title="myoa")
        wp = wp_()
        for spath, stub in oj.dictWalker(session_manager.stubStore):
            print (spath)
            print ("----")
        #oj.get_svelte_safelist(session_manager.stubStore)
    return wp

#jp.Route("/", launcher)
app.add_jproute("/", launcher)
# request = Dict()
# request.session_id = "abc"

# wp = launcher(request)

# app = jp.app
# jp.justpy(launcher, start_server=False)

# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/') 
