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

def launcher(request):
    session_manager = oj.get_session_manager(request.session_id)
    with oj.sessionctx(session_manager):

        cgens = [oj.Span_(f"span_{_}", text=f"span_{_}") for _ in range(0,10)]
        twocolumn_ = oj.Halign_(ojx.TwoColumnStackV_("twocolumn", cgens=cgens, pcp=[W/full]))

        wp_ = oj.WebPage_("oa",
                          cgens =[twocolumn_],
                          template_file='svelte.html',
                          title="myoa")
        wp = wp_()
        #oj.get_svelte_safelist(session_manager.stubStore)
    return wp

jp.Route("/", launcher)

#request = Dict()
#request.session_id = "abc"

#launcher(request)

app = jp.app
# jp.justpy(launcher, start_server=False)

# from starlette.testclient import TestClient
# client = TestClient(app)
# response = client.get('/') 
