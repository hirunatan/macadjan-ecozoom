from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
from django.conf import settings
from django.contrib.sites.models import Site
from macadjan import models
from macadjan_ecozoom import models as models_ecozoom
from treemenus import models as models_menus
#from themes import models as models_themes

class Command(BaseCommand):
    args = '<instance_slug> <instance_domain>'
    help = 'Initialize a newly created instance, by setting Site and SiteInfo, creating a menu and a theme.\n' \
           'You need to give the slug of the instance and also the public domain. For example:\n' \
           '  ./manage.py initialize_instance demo demo.mapunto.net'

    def handle(self, *args, **options):

        if len(args) != 2:
           return 'You need to give the slug of the instance and also the public domain. For example:\n' \
                  '  ./manage.py initialize_instance demo demo.mapunto.net\n'

        self.instance_slug = args[0]
        self.instance_domain = args[1]

        translation.activate(settings.LANGUAGE_CODE)

        current_site = self.init_current_site()
        current_site_info = self.init_current_site_info(current_site)
        main_menu = self.init_main_menu()
        #theme = self.init_theme(current_site)

        translation.deactivate()


    def init_current_site(self):
        current_site = Site.objects.get_current()
        current_site.name = self.instance_domain
        current_site.domain = self.instance_domain
        current_site.save()
        return current_site


    def init_current_site_info(self, current_site):
        try:
            current_site_info = current_site.site_info
        except models.SiteInfo.DoesNotExist:
            current_site_info = models.SiteInfo(site = current_site)
        current_site_info.website_name = self.instance_domain
        current_site_info.website_subtitle = ''
        current_site_info.website_description = ''
        current_site_info.footer_line = self.instance_domain
        current_site_info.map_bounds_left = -20037508.34
        current_site_info.map_bounds_right = 20037508.34
        current_site_info.map_bounds_bottom = -20037508.34
        current_site_info.map_bounds_top = 20037508.34
        current_site_info.map_zoom_levels = 18
        current_site_info.map_max_resolution = 156543
        current_site_info.map_units = 'meters'
        current_site_info.map_initial_lon = -3.86
        current_site_info.map_initial_lat = 48.38
        current_site_info.map_initial_zoom = 6
        current_site_info.new_entity_proposal_enabled = False
        current_site_info.entity_change_proposal_enabled = False
        current_site_info.description_hints = ''
        current_site_info.goals_hints = ''
        current_site_info.finances_hints = ''
        current_site_info.social_values_hints = ''
        current_site_info.how_to_access_hints = ''
        current_site_info.networks_member_hints = ''
        current_site_info.networks_works_with_hints = ''
        current_site_info.ongoing_projects_hints = ''
        current_site_info.needs_hints = ''
        current_site_info.offerings_hints = ''
        current_site_info.additional_info_hints = ''
        current_site_info.save()
        return current_site_info


    def init_main_menu(self):
        try:
            main_menu = models_menus.Menu.objects.get(name = 'main_menu')
        except models_menus.Menu.DoesNotExist:
            main_menu = models_menus.Menu(name = 'main_menu')

        root_menu_item = main_menu.root_item
        if not root_menu_item:
            root_menu_item = models_menus.MenuItem(menu = main_menu)
        root_menu_item.parent = None
        root_menu_item.caption = u'Root'
        root_menu_item.url = u''
        root_menu_item.named_url = u''
        root_menu_item.level = 0
        root_menu_item.rank = 0
        root_menu_item.save()

        main_menu.root_item = root_menu_item
        main_menu.save()

        try:
            menu_item = root_menu_item.menuitem_set.get(url = '/map/')
        except models_menus.MenuItem.DoesNotExist:
            menu_item = models_menus.MenuItem(parent = root_menu_item,
                                              menu = main_menu,
                                              url = '/map/')
        menu_item.caption = u'Mapa'
        menu_item.named_url = u''
        menu_item.level = 0
        menu_item.rank = 0
        menu_item.save()

        return main_menu

#    def init_theme(self, current_site):
#        themes = models_themes.Theme.objects.all()
#        if len(themes) > 1:
#            raise ValueError("There are more than 1 theme, i don't know how to handle this")
#        if len(themes) == 1:
#            theme = themes[0]
#        else:
#            theme = models_themes.Theme()
#
#        theme.name = self.instance_slug
#        theme.directory = self.instance_slug
#        theme.save()
#
#        theme.sites_available.clear()
#        theme.sites_available.add(current_site)
#        theme.sites_enabled.clear()
#        theme.sites_enabled.add(current_site)

