# algo

sort by bit count in row

hungarian to maximize rightness or minimize leftness

fix rows order lexographically

### cost matrix
cost of every column is sum of distances to most right bit lexicographicly ordered by bit_count in row
but it is n^2 bits for every cost but it should be reductible for concrete array

probably reductible to k which is number of set bits.

#### calculating cost for column
Properties:
 1. additive to n elements- cost of columns must be additive for any order of columns
 then they need to be additive to ordered_bit_counts in columns
 all ten columns must add up exactly to ordered_bit_counts
 2. comparable - 


column_cost: column,index,ordered_bit_counts,n -> cost
cost is vector of bits of size nxm it handles additivness and comparability
ideally could be of size n

cost for identity is n=m
cost for full is nlogm
cost for all different is n*m, but it is only possible when m<=n

0001 1 2 bits
0011 2 3 bits
0111 3 2 bits
1111 4 0 bits
----
1234
expected 16 bits
perfectly 7 bits
4 różne kolumy i 4 różne wiersze
4(diff)*log2(4+1)


0001 1 2 bits
0011 2 3 bits
0111 3 2 bits
1110 3 2 bits
1111 4 0 bits
2334
4*log2(4+1)
expected 20 bits
ideally 9bits
two

3\*4+4\*log2 2+1

unique, counts =np.unique(ordered_bit_counts,return_counts=True)
bit_size = n*len(unique) * math.ceil(log2(counts+1))

hmm but

0001 1 2 bits
0001 1 2 bits
0001 1 2 bits 
0001 1 2 bits
----
0004
expected 12
ideally 8
unknown_perfect 3
4\*log2(4+1)=12

0001 1 2bit
0010 1 2bit
0100 1 2bit
1000 1 2bit
----
1111
expected 4?
ideally 8 bits
expect 4 bits
1\*4*log2(1+1) = 4

[[0,0,0,1],[0,0,1,1],[0,1,1,1],[1,1,1,0],[1,1,1,1]]

[[0,0,0,1],[0,0,0,1],[0,0,0,1],[0,0,0,1]]

[[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,0,0,0]]


highest complexity is for dense matrix. I want to find optimal position of columns and I want to calculate their cost depending on position for cost matrix.
As specified bit count and column index are bot important. Then all proposed solution aren't useful.
The only way that I currently see is to define own type that will contain two numbers
first number would be of bit_count_in_row size noted as k and second number would be number of C(row_size,k)
Then I could define all needed operation for it.
For every n numbers in row previously I needed n^2 bits
With this second option it is n*log2(n)+n*log2()
