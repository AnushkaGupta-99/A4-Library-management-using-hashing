import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    #the words should be in lexicographically sorted order and sorted using merge sort
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        #O(kW log W+klogk) k books each with words<W ;book_titles and texts are lists
        self.book_titles=book_titles
        self.texts=texts
        self.updated_texts=[]
        self.sorted_book_titles=self.merge_sort(self.book_titles)
        self.booktitle_text_tuple = [(self.book_titles[i], self.texts[i]) for i in range(len(self.book_titles))]
        # Sort the paired books based on the book titles using merge sort
        self.sorted_booktitle_text_tuple = self.merge_sort(self.booktitle_text_tuple)
        #this is sorted acc to title
        self.updated_texts = [self.merge_sort(pair[1]) for pair in self.sorted_booktitle_text_tuple]

        #ALL ARE MAPPED USING i, distinct_words_in_books, updated_texts and sorted_book_titles
        self.distinct_words_in_books=[[] for _ in range(len(self.updated_texts))]
        for i in range(len(self.updated_texts)):
            text=self.updated_texts[i]
            for j in range(len(text)):
                if j==0:
                    self.distinct_words_in_books[i].append(text[0])
                else:
                    if text[j]==text[j-1]:
                        pass
                    else:
                        self.distinct_words_in_books[i].append(text[j])
            self.distinct_words_in_books[i]=self.merge_sort(self.distinct_words_in_books[i])


    def merge_tuples(self,left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i][0] < right[j][0]:
                if not result or result[-1] != left[i]: 
                    result.append(left[i])
                i += 1
            elif left[i][0] > right[j][0]:
                if not result or result[-1] != right[j]:  
                    result.append(right[j])
                j += 1
            elif left[i][0] == right[j][0]:
                if not result or result[-1] != left[i]:  
                    result.append(left[i])
                i += 1
                j += 1

        # Add remaining elements from left
        while i < len(left):
            if not result or result[-1] != left[i]:  
                result.append(left[i])
            i += 1

    
        while j < len(right):
            if not result or result[-1] != right[j]: 
                result.append(right[j])
            j += 1

        return result

            
                
    def merge_sort(self,arr):
        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left_half = self.merge_sort(arr[:mid])
        right_half = self.merge_sort(arr[mid:])
        if isinstance(arr[0], tuple):
            return self.merge_tuples(left_half, right_half)
        else:
            return self.merge(left_half, right_half)
        #return self.merge(left_half, right_half)

    def merge(self,left, right):
        sorted_arr = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                sorted_arr.append(left[i])
                i += 1
            else:
                sorted_arr.append(right[j])
                j += 1


        sorted_arr.extend(left[i:])
        sorted_arr.extend(right[j:])

        return sorted_arr

    def binary_search(self,arr, key):
        left, right = 0, len(arr) - 1

        while left <= right:
            mid = (left + right) // 2

            # Check if key is present at mid
            if arr[mid] == key:
                return mid

            # If key is greater, ignore the left half
            elif arr[mid] < key:
                left = mid + 1

            # If key is smaller, ignore the right half
            else:
                right = mid - 1

        # Key not found
        return -1

    
    
    def distinct_words(self, book_title):
        #O(D + log k) k-no of books D- no of distinct words
        index=self.binary_search(self.sorted_book_titles,book_title)
        distinct_words=self.distinct_words_in_books[index]
        return distinct_words 
        pass
    
    def count_distinct_words(self, book_title):
        #O(log k)
        index=self.binary_search(self.sorted_book_titles,book_title)
        return len(self.distinct_words_in_books[index])
        #returns the number of distinct words
        pass
    
    def search_keyword(self, keyword):
        #O(k log D)
        titles=[]
        for i in range(len(self.updated_texts)):
            if self.binary_search(self.distinct_words_in_books[i],keyword)!=-1:
                titles.append(self.sorted_book_titles[i])
        return titles

        #returns a list of all book titles which contain given keyword
        pass
    
    def print_books(self):
        #O(kD)
        #Print the book titles along with the distict words in a format similar to the HashTable prints.
        for i in range(len(self.texts)):
            print(self.sorted_book_titles[i],end=": ")
            for j in range(len(self.distinct_words_in_books[i])):
                print(self.distinct_words_in_books[i][j],end="")
                if j < len(self.distinct_words_in_books[i]) - 1:
                    print(" | ", end="")

            print()

                
        pass

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        #__init__ should run in time O(table size)
        self.name=name
        self.params=params
        if self.name=="Bezos":
            self.z1,self.z2,self.c2,self.initial_table_size=self.params[0],self.params[1],self.params[2],self.params[3]
        else:
            self.z,self.initial_table_size=self.params[0],self.params[1]
        if self.name=="Bezos":
            self.col_type="Double"
        elif self.name=="Jobs":
            self.col_type="Chain"
        else:
            self.col_type="Linear"

        self.library=ht.HashMap(self.col_type,self.params)
        self.book_list=[]
        

    


        pass
    
    def add_book(self, book_title, text):
        #add_book should run in time O(W+table size), where W is the number of words in the given book.
        book_hash=ht.HashSet(self.col_type,self.params)
        #but what about space constraints
        for i in text:
            if not book_hash.find(i):
                book_hash.distinct_list.append(i)
                book_hash.insert(i)
            #O(W)
        self.library.insert((book_title,book_hash))
        self.book_list=[]
        if self.col_type!="Chain":
            for i in self.library.table:
                if i!=None:
                    self.book_list.append(i[0])
        else:
            for i in self.library.table:
                if i!=None:
                    for j in i:
                        self.book_list.append(j[0])
        
        #O(1)
        pass
    
    def distinct_words(self, book_title):
        #distinct_words should run in time O(table size), where D is the number of distinct words in the book with the given title.
        x=self.library.find(book_title)
        x.distinct=0
        #x is the book hash table hashset
        #these will work for linear and double but not for chaining
        if self.col_type=="Chain":
            list=[]
            for i in x.table:
                if i is not None:
                    if len(i)>1:
                        for j in i:
                            list.append(j[0])
                            x.distinct+=1
                            
                    else:
                        list.append(i[0][0])
                        x.distinct+=1
            return list

            
        else:
            list=[]
            for i in x.table:
                if i is not None:
                    list.append(i[0])
                    x.distinct+=1       
            return list
        
        pass
    
    def count_distinct_words(self, book_title):
        #count_distinct_words should run in time O(1)
        x=self.library.find(book_title)
        return len(x.distinct_list)

        pass
    
    def search_keyword(self, keyword):
        #search_keyword should run in time O(k) according to the same notation, k is the number of books'
        l=[]
        for i in self.book_list:
            #so i is a book_title
            book=self.library.find(i)
            

            # book will be hash
            if book.find(keyword):
                #if True
                l.append(i) 
        return l
    
    def print_books(self):
        #print_books should run in time O(k table size)
        for i in range(len(self.book_list)):
            bookhash = self.library.find(self.book_list[i])
            print(self.book_list[i], end=": ")
            
            if bookhash.table is not None:
                if self.col_type == "Chain":
                    for j in range(len(bookhash.table)):
                        # Start printing each slot
                        if bookhash.table[j] is not None:
                            # Print words in the current slot, separated by `;`
                            for k in range(len(bookhash.table[j])):
                                print(bookhash.table[j][k][0], end="")
                        # Add `; ` between words within the same slot, but not after the last word
                                if k != len(bookhash.table[j]) - 1:
                                    print(" ; ", end="")
                        else:
                            print("<EMPTY>", end="")

                        # Decide whether to add `|` at the end of the slot
                        if j != len(bookhash.table) - 1:
                            print(" | ", end="")
                else:
                    for j in range(len(bookhash.table)):
                        if bookhash.table[j] is not None:# Print the word in the slot
                            print(bookhash.table[j][0], end="")
                        else:   # Print <EMPTY> for empty slots
                            print("<EMPTY>", end="")
            
