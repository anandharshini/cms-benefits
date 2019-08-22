from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu
from django.urls import reverse

from core.decorators import broker_login_required
class UserMenu(Menu):

    name = _("user menu")

    @broker_login_required
    def add_broker_nodes(self):
        nodes = []
        n3 = NavigationNode(_("Manage Employers"), '/crud/employer/employers/?toolbar_off', 3, attr={'visible_for_anonymous': False})
        nodes.append(n3)
        return nodes

    def get_nodes(self, request):
        nodes = []
        # n = NavigationNode(_("Profile"), reverse(profile), 1, attr={'visible_for_anonymous': False}),
        n1 = NavigationNode(_("Log in"), '/accounts/login/', 1, attr={'visible_for_authenticated': False})
        nodes.append(n1)
        n2 = NavigationNode(_("Sign up"), '/signup/?toolbar_off', 2, attr={'visible_for_authenticated': False})
        nodes.append(n2)
        n4 = NavigationNode(_("Log out"), '/accounts/logout/?toolbar_off', 4, attr={'visible_for_anonymous': False})
        nodes.append(n4)
        # broker_nodes = self.add_broker_nodes()
        return nodes
menu_pool.register_menu(UserMenu)
