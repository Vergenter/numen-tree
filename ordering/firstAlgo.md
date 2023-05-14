find offsets for second state
put columns in place so there is most matches all not mathed are moving candidates
item can have more matches in right column that left opposite cannot be true
The fill from right to left, probably there is chance that this method is incorrect

To well up it more 

Can node be better target for smaller row?



then can simplify this problem to this
I have 10 ranks
And 10 values with 10 scores each for it's rank
find max value.

This is solved


Now we to add higher/lower cost to lefter ones in a way that doesn't influence number of incorrect ones and 
by lexographically smallest I mean
from top to bottom offseted bits must be from smallest indices
If row doesn't matter
but relative height between different tiers matters
by this I mean that offsets for shorter sets matter more than longer
Importance order    
bit_difference_importance, bit_row_size, bit_to_offset

not exactly this
this is probably one param bit_row_size, bit_to_offset

there is not that many bit_row_size, bit_to_offset
we can encode them all, but what it gives us?
They are not additive.
Having offset from first rows and column should be most important or two or even more
then it means that cost of offset from zero node tier 1 should be from n+1 parts

n^(2n) space bound for number, it can be optimized but that is bad haha
Ideally you have maximally n^2(all values incorrect ones) offsets and this group need to be encompased

dimension looks as such count_unique(set_bit_row_size), count_unique_for_row_size(bit_column)(n), count(max_incorrect_bits)(n^2)(precisely only must sum to it)
but I have only n bits in column to calculate const soo probably not n at the end
in depth analysis of this space
1 can be offseted on n-1 ways
2 can be offseted on n-2 and n-3
X(n-k,k)
2d array nxn
group by bit_row_size, bit_to_offset -> grouping gs
g^n encodes all ineffeciently it is probably too big for simple space
but it is just g of n that is ordered for equality

So it can be maximally n^2



fix rows



I want to define additive cost for every offset in lexicographicall order
So I want sort rows 
I want to order whole arrays that have some properties in a way to find unique

I have 2d array for which i want to calculate cost of every incorrectly placed bit(currently it can be all set bits) in a way defined by set_bits_in_row, column_of_bit
in way that will define total_order on all 2d array of this size
I want to get total_order all 2d arrays 

lexicographicall smallest order


I've 2d array of bits in which I order columns to minimize incorrectly set bits, I can solve this problem with hungarian method.
By correctly set bits I mean bits that are in the same place for 2d array with rows sorted by number of set bits and columns sorted by value.(all 1 at right side)
I want to always get the same result for example there is two correct results, but I want to get only one:
```py
arr = [[1,1,1],[1,0,1],[0,1,0]]
perfect = [[0,0,1],[0,1,1],[1,1,1]]
nearest_1 = [[0,0,1],[1,1,0],[1,1,1]] # difference from perfect is 2 bits
nearest_2 = [[1,0,0],[0,1,1],[1,1,1]] # difference from perfect is 2 bits
```
How can I do that?

Note that order of rows can always be swapped, but rows always must be ordered by set_bits_count

I see one way of chossing always same result:

n is width of array

I enumerate all bits by (set_bits_in_row, bit_index_in_row) as g
for sure g is smaller or equal to n^2

there can be maximally x set bits, which can be stored in log2(x) space
for sure x is smaller or equal to n^2

then single value that will store all such combination for 2d array will have size log2(x)\*g which is bounded by log2(n^2)\*n^2, I will refer to it as offset_value

I can use the offset_value as lower bits in every cell in cost matrix, top is bit difference


cost_field_size is log2(n^2)*n^2+log2(n^2) which is n^2 for cost matrix

then whole cost matrix size is n^4*log(n^2)

By using this hungarian method will almost return unique 2d array.

This can be refined by applying hungarian method on every same_number_set_bits rows to minimize offset_value

Now resulting array should be unique, by this I mean lexographically smallest.

Is it viable?
Could it be done better?


Final question
Does there exist two non isomorphic graphs with different correct bits, but same number of them with same incorrect bits? yes, and two isomorphic exists too
moving are optimal so it doesn't incluence correct form
then only constrained is order?
number of 0 in rows is constrained then number of 1 is constrained too
10101 is same to 11100 hmm they order is undefined and I believe they can be non isomorphic
hah it is not that simple, if they are always isomorphic then it is ok too
they are different:
xx11
1101
x111

xx11
1011
x111

they are same
xx11
1101
x111

