import itertools
from ofjustpy.htmlcomponents import (Stub,
                                     Button_,
                                     Span_,
                                     StackH_,
                                     StackV_,
                                     Input_,
                                     Td_,
                                     Tr_,
                                     Table_ as ojTable_,
                                     Option_,
                                     Select_,
                                     WithBanner_,
                                     Div_,
                                     Slider_,
                                     StackD_,
                                     Halign_,
                                     genStubFunc)
from ofjustpy.ui_styles import  sty
import ofjustpy as oj
from typing import List, AnyStr, Callable, Any
from ofjustpy.icons import chevronright_icon
from ofjustpy.ui_styles import basesty, sty
from ofjustpy.tracker import trackStub
from tailwind_tags import (mr,
                           x,
                           pd,
                           y,
                           W,
                           max as twmax,
                           bg,
                           green,
                           rose,
                           db,
                           space,
                           jc,
                           ovf,
                           auto,
                           full,
                           hidden,
                           pink,
                           conc_twtags,
                           tstr,
                           bsw,
                           cyan,
                           sw,
                           variant,
                           gray,
                           fc,
                           slate,
                           bd,
                           H,
                           top,
                           right,
                           absolute
                           )
from ofjustpy import click
from dpath.util import get as dget
import justpy as jp 

@trackStub
def HierarchyNavigator_(key, hierarchy,  callback_terminal_selected, max_depth=6, max_childs=20, pcp=[], **kwargs):

    # ======================== the child panel =======================
    def on_childbtn_click(dbref, msg):
        #clabel = dbref.text
        #dbref.hinav.selected_child_label = dbref.text

        dbref.hinav.update_ui_child_select(dbref.text)
        pass
    childslots = [Button_(f"cbtn{i}", text=i, value=i, pcp=[
        pd/0, mr/y/0, "hidden"]).event_handle(click, on_childbtn_click) for i in range(max_childs)]

    childpanel_ = StackV_("childpanel", cgens=childslots, pcp=[twmax/W/"md"])

    # updates when child is clicked in childslot

    # ============================== end =============================

    # =========================== the arrows ==========================
    def on_arrow_click(dbref, msg):
        dbref.hinav.arrow_pos = dbref.value
        pass
    # waiting on svelte bug for rendering svg to be fixed 
    # arrows = [Button_(f"btn{i}", chevronright_icon, text="",  value=i, pcp=[mr/x/1]).event_handle(click, on_arrow_click)
    #           for i in range(max_depth)]
    arrows = [Button_(f"btn{i}", text=">",  value=i, pcp=[mr/x/1]).event_handle(click, on_arrow_click)
              for i in range(max_depth)]

    labels = [Span_(f"label{i}", text="", pcp=[mr/x/0])
              for i in range(max_depth)]

    steps = cgens = [StackH_(f"item{i}",
                             cgens=[labels[i], arrows[i]], pcp=[mr/x/0, 'hidden'])
                     for i in range(max_depth)]

    # ============================ end ===========================
    # ========================= update nav ui ========================

    def dummy_event_handler(dbref, message):
        pass
    # ============================== end =============================

    def postrender(dbref, label=labels, arrows=arrows, steps=steps, childslots=childslots
                   ):
        dbref.labels = labels
        dbref.arrows = arrows
        dbref.steps = steps
        dbref.addItems(steps)
        # targets arrows and labels have now been created
        dbref.show_depth = 0
        dbref.arrow_pos = 0
        dbref.steps[0].target.remove_class('hidden')  # root is always open
        dbref.show_path = []
        dbref.hierarchy = hierarchy
        dbref.childslots = childslots

        if 'click' not in dbref.stub.eventhandlers :
            raise ValueError("HierarchyNavigator requires click event handler for required for proper working")
        
        for arrow in arrows:
            arrow.target.hinav = dbref
        for cs in childslots:
            cs.target.hinav = dbref

        def update_ui_child_select(selected_child_label,  hinav=dbref, hierarchy=hierarchy):
            dval = dget(hierarchy, "/" +
                        "/".join([*hinav.show_path, selected_child_label]))
            # print(
            #     f"""{"/" +"/".join([*hinav.show_path, selected_child_label])}""")
            if isinstance(dval, dict):
                hinav.unfold(selected_child_label)
            else:
                terminal_path = f"""{"/" +"/".join([*hinav.show_path, selected_child_label])}"""

                callback_terminal_selected(terminal_path)

        dbref.update_ui_child_select = update_ui_child_select

        def unfold(child_label, hinav=dbref):
            # the unseen arrow
            hinav.show_depth += 1
            fua = hinav.steps[hinav.show_depth]
            fua.target.remove_class('hidden')
            fua.target.set_class('flex') #When hiding flex get taken out
            hinav.labels[hinav.show_depth].target.text = child_label
            hinav.show_path.append(child_label)
            hinav.update_child_panel()
            pass
        dbref.unfold = unfold

        def fold(fold_idx, hinav=dbref):
            # path=self.show_path.split("/")
            for i in range(hinav.show_depth, fold_idx, -1):
                arrstub = dbref.steps[i]
                arrstub.target.set_class('hidden')
                hinav.show_path.pop()
            hinav.show_depth = fold_idx
            dbref.update_child_panel()

        dbref.fold = fold

        def update_child_panel(hinav=dbref):
            for cs in childslots:
                cs.target.set_class('hidden')
                cs.target.text = ""
            showitem = dget(hinav.hierarchy, "/" + "/".join(hinav.show_path))
            for cbtnstub, clabel in zip(childslots,
                                        filter(lambda x : x != '_cref', showitem.keys())
                                        ):
                cbtnstub.target.remove_class('hidden')
                cbtnstub.target.set_class('flex')
                cbtnstub.target.text = clabel
                cbtnstub.target.value = clabel
        dbref.update_child_panel = update_child_panel
        update_child_panel()

    def on_click_hook(dbref, msg):
        """
        if the arrows are clicked then this hook will be called too
        """

        if dbref.show_depth != dbref.arrow_pos:
            dbref.fold(dbref.arrow_pos)
        # TODO: also call any registered events
        pass
    stub = Stub(key, jp.Div, twsty_tags=[
                *pcp, *sty.stackh], postrender=postrender, redirects=[('click', on_click_hook)], **kwargs)
    stub.childpanel_ = childpanel_
    return stub


