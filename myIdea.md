shareness metric

should measure how much elements are shared
more means more sparse
non connected is max
every thing shared is min
```
[
 1111
 0111
 0011
 0001
] 
```
is thus 0 because everything shared
it is 1234
```
[
 1111
 0111
 0011
 0010
]
``` 
is 0 too
it is 1243
then find max order
then find min order
abolute min order is all ones, but now we have some information
but sum is const then min for this shape is 2233
then best is descending max
worst is all min
looking at this differently 4321 is max 3322 is min digits sorted from bigest to smalest
or 1234 is min
and 2233 is max

```
[
 1111
 0111
 0011
 0100
]
``` 
s >0
at first it is
1333
```
[
 1111
 0111
 0011
 1000
]
``` 
is >0
2233
For my usecase this two should be different:
```
[
 1111
 0111
 0011
 0100
]
``` 
is >0
1333 and one misplacement

```
[
 1111
 0111
 0011
 1000
]
``` 
is >0
2233 and one misplacement
And thid two same
```
[
 1111
 0111
 0011
 0001
]
``` 
1234 and 0 misplacement
is thus 0 because everything shared

```
[
 1111
 0111
 0011
 0010
]
``` 
is 0 too
1234 and 0 misplacement
This three should be different:|
```
[
 1111
 0111
 0011
 0001
] 
```
this is known 0 
```
[
 1111
 0111
 0011
 0100
] 
```
1333 and 1 misplacement
I would say offset by 1
```
[
 1111
 0111
 0011
 1000
] 
```
2233 and 1 misplacement
I would say offset by 2
but then this:
```
[
 1111
 0111
 1001
 0001
] 
```
It is 2224
I would say that is better ordered than 2233
then it would be offseted less
## There is problem
This should be different
```
[
 1111
 0111
 0011
 1000
] 
```
2233
there is one misplacement
```
[
 1111
 0111
 1001
 1000
] 
```
2233
there is two misplacement

# first method proposition
get in column counts
get in rows count
find biggest displacement 
find minimal displacement 
find current displacement 
in columns count are near to be good
We have this two
```
[
 1111
 0111
 0011
 1000
] 
```
1000 is displaced by 2
```
[
 1111
 0111
 1001
 1000
] 
```
1001 is displaced by 1
1000 is displaced by 1 and all other displacemnt are equal?
[
 1111
 0111
 1001
 0100
] 
same displacement as top but should be different

displacement shoud have value depending with who you are displaced.
because in situation one 
1000 is displaced to 0111
in two 
0100 is displaced to 1001
being displaced to denser element should be more importnat nad how does work dipslacement to diplaced element and when this shouldn't matter

```
[
 1111
 0111
 1001
 1000
] 
```
is this 
```
[
 1111
 1101
 0011
 0010
] 
```
2233
1101 is misplaced by one

this operator must be comutative it guarantess that isomorphism give same result
this operator must return different result for every non isomorphic graph then it should return different result for every argument
then this function must be injective
And at best it needs to be injective to minimal set
Then it should be injective into non-isomophic graph enumeration
non-isomorphic graph enumeration is bijective and so I need inverse function


### Intuitive enumeration
biggest sets from top to botton
bigger number from left to right
both criteria make draws. Same size sets and same times of numbers
draw are acceptable only if they for nodes that are same
```
4 1111    1111    1111    1111    1111    1111
3 0111    0111    0111    0111    0111    0111
2 0011    0011    0011    1001    1001    1001
1 0001    0100    1000    0001    0010    1000
----------------------------------------------
  1234    1333    2233    2224    2233    3223
                                          2233
----------------------------------------------
                                          1111
                                          1101
                                          0011
                                          0010
----------------------------------------------
                                          2233                                        
```
1. is perfect
2. is 4:3:2(p) or 4:2:1 or 3:4:2 or 3:3:2
```
1111
0111
0011
0100
```
3. is 4:1:4(P)
4. is 3:1:3(P)
5. is 3:1:3&4:3:4(P) or 3:1:3 -> probably format is wrong, because it is too hard
```
1111
0111
1010
0001
```

6. is 3:1:3&4:1:4(P) or 2:3:1 or 2:2:1
```
1111
1110
0011
0001
```
For all this matrices there is only one way to fix it to perfect form
But I don't know if it is usefull.
Hypothesis to test:
x. this perfect matrices are always sorted by column sum, is there more to it?
a. can I find forms with smallest numbers of fixes in P?

