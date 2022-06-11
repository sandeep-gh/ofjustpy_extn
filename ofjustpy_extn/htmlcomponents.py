from ofjustpy.htmlcomponents import HCC, Stub, Button_, Span_, StackH_, StackV_, Input_, Td_, Tr_, Table_ as ojTable_, Option_, Select_, WithBanner_
import ofjustpy as oj
from ofjustpy.icons import chevronright_icon
from ofjustpy.ui_styles import basesty, sty
from ofjustpy.tracker import trackStub
from tailwind_tags import mr, x, pd, y
from ofjustpy import click
from dpath.util import get as dget


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

    childpanel_ = StackV_("childpanel", cgens=childslots)

    # updates when child is clicked in childslot

    # ============================== end =============================

    # =========================== the arrows ==========================
    def on_arrow_click(dbref, msg):
        print("arrow clicked: folding till level ",  dbref.value)
        dbref.hinav.arrow_pos = dbref.value
        pass
    arrows = [Button_(f"btn{i}", chevronright_icon, text="",  value=i, pcp=[mr/x/1]).event_handle(click, on_arrow_click)
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

        print("event handles ", dbref.stub.eventhandlers)
        if 'click' not in dbref.stub.eventhandlers :
            raise ValueError("HierarchyNavigator requires click event handler for required for proper working")
        
        for arrow in arrows:
            arrow.target.hinav = dbref
        for cs in childslots:
            cs.target.hinav = dbref

        def update_ui_child_select(selected_child_label,  hinav=dbref, hierarchy=hierarchy):
            print(f"in update_ui_child_select {selected_child_label}")
            dval = dget(hierarchy, "/" +
                        "/".join([*hinav.show_path, selected_child_label]))
            print(
                f"""{"/" +"/".join([*hinav.show_path, selected_child_label])}""")
            if isinstance(dval, dict):
                hinav.unfold(selected_child_label)
            else:
                terminal_path = f"""{"/" +"/".join([*hinav.show_path, selected_child_label])}"""
                print("Hierarchy component: at terminal point")
                callback_terminal_selected(terminal_path)

        dbref.update_ui_child_select = update_ui_child_select

        def unfold(child_label, hinav=dbref):
            # the unseen arrow
            hinav.show_depth += 1
            fua = hinav.steps[hinav.show_depth]
            print("fua = ", fua.target.classes)
            fua.target.remove_class('hidden')
            print("fua = ", fua.target.classes)
            hinav.labels[hinav.show_depth].target.text = child_label
            hinav.show_path.append(child_label)
            print("unfolded: new depth ", hinav.show_depth, " new path :", hinav.show_path )
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
            print("post fold ", hinav.show_depth)
            dbref.update_child_panel()

        dbref.fold = fold

        def update_child_panel(hinav=dbref):
            for cs in childslots:
                cs.target.set_class('hidden')
                cs.target.text = ""
            showitem = dget(hinav.hierarchy, "/" + "/".join(hinav.show_path))
            print("update_child_panel: childpanel refreshed: new child labels = ", showitem.keys())
            for cbtnstub, clabel in zip(childslots, showitem.keys()):
                cbtnstub.target.remove_class('hidden')
                cbtnstub.target.text = clabel
                cbtnstub.target.value = clabel
        dbref.update_child_panel = update_child_panel
        update_child_panel()

    def on_click_hook(dbref, msg):
        """
        if the arrows are clicked then this hook will be called too
        """
        print("hinav clicked called ", dbref.show_depth, " ", dbref.arrow_pos)
        if dbref.show_depth != dbref.arrow_pos:
            dbref.fold(dbref.arrow_pos)
        # TODO: also call any registered events
        pass
    stub = Stub(key, HCC, twsty_tags=[
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



@trackStub
def EnumSelector_(key, enumtype, label=None, on_select=None):
    if not label:
        label = enumtype.__name__
    enumselect_ = Select_(
        "selector",
        [Option_(str(_.value), text=str(_.value), value=str(_.value)) for _ in enumtype],
        value=str(next(iter(enumtype))).value)
    if on_select:
        enumselect_.event_handle(oj.change, on_select)
    return WithBanner_(key, label, enumselect_)
    
    