def Table_(key, values, add_cbox=False):
    def rows_():
        for i, row in enumerate(values):
            def cgens():
                if add_cbox:
                    yield Input_(f"cbox_{i}", type='checkbox', pcp=sty.checkbox, value=str(i))
                for j, item in enumerate(row):
                    yield Td_(f"cell{i}{j}", text=item)
            yield Tr_(f"row_{i}", cgens(), isodd=i%2==1)
    return ojTable_(key, rows_())



def EnumSelector_(key, enumtype):
    enumselect_ = Select_(
        key,
        [Option_(str(_.value), text=str(_.value), value=str(_.value)) for _ in enumtype],
        value=str(next(iter(enumtype)).value)
        )
    return enumselect_
    


@trackStub
def TwoColumnStackV_(key: AnyStr, cgens: List, pcp: List = [], **kwargs):
    bg_colors = [bg/green/1, bg/rose/1]
    idx = 0
    cgen_parts = [[], []]
    for _ in cgens:
        cgen_parts[idx%2].append(_)
        _.update_twsty_tags(bg_colors[(int(idx/2))%2])

        idx = idx + 1


    boxes = [StackV_("leftbox", cgens=cgen_parts[0], pcp=[W/"5/12", space/y/2]),
              StackV_("rightbox", cgens=cgen_parts[1], pcp=[W/"5/12", space/y/2])
              ]
    def postrender(dbref):
        # boxes[0](dbref)
        # boxes[1](dbref)
        pass
    stub = Stub(key,
                jp.Div,
                twsty_tags=[db.f, jc.center, space/x/4, *pcp],
                postrender=postrender,
                cgens = boxes,
                **kwargs)
    return stub


# https://coady.github.io/posts/split-an-iterable/

def chunks(iterable, size):
    """Generate adjacent chunks of data"""
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, size)), ())


#class Dockbar(jp.Div):
    # reactctx=[
    #     ojr.Ctx("/dockbar/dockit", ojr.isstr, ojr.UIOps.DOCK),
    #     ojr.Ctx("/dockbar/undockit", ojr.isstr, ojr.UIOps.UNDOCK),
    # ]
                         
    #@ojr.CfgLoopRunner
    # def undock_eh(dbref, msg):
    #     """
    #     undock event handler
    #     """
    #     dbref.barpanel
    #     msg.value
    #     return "/barpanel/undock", (dbref.barpanel, msg.value)

    # def __init__(self,  **kwargs):
        
    #     super().__init__(**kwargs)

    # def dockit(self, target):
    #     addItems([oj.Button_(target.stub.key + "_dbtn",
    #                                        text=target.stub.key,
    #                                        value = target.stub.spath,
    #                                        ).event_handle(oj.click,
    #                                                       undock_eh)
    #                             ]
    #                            )
            

    #     target.add_twsty_tags(hidden)
    #     print ("need to dock ", target.stub.spath)
    #     pass

    # def undockit(self, target):
    #     dockbtn = self.barpanel.getItem(target.stub)
    #     target_spath = dockbtn.value # need to retrieve from dockbtn
    #     print ("need to undock ", target_spath)
    #     pass


# ============================== dockbar =============================
undock_btn_sty = [bsw.xl,
                      bg/cyan/5,
                      sw/cyan/"500/50",
                      *variant(bg/gray/4,
                                 fc/slate/5,
                                 bd/slate/2,
                                 bsw.none,
                                 rv="disabled")
                                            
                      ]

dock_btn_gen = lambda key: Button_(f"dock_{key}", text="-", pcp=[bg/pink/1, W/6, H/6, top/1, right/1, absolute])