b. is there always only one way to fix it?
```
001111
110011
```
There are two but probably only one :)
2:1:3&2:2:4 or 2:1:4&2:2:3 but we can order them by indices as smallest to smallest 
I believe that this fixes are always orderless and unique :)
always 0 and 1 are swapped, if minimall number of swaps is made they are commutative
bb. Wrong question. Is there always one form to fix? or are there multiple form with minimal number of fixes? There are multiple forms
```
0011
1000
```
vs
```
0011
0100
```
both same path to fix, but fix for first is smaller 2:1:4 vs 2:2:4
```
0011
0100
1000
``` 
vs
```
0011
1000
0100
``` 
bbb. Can I use at least fact that this can order? yes
yes because swappings are triplets of int and they can be sorted, then there exist exactly one form by this sorting
Best form is with smallest ammount of smallest triplets
c. Can I found smallest triplets in P, or there is NP of them :/
ddd. are fix operation enough for no isomorphism? For this example probably true
I can hope that best notation will make always shortest sequence of swaps
Perfect notation will make only 1 shortest path possible, but is it possible?
There could be multiple forms that enable perfect notation, then ideal notation would always have only one form or rules of operation enable only one form with only shortest path
Ideal notation is notation that for all graphs have only operation that moves it to perfect form. 
Is lexical ordering like this? Nope

I can probably say that form that has minimal number of steps to perfect notation is best? But can I efficiently find it?
Advantage of this perfect form is that it is total ordered
#### Probably useless rattle
probably solution is operator that never can be expressed by swaps it would create always non isomorphic graph
but ideally this operator would never fall into cycle or it's cycle would be all graphs
But what properties would it need to have to be 
but all this operation on one graph would create all non isomorphic graphs.
but it would be surjective
result of it would need to be andable and it is for operator O if I can Oa and Ob then the result is not isomorphic to a and b 
 1000
 0000
 0000
 0010

That is complicated idea

Best idea would be intuitive enumeration, because current complexity comes from finding minimal lexicographic representation.


### new idea
1. find most ordered form
2. note displacement in form of index_swap



Even if matrix ordering is in P
There still could be mutltiple nearest forms if not isomorphism is checked correctly then it is enough
The problem is inverted. 
### Does there exist multiple offsets that makes same graph? yes
```
0011    0011    0011
0001    0100    1000
```
Can we match them all? (Can we efficiently reduce them to itself?)
### Is it possible that offset between different set sizes creates same graph? yes
Yes because offset can create same graph to original 
"""
1111    1111    1111 
0111    0111    1011
0011    0101    0011
0001    0001    0001
"""
### Does this operator need to create non isomorhic graph? NO NEED TO KNOW
### Can I say that two graphs are isomorphic?
If I have form with shortest offsets to fix even with it no
Two non isomorphic graphs can have same numbers fix to be done.
There can be multiple forms of isomorhic graph.
Then I would need to know which swap operators create isomorphic graphs and which no.
Offset operator can create same graph as original and multiple isomorphic graphs.
can 3->2 create non isomorphic graph?
can 3->non2 create isomorphic graph?
If both are false then operator can be defined in non auto morphing way.
If both have same minimal numbers of operator applying they can be isomorphic
if graphs are isomorphic they need to be mappable, and theirs swaps need to be mappable
But only their count is easly distinctive
I have nothing, even with this.
If I don't have any special properties of this swap then it is useless.
There is only one perfect form of graph.
To check isomorphism I would need to check if chain of swaps is equal to other
This is easly solvable if they both graphs have same form
### Does two sorted isomorphic graph can look differently?
### Can I effeciently find form of graph that has smallest offset? 
It uses that offset is sortable.
It is guaranteed that there is only one form with smallest shortest path.
This will guarantee that all isomorphic graph would look the same.
It would need operation in P that will go through isomorphic graphs and find one with smallest offsets and it cannot go through all.
So there need to exist method that will find smallest move to fix 

Then one problem to go
## find form with smallest shortest offsets in P
1. find how to find offsets for graph
2. find how to find minimal number of offsets for graph
3. find how to minimize offset cost