# Add " | " separator after each slot, but not after the last one
                        if j != len(bookhash.table) - 1:
                            print(" | ", end="")

                            
            print()  # Newline after each book


        




















        '''for i in self.book_list:
            bookhash=self.library.find(i)
            print(i,end=": ")
            if bookhash.table!=None: #if the table is empty
                for j in range(len(bookhash.table)):
                    if j!=len(bookhash.table)-1:
                        if bookhash.table[j]!=None:
                            #J IS THE JTH SLOT IN BOOK HASHTABLE WHICH WILL CONTAIN WORDS CHAINED
                            #[J][K] IS THE KTH WORD, BUT I HAVE TO CHECK IF WORD IS WORD OR IF IT IS TUPLE
                            for k in range(len(bookhash.table[j])):
                                if k!=len(bookhash.table[j])-1:
                                    if bookhash.table[j][k]!=None:
                                        print(bookhash.table[j][k],end=";")
                                    else:
                                        print(bookhash.table[j][k],end=" | ")
                        else:
                            print("<EMPTY>",end=" | ")
                    else:
                        if bookhash.table[j]!=None:
                            for k in range(len(bookhash.table[j])):
                                if k!=len(bookhash.table[j])-1:
                                    if bookhash.table[j][k][0]!=None:
                                        print(bookhash.table[j][k][0],end=";")
                                    else:
                                        print(bookhash.table[j][k][0],end="")
                        else:
                            print("<EMPTY>",end="")
            print()'''


