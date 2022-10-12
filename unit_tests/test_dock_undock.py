"""
drop down color not working in firefox
"""

from tailwind_tags import *
import ofjustpy as oj
from addict import Dict
import justpy as jp
import ofjustpy_extn as ojx

def on_btn_click(dbref,msg):
    pass

all_colors = [slate , gray , zinc , neutral , stone , red , orange , amber , yellow , lime , green , emerald , teal , cyan , sky , blue , indigo , violet , purple , fuchsia , pink , rose]

app = jp.build_app()
def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    undock_btn_sty = [bsw.xl, bg/cyan/5, sw/cyan/"500/50"]
    dock_btn_gen = lambda key: oj.Button_(f"dock_{key}", text="-", pcp=[bg/pink/1])
    with oj.sessionctx(session_manager):
        with session_manager.uictx("tlctx") as tlctx:
            dockbar_ = ojx.Dockbar_('dockbar',
                                    undock_btn_sty = undock_btn_sty,
                                    dock_btn_gen=dock_btn_gen,
                              
                                    )
            span1_  = oj.Span_("targetSpan1",
                     text="aspan",
                     )
            dock_btn1_  = dockbar_.dockify(span1_)

            span2_  = oj.Span_("targetSpan2",
                     text="aspan",
                     )
            dock_btn2_  = dockbar_.dockify(span2_)
            
        cgens = [span1_, dock_btn1_, span2_, dock_btn2_]
        panel_ = oj.Halign_(oj.StackV_("panel", cgens=cgens))

        wp_ = oj.WebPage_("oa",
                          cgens =[dockbar_, panel_],
                          template_file='svelte.html',
                          title="myoa")
        wp = wp_()
        wp.session_manager = session_manager
        oj.get_svelte_safelist(session_manager.stubStore)
    return wp

#jp.Route("/", launcher)
app.add_jproute("/", launcher)

# ============================== testing =============================
request = Dict()
request.session_id = "abc"

wp = launcher(request)
_sm = wp.session_manager
_ss = _sm.stubStore
msg = Dict()
msg.value = "h"
msg.page = wp
print(_ss.tlctx.keys())
with oj.sessionctx(_sm):
    # dock target1
    _ss.tlctx.dock_targetSpan1.target.on_click(msg)
    # dock target 2
    _ss.tlctx.dock_targetSpan2.target.on_click(msg)

    # undock target 1
    _ss.tlctx.undockbtn_targetSpan1.target.on_click(msg)

        # undock target 1
    _ss.tlctx.undockbtn_targetSpan2.target.on_click(msg)
    

# ================================ end ===============================

# jp.justpy(launcher, start_server=False)

# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/') 
