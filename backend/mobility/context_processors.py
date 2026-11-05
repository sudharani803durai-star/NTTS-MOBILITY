from .models import SiteTheme

def global_site_theme(request):
    try:
        return {"site_theme": SiteTheme.objects.first()}
    except Exception:
        return {"site_theme": None}
