from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type=collision_type
        self.params=params
        if collision_type!="Double":
            self.z,self.table_size=params[:2]
        #self.size=get_next_size(self.table_size) #handles general case for when table size is not fixed also 
        self.count=0 #no of elements in the hash table
        if collision_type=="Double":
            self.z1, self.z2,self.c2,self.table_size=params[0],params[1],params[2],params[3] 
        self.table=[None]*self.table_size
        self.load=0

        
        pass

    def latin_to_num(self, char):
        if 'a' <= char <= 'z':
            return ord(char) - ord('a')
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 26
        else:
            return ord(char)

    def _polynomial_accumulation_hash(self, key, z):
        h_value = 0
        for i, char in enumerate(key):

            h_value += self.latin_to_num(char) * (z ** i)
        #should i include this return stmt
        return h_value

    def _hash1(self, key):
        if self.collision_type=="Double":
            return self._polynomial_accumulation_hash(key, self.z1)%self.table_size
        else:
            return self._polynomial_accumulation_hash(key, self.z)%self.table_size
        

    def _hash2(self, key):
        # For double hashing, use a different z (self.z2) and table_size value (self.c2).
        h2_value = self.c2 - (self._polynomial_accumulation_hash(key, self.z2) % self.c2)
        return h2_value
    

    def _linear_probe(self, key, i):
        return (self._hash1(key) + i) % self.table_size

    def _double_hash(self, key, i):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        return (h1 + i * h2) % self.table_size



    
    def insert(self, x):
        if isinstance(x, tuple):
            key, value = x
        else:
            key, value = x, None  # For HashSet, value is not relevant and set as None
    
        index = self._hash1(key)
        i=0
        if self.collision_type == "Chain":
            if self.table[index] is None:
                self.table[index] = []
            for k, v in self.table[index]:
                if k == key:
                    return
            
            self.table[index].append((key, value))
            self.count+=1
        
        
        else:#for linear or double
            while self.table[index] is not None:
                if self.table[index][0] == key:
                    return  # Key exists, so skip insertion
                i+=1
                if i >= len(self.table):
                    raise Exception("Table is full")
            
                # Move to the next slot in case of collision
                if self.collision_type=="Linear":
                    index = self._linear_probe(key,i)
                else:
                    index=self._double_hash(key,i)  # Adjust as necessary for double hashing
            
            # Place the new (key, value) pair or key in the determined slot
    
            self.table[index] = (key, value)
            self.count += 1  # Increment the element count


            pass
    
    def find(self, key):
        index = self.get_slot(key)
        
        if self.collision_type == "Chain":
            if self.table[index] is None:
                return None
            for k, v in self.table[index]:
                if k == key:
                    return v
                #so this code works for hashmaps but not hashset
                # we have to return value in case of hashmap 
        #when collision type is linear or double 
        elif self.table[index] is not None and self.table[index][0] == key:
            return self.table[index][1]
        
        
        return None
    
    def get_slot(self, key):
        index = self._hash1(key)
        i = 0
        
        while True:
            if self.collision_type == "Chain":
                return index
            #in case of chaining, the index doesnt change
            elif self.collision_type == "Linear":
                index = self._linear_probe(key, i)

            elif self.collision_type == "Double":
                index = self._double_hash(key, i)
            #find index to be used to store the key
            
            if self.table[index] is None or self.table[index][0] == key:
                #check if that index is empty or if that index already stores the key
                return index
            
            i += 1
        pass
    
    def get_load(self):
        #self.load=self.count/self.table_size
        return self.count / self.table_size

    
    def __str__(self):
        result = []
        for slot in self.table:
            if slot is None:
                result.append("<EMPTY>")
            elif self.collision_type == "Chain":
                entries = " ; ".join(f"({k}, {v})" for k, v in slot)
                result.append(entries)
            else:
                key, value = slot
                result.append(f"({key}, {value})")
        return " | ".join(result)
    #this is to be used in hash maps
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        
            
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        self.distinct=0
        self.distinct_list=[]
        super().__init__(collision_type, params)
        pass
    
    def insert(self, key):
        super().insert((key, None))
        pass
    
    def find(self, key):
        index = self.get_slot(key)
        
        if self.collision_type == "Chain":
            if self.table[index] is None:
                return None
            for k, v in self.table[index]:
                if k == key:
                    return True
                #so this code works for hashmaps but not hashset
                # we have to return value in case of hashmap 
        #when collision type is linear or double 
        elif self.table[index] is not None and self.table[index][0] == key:
            return True
        
        
        return False

    
    def get_slot(self, key):
        return super().get_slot(key)

        pass
    
    def get_load(self):
        return super().get_load()
        pass
    
    def __str__(self):
        #print("IM RUNNING")
        result = []
        for slot in self.table:
            if slot is None:
                result.append("<EMPTY>")
            elif self.collision_type == "Chain":
                if slot:
                    entries = " ; ".join(f"{k}" for k, _ in slot)
                    result.append(entries)
                else:
                    result.append("<EMPTY>")
            else:
                if slot:
                    key, _ = slot
                    result.append(f"{key}")
                else:
                    result.append("<EMPTY>")
        return " | ".join(result)
    #created separately for hash sets
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        pass
    
    def insert(self, x):
        super().insert(x)
        # x = (key, value)
        pass
    
    def find(self, key):
        return super().find(key)
        pass
    
    def get_slot(self, key):
        return super().get_slot(key)
        pass
    
    def get_load(self):
        return super().get_load()

        pass
    
    def __str__(self):
        return super().__str__()
        
        pass



