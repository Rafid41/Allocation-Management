# App_Admin_Panel/templatetags/nav_CDB_links_loader.py
from django import template
from django.contrib.staticfiles.finders import find
import os

register = template.Library()

@register.simple_tag
def external_link_from_static(filename):
    """
    Find and return trimmed content of static/links/<filename>.
    Usage:
        {% external_link_from_static "Central_Database_Gateway.txt" as central_database_gateway_link %}
    Returns empty string on failure.
    """
    # Accept either "Central_Database_Gateway.txt" or "links/Central_Database_Gateway.txt"
    subpath = filename
    if not subpath.startswith("links" + os.sep) and not subpath.startswith("links/"):
        subpath = os.path.join("links", filename)

    # Use staticfiles finders so it works in dev and after collectstatic
    file_path = find(subpath)
    if not file_path:
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""
