from consolemenu import SelectionMenu, MenuFormatBuilder
from consolemenu.format import MenuBorderStyleType
from consolemenu.menu_component import Dimension


menu_format = MenuFormatBuilder(max_dimension=Dimension(width=50, height=40)) \
    .set_border_style_type(MenuBorderStyleType.HEAVY_BORDER) \
    .set_title_align('center') \
    .set_subtitle_align('center') \
    .show_header_bottom_border(True) \
    .set_items_left_padding(0)\
    .set_items_top_padding(0)\
    .set_items_bottom_padding(0)\
    .set_items_right_padding(0)


def selection_menu(strings, title):
    menu = SelectionMenu(strings, title, '', False, menu_format)
    menu.show()
    menu.join()
    return menu.selected_option
