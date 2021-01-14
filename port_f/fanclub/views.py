from django.views.generic.base import TemplateView


# 메인화면
class IndexView(TemplateView):
    template_name = 'index.html'

    
