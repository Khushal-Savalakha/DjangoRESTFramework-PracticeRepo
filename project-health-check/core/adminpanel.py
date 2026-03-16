from django.contrib import admin

JAZZMIN_SETTINGS = {
    "site_title": "project_health_check Admin",
    "site_header": "PROJECT_HEALTCH_CHECK",
    "site_brand": "project_health_check",
    "welcome_sign": "PROJECT_HEALTCH_CHECK ADMIN",
    "site_logo": "image/logo.png",
    "topmenu_links": [
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
            "icon": "fas fa-home",
        },
    ],
    # Small text below the logo
    "site_logo_text": "Dashboard",
    # Icon for the site
    "site_icon": None,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "show_ui_builder": False,
}


JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-lightblue",
    "navbar": "navbar-dark navbar-dark-primary",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "litera",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


ADMIN_ORDERING = (
    ("userauth", ("User",)),
    (
        "healthcheck",
        (
            "ProjectDetail",
            "ProjectHealthLog",
            "ProjectNotificationLog",
            "ServerHealthLog",
            "ServerDetails",
            "ServerMonitoringConfig",
            "ServerHealthNotificationLogAdmin",
            "ServerExpiryNotificationLogAdmin"
        ),
    ),
)


# def get_app_list(self, request, app_label=None):
#     app_dict = self._build_app_dict(request, app_label)

#     if not app_dict:
#         return

#     NEW_ADMIN_ORDERING = []
#     if app_label:
#         for ao in ADMIN_ORDERING:
#             if ao[0] == app_label:
#                 NEW_ADMIN_ORDERING.append(ao)
#                 break

#     if not app_label:
#         for app_key, value in list(app_dict.items()):
#             if not any(app_key in ao_app for ao_app in ADMIN_ORDERING):
#                 app_dict.pop(app_key)

#     app_list = sorted(
#         app_dict.values(),
#         key=lambda x: [ao[0] for ao in ADMIN_ORDERING].index(x["app_label"]),
#     )

#     for app, ao in zip(app_list, NEW_ADMIN_ORDERING or ADMIN_ORDERING):
#         if app["app_label"] == ao[0]:
#             for model in list(app["models"]):
#                 # print("---->",model)
#                 if model["object_name"] not in ao[1]:
#                     app["models"].remove(model)
#         app["models"].sort(key=lambda x: ao[1].index(x["object_name"]))
#     return app_list


# admin.AdminSite.get_app_list = get_app_list


def get_app_list(self, request, app_label=None):
    app_dict = self._build_app_dict(request, app_label)

    if not app_dict:
        return

    # ✅ Always remove apps not in ADMIN_ORDERING, regardless of app_label
    for app_key in list(app_dict.keys()):
        if not any(app_key == ao[0] for ao in ADMIN_ORDERING):
            app_dict.pop(app_key)

    if not app_dict:
        return

    NEW_ADMIN_ORDERING = []
    if app_label:
        for ao in ADMIN_ORDERING:
            if ao[0] == app_label:
                NEW_ADMIN_ORDERING.append(ao)
                break

    app_list = sorted(
        app_dict.values(),
        key=lambda x: [ao[0] for ao in ADMIN_ORDERING].index(x["app_label"]),
    )

    for app, ao in zip(app_list, NEW_ADMIN_ORDERING or ADMIN_ORDERING):
        if app["app_label"] == ao[0]:
            for model in list(app["models"]):
                if model["object_name"] not in ao[1]:
                    app["models"].remove(model)
        app["models"].sort(key=lambda x: ao[1].index(x["object_name"]))

    return app_list

admin.AdminSite.get_app_list = get_app_list