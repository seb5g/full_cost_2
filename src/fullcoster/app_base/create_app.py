""" Create a new app from the jinja2 template directory app_base.activity_base"""


if __name__ == '__main__':
    from jinja2 import Environment, PackageLoader, select_autoescape

    env = Environment(
        loader=PackageLoader("fullcoster.app_base", package_path="activity_template"),
        autoescape=select_autoescape()
    )

    pass