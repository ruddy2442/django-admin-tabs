from django.contrib import admin
from django.contrib.admin.options import StackedInline, TabularInline

from example_admintabs_project.example_app.models import Article, Category

from admin_tabs.helpers import TabbedModelAdmin, TabbedPageConfig, Config


class ArticlePageConfig(TabbedPageConfig):
    class FieldsetsConfig:
        titles = Config(fields=["title", "subtitle"], name="Title & Subtitle")
        miscdata = Config(fields=["modified_at", "created_at", "is_online"], name="Dates & State")
        content = Config(name="Content", fields=["content"])
        authors = Config(name="Authors", inline="ArticleToUserInline")
        categories = Config(name="Category", inline="ArticleToCategoryInline")
    
    class ColsConfig:
        content_col = Config(name="Contenu", fieldsets=["content"], css_classes=["col1"])
        titles_col = Config(name="Titles", fieldsets=["titles", "miscdata"], css_classes=["col1"])
        authors_col = Config(name="Authors", fieldsets=["authors"], css_classes=["col1"])
        categories_col = Config(name="Categories", fieldsets=["categories"], css_classes=["col1"])
    
    class TabsConfig:
        main_tab = Config(name="Main", cols=["content_col", "titles_col"])
        secondary_tab = Config(name="Relations", cols=["authors_col", "categories_col"])


class ArticleToUserInline(TabularInline):
    model = Article.authors.through


class ArticleToCategoryInline(StackedInline):
    model = Article.categories.through


class ArticleAdmin(TabbedModelAdmin):
    page_config_class = ArticlePageConfig
    readonly_fields = ('created_at', 'modified_at')
    inlines = (ArticleToUserInline, ArticleToCategoryInline)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)