@trackStub
def Dockbar_(key,  cgens = [], pcp:List = [], **kwargs):


    def postrender(dockbar_dbref):
        dockbar_dbref.addItems(dockbar_dbref.stub.undock_btns)
        pass

    def on_undock_click(undock_btn, msg):

        # make sure we make the undock button disappear
        #undock_btn_.target.add_twsty_tags(hidden)
        #find the hero
        undock_btn.stub.thehero_.target.remove_twsty_tags(hidden)
        #undock_btn.add_twsty_tags(hidden)
        undock_btn.disabled = True
        pass

    def on_dock_click(dock_btn, msg):
        dockbar_ = dock_btn.stub.dockbar_
        # minimize button clicked ; make target disapper
        
        # curr_hero_: for lack of better word; is the actual html component/frame/window/ that
        # is being minified
            
        (curr_hero_, undock_btn_) = dockbar_.dock_smap[dock_btn.stub.spath]
        curr_hero_.target.add_twsty_tags(hidden)
        assert  "hidden" in curr_hero_.target.classes

        print("on dock clicked ")
        # unhide the undock button in the dockbar
        # undock_btn_.target.remove_twsty_tags(hidden)
        # assert undock_btn_.thehero_ == curr_hero_
        undock_btn_.target.disabled = False
        
        pass
    
    class DockbarStub(Stub):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.undock_btn_sty = kwargs.get('undock_btn_sty', [])
            self.dock_btn_gen = kwargs.get('dock_btn_gen', None)
            self.undock_btns = []
            self.dock_smap = {}
            
        def dockify(self, dbref_):
            key = dbref_.key
            dock_label = dbref_.kwargs.get("dock_label", key)
            undock_btn_ = oj.Button_(f"undockbtn_{key}",
                                     text=dock_label, disabled=True, 
                                     pcp = [*self.undock_btn_sty]).event_handle(oj.click,
                                                                        on_undock_click)


            undock_btn_.thehero_ = dbref_
            self.undock_btns.append(undock_btn_)
            #undock_btn_.dockbar_ = self
            #self.undock_btns.append(btn_)
            #self.undock_smap[btn_.spath] = dbref_
            #undock_btn_.whotoundock = dbref_
            dock_btn = self.dock_btn_gen(key).event_handle(oj.click,
                                                           on_dock_click)
            #self.dock_btns.append(dock_btn)
            self.dock_smap[dock_btn.spath] = (dbref_, undock_btn_)

            dock_btn.dockbar_ = self
            return dock_btn

    return DockbarStub(key,
                       jp.Div,
                       postrender=postrender,
                       twsty_tags = conc_twtags(*sty.dockbar, *pcp),
                       cgens = cgens,
                       **kwargs
                )

# ============================ end dockbar ===========================

# def Dockbar_(key: AnyStr):
# #     return oj.Div_(key, text="Make me a dockbar")

# # ==================== dockbar utils related stuff ===================
# def build_dockify(dockbar_):
#     """
#     generates the dockify function for dockbar_.
#     usage dockify(dbref_) will make dockify the dbref. i.e.
#     will place a minimizer button. and corresponding undockify 
#     button in the barpanel.
    
#     ideally this functionality should be part of stub class but creating a
#     class for just one use case is not worth it. 
#     """
#     def on_dockbtn_click(dbref, msg):
#         dockbar_.target.dockit(dbref)
#         pass

#     def dockify(dbref_):
#         key = dbref_.key
#         return oj.Button_(f"dockbtn_{key}",
#                    text="", value=dbref_.spath).event_handle(oj.submit,
#                                             on_dockbtn_click)


#     return dockify
            
# # =============================== end: ===============================
def Paginate_(key: AnyStr, cgens: List, num_pages=10, chunk_size=100, container_type= TwoColumnStackV_, pcp: List = [], **kwargs):
    """
    """
    parts = chunks(cgens, chunk_size)
    page_containers = [container_type(f"{key}_container_{cid}",
                                       # cgens=[Span_(f"content_{cid}",
                                       #              text=f"put content here for {cid}" )
                                       #        ]
                                      cgens= achunk,
                                      pcp=[W/full]
                                       )
                       for cid, achunk in enumerate(parts)
                       ]
        
    def postrender(dbref):
        #print ("deck has been initialized")
        pass
        
    page_deck_ = oj.StackD_(f"{key}_deck", cgens=page_containers, postrender=postrender, pcp=[])


    def on_page_id_select(page_selector, msg):
        #print ("page selected = ", msg.value)
        #page_selector.paginate.curr_page = msg.value
        #TODO: do we need to check msg.value
        selected_page = page_containers[int(msg.value)]
        page_deck_.target.bring_to_front(selected_page.spath)
        
        pass
        
    page_selector_ = Halign_(Slider_(f"{key}_slider_i",
                             range(num_pages)).event_handle(oj.click,
                                                            on_page_id_select),
                             align="end")
    return StackV_(key, cgens=[page_selector_, page_deck_], pcp = pcp)

                       

class VForm(jp.Form):
    def validate():
        """
        validate all the inputs in the form
        """
        print ("validate called")
    pass
