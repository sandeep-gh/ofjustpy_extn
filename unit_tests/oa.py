import justpy as jp
from ofjustpy_extn import HierarchyNavigator_
from addict import Dict
import ofjustpy as oj
import ofjustpy_styeditor as ojs
from tailwind_tags import *
myhierarchy = {'h1': {'h2': {'h3': {'h4': 1}}}}

def walker(de, kpath="/"):
    yield f"{kpath}{de.stub.key}", de
    for ce in de.components:
        yield from walker(ce, f"{kpath}{de.stub.key}/")

        
def launcher(request):
    session_id = "asession"
    session_manager = oj.get_session_manager(session_id)

    def on_click(dbref, msg):
        pass
    with oj.sessionctx(session_manager):
        hinav_ = HierarchyNavigator_(
            "hinav", myhierarchy).event_handle(oj.click, on_click)

        wp = oj.WebPage_("wp", body_styl=[
            bg/pink/"100/10"], cgens=[])()       
    #wp = jp.WebPage()
    #wp.tailwind = False
    #wp.head_html = """<script src="https://cdn.tailwindcss.com/"></script>"""

    # ================ build wp component hierarch ===============
    component_hierarchy = Dict()
    for cpath, ce in walker(wp):
        ojs.dpathutils.dnew(component_hierarchy, cpath + "/_cref", ce)

    print(component_hierarchy)
    # ================j========= done =========================
    hinav_.childpanel_(wp)
    hinav_(wp)
    with oj.sessionctx(session_manager):
        hinav2_ = HierarchyNavigator_(
            "hinav2", component_hierarchy).event_handle(oj.click, on_click)
    hinav2_.childpanel_(wp)
    hinav2_(wp)
        
    wp.session_manager = session_manager
    
    return wp


# request = Dict()
# request.session_id = "session_id"
# wp = launcher(request)
# stubStore = wp.session_manager.stubStore
# hinav_  = stubStore.hinav
# childpanel_ = hinav_.childpanel_
# #msg = Dict()
# stubStore.cbtn0.target.on_click(None)
# stubStore.cbtn0.target.on_click(None)
#print(hinav_)
app = jp.app
jp.justpy(launcher, start_server=False)

