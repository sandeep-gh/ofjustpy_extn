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

def terminal_node_callback(spath):
    print ('terminal node selected', spath)
    pass
            
def launcher(request):
    session_id = "asession"
    session_manager = oj.get_session_manager(session_id)
    stubStore = session_manager.stubStore
    def on_click(dbref, msg):
        pass
    def on_btn_click(dbref, msg):

        pass

    def on_input_change(dbref, msg):

        pass
    
    with oj.sessionctx(session_manager):
        hinav_ = HierarchyNavigator_(
            "hinav", myhierarchy, terminal_node_callback).event_handle(oj.click, on_click)
        def stubs():
            for _ in [oj.Circle_("mycircle", text="myc").event_handle(oj.click, on_btn_click),

                      oj.Span_("myspan", text="span text"),
                      oj.A_("myA", text="myurl", href="myurl"),
                      oj.P_("myP", text="my looooongins para"),
                      ]:
                yield _

        mystackv = oj.Halign_(oj.StackV_(
            "mystackv", cgens=[oj.Halign_(stub) for stub in stubs()]))
        
        wp = oj.WebPage_("wp", body_styl=[
            bg/pink/"100/10"], cgens=[mystackv], template_file='svelte.html', title="a hierarchy navigator")()       

    # ================ build wp component hierarch ===============
    component_hierarchy = Dict()
    for cpath, ce in walker(wp):
        ojs.dpathutils.dnew(component_hierarchy, cpath + "/_cref", ce)

    # ================j========= done =========================
    hinav_.childpanel_(wp)
    hinav_(wp)

    with oj.sessionctx(session_manager):
        hinav2_ = HierarchyNavigator_(
            "hinav2", component_hierarchy, terminal_node_callback).event_handle(oj.click, on_click)
        oj.StackW_("hinavViewPanel",
                cgens = [
                    hinav2_.childpanel_,
                    oj.Prose_("content", text="tons and tons of lots of text", pcp=[max/W/"prose"])]
                )

        oj.StackV_("hinavPanel", cgens = [stubStore.hinavViewPanel, hinav2_])
        oj.Container_("tlc", cgens = [stubStore.hinavPanel], pcp=[bg/pink/"100/20"])
        #hinav2_.childpanel_(wp)
        #hinav2_(wp)
        stubStore.tlc(wp)
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




















