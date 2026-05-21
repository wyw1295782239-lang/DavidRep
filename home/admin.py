from django.contrib import admin
from home.models import TravelInfo, Review, PageVisit

class TravelInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'province','rating','review_count','actual_price','is_free','popularity_score')
    list_display_links=('name','city')
    #可筛选的字段
    list_filter=('province','city','is_free','is_ad','is_recommended')
    #可检索的字段
    search_fields=('name','city','province','tags')
    #分页设置
    list_per_page=50
    #按某些字段排序
    ordering=('-review_count',)
    #编辑页面的分组情况
    fieldsets=(
    ('基本信息',{'fields':('name','city','province','tags')}),
    ('评分与热度',{'fields':('rating','review_count','popularity_score','is_recommended')}),
    ('价格信息',{'fields':('market_price','discount_price','actual_price','is_free')}),
    ('位置信息',{'fields':('longtitude','latitude','distance_from_center')}),
    ('其他信息',{'fields':('is_ad','image_url','detail_link')})
     )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('spot', 'username', 'rating', 'content', 'created_at')
    list_display_links = ('spot', 'username')
    list_filter = ('rating', 'created_at')
    search_fields = ('spot__name', 'username', 'content')
    list_per_page = 50
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('page_name', 'page_url', 'visit_count', 'first_visit', 'last_visit')
    list_display_links = ('page_name', 'page_url')
    list_filter = ('first_visit', 'last_visit')
    search_fields = ('page_name', 'page_url')
    list_per_page = 50
    ordering = ('-visit_count',)
    readonly_fields = ('first_visit', 'last_visit')

#注册对应的Admin类
admin.site.register(TravelInfo,TravelInfoAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(PageVisit, PageVisitAdmin)




# Register your models here.
