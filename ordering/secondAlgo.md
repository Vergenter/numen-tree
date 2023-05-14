### find minimal binary value for tree
#### Minimize binary number created by flattening 2d array of bits where rows and columns can be freely swapped
splits starts empty it defines col indices that separates array into parts
optimization_variants = [Tuple[rows_indices,columns_indices]]
for row_idx in rows:
1. for Tuple[rows_indices,columns_indices] in optimization_variants:
Find rows that have lexographically highest count of zeros in parts defined by splits. If there are not splits defined, then whole row.
If there is row/are rows that are exactly same as previous then choose any of them
For each row create modified copy of rows indices with added itself
This step create from many optimization_variants sometimes more optimization_variants

2. Filter new optimization_variants by lexographically highest count of zeros

3. for every row copy columns_indices then 
sort it by values in row in parts for each part separately

4. add splits in existing parts using count of zeros in parts. Splits will be the same for all rows from previous step in the opposite one row would be better than other, thus it is impossible.
note that if whole part is zeros then no split is added

end for row_idx




#### 2

f: splits, list[Tuple[rows_indices,columns_indices]] -> Tuple[rows_indices,columns_indices]
for row_idx in range(rows):
 
Theory no. 1 all best rows are exaclty the same False!
0001    0001
1000 => 0010
1110    1110
vs
1000    0001
0001 => 0010
1110    1101











