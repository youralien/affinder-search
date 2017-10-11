# Yelp Academic Dataset Mining for Affordances of a Yelp Category

## TF-IDF 

### Without Stop Words

Code 
```python
    vect = TfidfVectorizer(input='filename', vocabulary=None, stop_words=None)
```

Sushi Bars
```
   feature     tfidf
0      the  0.607655
1      and  0.394959
2       to  0.244725
3      was  0.226179
4       it  0.186721
5       of  0.177050
6       is  0.159853
7      for  0.142715
8    sushi  0.130791
9       we  0.123039
10      in  0.120412
11    that  0.100120
12     but  0.100053
13     you  0.098694
14    this  0.096096
15      my  0.090169
16    with  0.089938
17    they  0.084096
18     not  0.076624
19      on  0.076280
20    food  0.070777
21    good  0.070656
22   place  0.070567
23     had  0.068111
24    have  0.067912
```

Bikes
```
   feature     tfidf
0      the  0.500588
1      and  0.430958
2       to  0.353340
3     bike  0.201304
4      for  0.170657
5       in  0.166733
6       my  0.166371
7       of  0.164464
8      was  0.154151
9       it  0.153372
10    they  0.146218
11    that  0.118494
12     you  0.110492
13      is  0.107305
14      me  0.103561
15      on  0.100889
16    with  0.089810
17    have  0.086373
18    this  0.086011
19      he  0.068154
20     but  0.066707
21    shop  0.062295
22      at  0.061989
23     are  0.060736
24   bikes  0.059734
```

Dance Clubs
```
   feature     tfidf
0      the  0.593143
1      and  0.363814
2       to  0.334453
3      was  0.198797
4       of  0.183976
5       it  0.173029
6       in  0.171071
7       is  0.136333
8      for  0.133892
9      you  0.132402
10      we  0.128391
11    that  0.114455
12      on  0.096098
13     but  0.094006
14    this  0.089930
15    with  0.084367
16      my  0.082671
17    they  0.076427
18    were  0.072722
19   there  0.072641
20      at  0.071858
21      so  0.069425
22     not  0.069105
23    have  0.066813
24    club  0.065544
```
