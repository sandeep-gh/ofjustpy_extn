import justpy as jp
from ofjustpy_extn import HierarchyNavigator_
from addict import Dict
import ofjustpy as oj
myhierarchy = {'h1': {'h2': {'h3': {'h4': 1}}}}


def launcher(request):
    session_id = "asession"
    session_manager = oj.get_session_manager(session_id)

    with oj.sessionctx(session_manager):
        hinav_ = HierarchyNavigator_("hinav", myhierarchy)
    wp = jp.WebPage()
    wp.tailwind = False
    wp.head_html = """<script src="https://cdn.tailwindcss.com/"></script>"""
    hinav_.childpanel_(wp)
    hinav_(wp)
    return wp


request = Dict()
request.session_id = "session_id"
#wp = launcher(request)
app = jp.app
jp.justpy(launcher, start_server=False)
