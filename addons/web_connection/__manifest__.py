{
    "name": "Web -  Connection",
    "version": "16.0.1.0.0",
    "author": "DATN/connection",
    "website": "",
    "category": "Technical",
    "depends": ["base_setup"],
    "external_dependencies": {"python": ["requests"]},
    "data": [
        "security/ir.model.access.csv",
        "views/web_connection.xml",
        "views/res_config_settings.xml",
        "views/web_menu.xml",
    ],
    "assets": {},
    "installable": True,
    "maintainers": [],
}
