from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from ..enums.item_type_enum import ItemTypeEnum

from ..entities.item import Item


class IItemRepository(ABC):
    
    
    @abstractmethod
    def get_all_items(self) -> List[Item]:
        '''
        Returns all the itens in the database 
        '''
        pass
    
    @abstractmethod
    def get_item(self, item_id: int) -> Optional[Item]:
        '''
        Returns the item with the given id.
        If the item does not exist, returns None
        '''
        pass
    
    @abstractmethod
    def create_item(self, item: Item, item_id: int) -> Item:
        '''
        Creates a new item in the database
        '''
        pass
    
    @abstractmethod
    def delete_item(self, item_id: int) -> Item:
        '''
        Deletes the item with the given id.
        If the item does not exist, returns None
        '''
        
    @abstractmethod
    def update_item(self, item_id:int, name:str=None, price:float=None, item_type:ItemTypeEnum=None, admin_permission:bool=None) -> Item:
        '''
        Updates the item with the given id.
        If the item does not exist, returns None
        '''
        pass
    
    