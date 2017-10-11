# Yelp Academic Dataset Mining for Affordances of a Yelp Category

## TF-IDF

### With English Stop Words provided by Sklearn

#### Method
```python
    vect = TfidfVectorizer(input='filename',
        vocabulary=None, stop_words=ENGLISH_STOP_WORDS)
```

#### Data
Sushi Bars
```
       feature     tfidf
0        sushi  0.480726
1         food  0.260143
2         good  0.259699
3        place  0.259370
4      service  0.185683
5        great  0.184497
6         roll  0.148693
7         like  0.147573
8         just  0.136568
9        rolls  0.129404
10        time  0.126187
11      really  0.115643
12  restaurant  0.107855
13       fresh  0.099419
14     ordered  0.094280
15       order  0.092713
16        menu  0.091362
17          ve  0.089995
18        fish  0.084146
19         eat  0.082718
20        best  0.082076
21        came  0.077533
22         don  0.075465
23         try  0.074581
24        rice  0.074175
```

Bikes
```
     feature     tfidf
0       bike  0.679804
1       shop  0.210371
2      bikes  0.201723
3      great  0.185649
4    service  0.176860
5       just  0.126899
6       time  0.125865
7      store  0.122763
8        new  0.119473
9       like  0.107488
10     place  0.106219
11      good  0.097430
12     staff  0.090569
13    really  0.084412
14  friendly  0.077926
15      went  0.076986
16        ve  0.075999
17  customer  0.073837
18   helpful  0.068338
19       got  0.068056
20       did  0.067586
21       don  0.066975
22      didn  0.066740
23      ride  0.065377
24      know  0.065048
```

Dance Clubs
```
    feature     tfidf
0      club  0.290103
1     place  0.248283
2     night  0.210500
3      like  0.201289
4      good  0.188407
5      time  0.185168
6      just  0.179019
7    people  0.170152
8     vegas  0.169320
9     great  0.162827
10    dance  0.157334
11    music  0.156910
12   drinks  0.147426
13      got  0.135872
14   really  0.129811
15      bar  0.121806
16  service  0.115593
17     line  0.113051
18    floor  0.112739
19      don  0.106310
20     went  0.099153
21    table  0.089222
22   pretty  0.087663
23     free  0.087463
24     nice  0.087087
```

#### Insights
Words like `don` and `didn` shows me that the parser is not doing well words that have apostrophes like `don't` and `didn't`.

Some words come up a lot in any sort of review, not so relevant to the place, i.e. shop, place, great, service, just, time, store, new, like, good, really. I'm almost tempted to put words or phrases like staff, really, friendly into this bucket of overused too.

[https://buhrmann.github.io/tfidf-analysis.html](tfidf)

This resource speaks of taking the average of all TFIDFS over the documents, to see which are the most important words across documents.  That might reveal the "reviewy" words that aren't relevant to affordances per category.

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