xx11
1110
x111

hmm but I can reorder them and find min form too? Hmm but it does touch incorrect bits
just min for correct part is more important :D


There would be guarante if moving has target encoded, but can it be done in cost matrix?
By this I mean cost of moving to lower index should be smaller, but then cost is depended on previous columns, because being second one is more costly


Just defining cost for not being on the right and not about correctness?
Looks like it solves this.
Just less right it is the worse it is


### Then algorithm

get 2d array A of dimensions nxn
Sort rows by set bits count

calculate cost matrix for every bit
bits in columns with less bits cost more
more to left bit cost more 
to do this I calculate g = n*unique_bits_rows
all of them can have value n but cannot more so its log2(n) number for count
then cost of node is g*log2(n) where first bits are 0,0 and least are (n,n)
I can optimize it using rank of a specific combination of g non-negative integers that sum to k
I would need to add bits to padd for possible additions

This could not work because of this value are not additive

But combination of g non-negative integers that sum to k has where k is all set bits in graph
I was naivly thinking that all g can be log2k but it is not true it can be optimized
It will result in problem g non-negative integers with limits l1,l2,...,lg that sum maximally to k
simple limits I can define as g with counts.
It reduces g=n^2 to n^2 bits where only k bits can be set
and g=n to n^2 where only k bits can be set

it can be optimized further
every limit can be log2 as count them, it optimizes best scenario g=n to nlog2n and still supports k optimization
but pessimistic is still same g=n^2 when all limits are 1 but there is still k optimization
k optimization sum maximally to k

or there is even better optimization bits in row can only be in this number of places
by this I mean for all rows with bit set size x, there is only h bits that can be distributed in them, and there are even additional constraint
I'm distributing columns then not ones but whole values.
In this idea I distribute columns for whole matrix which is much smaller space than only columns for same set bits sizes
My space is n columns at n positions I can order them from smallest to biggest with my bit constraint. Hungarian algorithm is not needed hmm
all of them are just simple vector that I can sort lexicographically using vectors_with_set_bit_count. This removes whole memory constraint



I can split it in even smaller parts

then for column I need to calculate cost 
row_set_bit_counts -> g
cost_of_column(col,idx,row_set_bit_counts) -> biginteger
first part should be bit difference second part is left_topness

calculate cost matrix as difference of bits to array that has rows sorted by bit count and columns by value
merge costs

optimize using hungarian method

apply hungarian method on rows with same number of set bits. -> it can be just lexsort
there is guarantee because to normal offset cost there is additional cost of height

canonic form

#### offset cost is


### algo v2

get 2d array A of dimensions nxn
Sort rows by set bits count

sort columns lexicographically treating sum of indices values for same_bit_set_rows as one number
previous step gave simple enumeration from 1 to n for every column
append it to bit difference for swaps as latter part (I don't even know if I do need first part and thus hungarian method)
hungarian method

lexsort rows by binary_repr_of_row, set_bits_rows

canonic form


### reduced algorithm

get 2d array A of dimensions nxm
Sort rows by set bits count
sort columns lexicographically treating sum of indices values for same_bit_set_rows as one number
lexsort rows by binary_repr_of_row, set_bits_rows
canonic form

It doesn't work because:
[[0 0 0 1]
 [0 1 0 1]
 [1 0 1 0]
 [1 1 1 0]]
[[0 0 0 1]
 [0 0 1 1]
 [1 1 0 0]
 [1 1 1 0]]

Simple solution sort lexographicaly columns
Is it possible that lexographicall sort of column would be destoryed by rows sort? yes
More important can because of it two graph have different form? yes
Then I'm looking for two graphs after first step being different by swap and giving different result.


equal columns
 [0 0 0 1]
 [0 1 0 1]
 [1 0 1 0]
 [0 1 0 1]
 [1 0 1 0]
changes to this
 [0 0 0 1]
 [0 0 1 1]
 [0 0 1 1]
 [1 1 0 0]
 [1 1 0 0]
 
 [0 0 0 1]
 [1 0 1 0]
 [1 0 1 0]
 [0 1 0 1]
 [0 1 0 1]
changes to this
 [0 0 0 1]
 [0 1 1 0]
 [0 1 1 0]
 [1 0 0 1]
 [1 0 0 1]
#### why I think it works

Sort rows by set bits count -> stabilizes next sorting
order columns uniquely
order rows uniquely
canonic form

