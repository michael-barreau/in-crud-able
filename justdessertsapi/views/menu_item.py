"""View module for handling requests about Menu Items"""

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from justdessertsapi.models import MenuItem

class MenuItemView(ViewSet):
    """Menu Items Viewset"""

    def retrieve(self, request, pk):
        """Handle GET request for single menu item"""
        try:    
            menu_item = MenuItem.objects.get(pk=pk)
            serializer = MenuItemSerializer(menu_item)
            return Response(serializer.data)
        except MenuItem.DoesNotExist as e:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        """Handle GET request to get all menu items"""
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """ Handle a POST request for a menu item """
        
        new_menu_item = MenuItem.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            price=request.data["price"],
            type=request.data["type"],
            serving_size=request.data.get("serving_size")
        )
        serializer = MenuItemSerializer(new_menu_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def update(self, request, pk):
        """ Handles a PUT request for a menu item """
        editing_menu_item = MenuItem.objects.get(pk=pk)
        
        editing_menu_item.title = request.data["title"]
        editing_menu_item.description = request.data["description"]
        editing_menu_item.price = request.data["price"]
        editing_menu_item.type = request.data["type"]
        editing_menu_item.serving_size = request.data.get("serving_size")
        
        editing_menu_item.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """ Handles a DELETE request for a menu item """
        try:
            menu_item = MenuItem.objects.get(pk=pk)
            menu_item.delete()
        except MenuItem.DoesNotExist as ex:
            return Response({}, status=status.HTTP_404_NOT_FOUND) 
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class MenuItemSerializer(serializers.ModelSerializer):
    """ JSON serializer for menu items """
    class Meta:
        model = MenuItem
        fields = ('id', 'title', 'description', 'price', 'type','serving_size')