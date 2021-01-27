from django.conf.urls import url
from django.conf.urls import include
from .views import user, article, tag, category

urlpatterns = [
    url(r'^index.html$',user.index,name='index'),
    url(r'^base-info.html',user.base_info,name='base-info'),
    url(r'^upload-avatar.html$', user.upload_avatar),
    url(r'^tag/(?P<tag_id>\d+).html$', tag.tag, name='tag'),
    url(r'backend/del_tag/', tag.del_tag),
    url(r'backend/add_tag/', tag.add_tag),
    url(r'backend/edit_tag/', tag.edit_tag),
    url(r'^category/(?P<blog_id>\d+).html$', category.category, name='category'),
    url(r'backend/add_category/', category.add_category),
    url(r'backend/del_category/', category.del_category),
    url(r'backend/edit_category/', category.edit_category),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', article.article, name='article'),
    url(r'^article/add_article/', article.add_article),
    url(r'^article/del_article/', article.del_article),
    url(r'^article/edit_article_(?P<art_id>\d+).html', article.edit_article),
    url(r'^upload/', article.upload),
]