from collections import Counter
from django.urls import reverse
from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html,urlencode
from store.models import Product,Customer,Address,Collection,Promotion,Order,OrderItem,CartItem

# Register your models here

admin.site.site_header = "Storefront Admin"
admin.site.index_title = 'Admin'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','product_count']
    search_fields = ['title']
    
    #
    @admin.display(ordering='product_count')
    def product_count(self,collection):
        
        url  = reverse('admin:store_product_changelist') + '?' + urlencode({'collection__id': str(collection.id)}) 
        return format_html(f'<a href="{url}">{collection.product_count}</a>')
    
    def  get_queryset(self,request):
        return super().get_queryset(request).annotate(product_count=Count('product'))



class InventoryFilter(admin.SimpleListFilter):
  
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self,request,model_admin):
        return [('<10','low')]
    def queryset(self,request,queryset):
       if self.value() == '<10':
           return queryset.filter(inventory__lt=10)
           

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug':['title'],}
    list_display =  ['title','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    
    def collection_title(self,product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    
    list_display = ['first_name','last_name','membership','orders']
    list_editable = ['membership']
    ordering = ['first_name','last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    @admin.display(ordering='orders')
    def orders(self, customer):
        url = reverse('admin:store_order_changelist')
        params = urlencode({'customer_id': str(customer.id)})
        return format_html(f'<a href="{url}?{params}">view Orders</a>')
    
    orders.short_description = 'Orders'
    def get_queryset(self,request):
        return super().get_queryset(request).annotate(orders=Count('customer.order'))
    
        
    
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    autocomplete_fields = ['customer']
    
   


admin.site.register(Address)

admin.site.register(Promotion)
admin.site.register(OrderItem)
admin.site.register(CartItem)

