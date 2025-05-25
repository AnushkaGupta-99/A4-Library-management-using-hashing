from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        # Update the table size and create a new table
        new_size = get_next_size()
        old_table = self.table  # Store the old table for rehashing
        self.table_size = new_size
        self.table = [None] * self.table_size if self.collision_type != "Chain" else [[] for _ in range(self.table_size)]
        #old_count = self.count  # Track original count to ensure correct reinsertions
        self.count=0
        # Reinsert each item into the new table
        for item in old_table:
            if item:
                if self.collision_type == "Chain":
                    for key, _ in item:
                        self.insert(key)
                else:
                    self.insert(item[0])

    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)

        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        

    def rehash(self):
        # Update the table size and create a new table
        new_size = get_next_size()
        old_table = self.table  # Store the old table for rehashing
        self.table_size = new_size
        self.table = [None] * self.table_size if self.collision_type != "Chain" else [[] for _ in range(self.table_size)]
        old_count = self.count  

        # Reinsert each item into the new table
        for item in old_table:
            if item:
                if self.collision_type == "Chain":
                    for j in item:
                        self.insert(j)
                else:
                    self.insert(item)

    
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        if self.get_load() >= 0.5:
            self.rehash()