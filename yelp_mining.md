# Yelp Academic Dataset Mining for Affordances of a Yelp Category

## Affordance Language Demo

### natural language to keywords: sklearn stopwords; yelp categories from sklearn tfidf with stopwords joined for each word

```
Loading...
Type a natural language affordance requirement:

{'affordance.   ': 'Someone in a downtown riding their bike\n',
 'keywords      ': ['downtown', 'riding', 'bike']}
{'yelp category ': [u'Public Transportation',
                    u'Bar Crawl',
                    u'Historical Tours',
                    u'Public Services & Government',
                    u'Scooter Rentals',
                    u'Bike Sharing',
                    u'Transportation',
                    u'Bus Tours',
                    u'Tours',
                    u'Beaches',
                    u'Party Bike Rentals',
                    u'Parks',
                    u'Trains']}
Type another affordance query:

{'affordance.   ': 'Someone with a box and tape\n',
 'keywords      ': ['box', 'tape']}
{'yelp category ': [u'Notaries',
                    u'Shipping Centers',
                    u'Mailbox Centers',
                    u'Post Offices',
                    u'Shredding Services',
                    u'Printing Services',
                    u'Signmaking',
                    u'Couriers & Delivery Services',
                    u'Hardware Stores',
                    u'Gift Shops',
                    u'Propane',
                    u'Mass Media',
                    u'Public Services & Government',
                    u'Car Stereo Installation',
                    u'Appliances',
                    u'Office Equipment',
                    u'Movers',
                    u'Nurseries & Gardening',
                    u'Self Storage',
                    u'Videos & Video Game Rental',
                    u'Building Supplies',
                    u'Professional Services',
                    u'Local Services',
                    u'Packing Supplies',
                    u'Truck Rental',
                    u'Packing Services',
                    u'Auction Houses',
                    u'Trophy Shops',
                    u'Digitizing Services',
                    u'Music & Video',
                    u'Mags',
                    u'Books',
                    u'Music & DVDs',
                    u'Discount Store',
                    u'Estate Liquidation']}
```

####

## TF-IDF - Most relevant categories for a word 

### With TFIDF features coming from sklearn with stopwords, on all documents

#### Method
```python
def query_categories_by_word(word, X, categories, vocabulary, top_n=25):
    if isinstance(vocabulary, list):
        col_id = vocabulary.index(word)
    elif isinstance(vocabulary, np.ndarray):
        (col_id,), = np.where(vocabulary == word)

    return top_docs_for_word(X, categories, col_id, top_n)

def top_docs_for_word(X, document_names, col_id, top_n=25):
    """ Top docs by tfidf value for specific word (matrix col)
    """
    col = np.squeeze(X[:, col_id].toarray())
    return top_tfidf_feats(col, document_names, top_n)

def top_tfidf_feats(array, features, top_n=25):
    """ Get top n tfidf values in array and return them with their corresponding
    feature names.
    Source: https://buhrmann.github.io/tfidf-analysis.html
    """
    topn_ids = np.argsort(array)[::-1][:top_n]
    top_feats = [(features[i], array[i]) for i in topn_ids]
    df = pd.DataFrame(top_feats)
    df.columns = ['feature', 'tfidf']
    return df
```

#### Data
candles
```
                        feature     tfidf
0                 Candle Stores  0.084929
1               Religious Items  0.081032
2            Cards & Stationery  0.047412
3                Spiritual Shop  0.033402
4                    Gift Shops  0.032042
5                         Honey  0.027251
6                       Flowers  0.025061
7               Flowers & Gifts  0.021515
8                 Arts & Crafts  0.020368
9                     Tableware  0.018039
10                   Home Decor  0.017998
11                 Pop-up Shops  0.017876
12               Kitchen & Bath  0.016730
13       Psychics & Astrologers  0.016098
14                 Art Supplies  0.013669
15            Personal Shopping  0.013443
16                   Bookstores  0.013171
17                         Soba  0.011802
18  Holiday Decorating Services  0.010427
19                      Jewelry  0.009496
20                Home & Garden  0.009063
21                 Home Staging  0.008448
22                     Churches  0.008260
23          Holiday Decorations  0.008110
24                     Antiques  0.007967
```

candle
```
                    feature     tfidf
0           Religious Items  0.030887
1              Ice Delivery  0.022415
2      Immunodermatologists  0.015064
3                   Flowers  0.011941
4               Paint & Sip  0.011072
5       Holiday Decorations  0.009661
6        Cards & Stationery  0.009403
7               Art Classes  0.008631
8            Spiritual Shop  0.008376
9                Beer Tours  0.008355
10               Gift Shops  0.008291
11            Arts & Crafts  0.007063
12          Flowers & Gifts  0.006708
13               Home Decor  0.006450
14          Scavenger Hunts  0.006150
15        Religious Schools  0.006120
16             Art Supplies  0.006064
17  Religious Organizations  0.004795
18                 Churches  0.004608
19           Kitchen & Bath  0.004473
20                 Pub Food  0.004368
21             Pop-up Shops  0.004259
22            Fabric Stores  0.004176
23       Children's Museums  0.004082
24          Wedding Chapels  0.004021
```

beautiful
```
                             feature     tfidf
0                        Calligraphy  0.203983
1                            Flowers  0.171869
2                 Indoor Landscaping  0.161185
3        Holiday Decorating Services  0.139978
4                  Botanical Gardens  0.130274
5                          Art Tours  0.121111
6                           Florists  0.115861
7                     Opera & Ballet  0.102956
8                   Wedding Planning  0.097359
9                         Street Art  0.093276
10     Funeral Services & Cemeteries  0.092552
11                   Flowers & Gifts  0.090511
12  Landmarks & Historical Buildings  0.089456
13                   Cultural Center  0.085831
14                       Flyboarding  0.083697
15                        Officiants  0.083661
16                     Country Clubs  0.080936
17                    Horse Boarding  0.080295
18                   Visitor Centers  0.079797
19                             Parks  0.076435
20                             Lakes  0.075439
21                          Churches  0.074905
22           Religious Organizations  0.074841
23                         Hotel bar  0.073435
24                   Pet Photography  0.073125
```

sitting
```
0               House Sitters  0.060971
1                 Dog Walkers  0.056524
2              Outdoor Movies  0.048842
3             Home Developers  0.035570
4          Storefront Clinics  0.034827
5               Candle Stores  0.034620
6                   Hotel bar  0.033775
7        Commissioned Artists  0.025467
8              Opera & Ballet  0.024891
9                    Sledding  0.024202
10                 Synagogues  0.023304
11             Senior Centers  0.023249
12            Performing Arts  0.023239
13          Stadiums & Arenas  0.022826
14         Pet Transportation  0.021816
15                Courthouses  0.020840
16            Baseball Fields  0.019245
17                Ski Resorts  0.019219
18               Radiologists  0.018831
19               Comedy Clubs  0.018761
20               Wallpapering  0.018676
21                    Cabaret  0.018572
22  Professional Sports Teams  0.018447
23                    Reunion  0.018246
24           Fire Departments  0.018119
```

jumping
```
0         Trampoline Parks  0.107659
1                Skydiving  0.065636
2               Gymnastics  0.025378
3       Recreation Centers  0.024797
4              Skate Parks  0.022462
5            Rock Climbing  0.016727
6                Laser Tag  0.016222
7          Kids Activities  0.015811
8           Haunted Houses  0.015034
9          Amusement Parks  0.014790
10         Pumpkin Patches  0.014115
11            Hang Gliding  0.012416
12             Playgrounds  0.012118
13          Cannabis Tours  0.011604
14      Addiction Medicine  0.011549
15           Observatories  0.011336
16              Island Pub  0.009093
17          Horse Boarding  0.008428
18         Leisure Centers  0.008152
19        Attraction Farms  0.007794
20            Pop-up Shops  0.007393
21               Ziplining  0.007154
22              Boat Tours  0.006873
23  Party & Event Planning  0.006844
24                 Surfing  0.006725
```

#### Insights
Candle and Candles give different lists.  There may be some overlaps, but Candle Shops as a category wasn't even in the top 25 for "candle", while it was #1 for "candles".  We're losing out on information if we only query for one or the other.

One fix is lemmatization during the parsing/vectorizing step of the documents.  We would have only one word representing candle.

Another fix is to use word embeddings to find related words to candle.  That might lead us to candles (and probably other words too, like light, wax). Then we can combine their tfidf scores in some way to balance this out.

## TF-IDF - Most relevant words per category

### With defaults for word frequencies provided by spaCy + textacy

#### Method
```python
    terms_list = (doc.to_terms_list(ngrams=1, as_strings=True)
                  for doc in corpus)
    vect = textacy.Vectorizer(
        weighting='tfidf', normalize=True, smooth_idf=True,
        min_df=2, max_df=0.95)
```


#### Data

Sushi Bars
```
       feature     tfidf
0      sashimi  0.393490
1        spicy  0.388859
2         ayce  0.308021
3       shrimp  0.286034
4      tempura  0.263642
5     waitress  0.249857
6         miso  0.199458
7    appetizer  0.194952
8        fried  0.174852
9       nigiri  0.171359
10      buffet  0.132702
11    teriyaki  0.109078
12     seafood  0.104633
13     hibachi  0.098755
14     avocado  0.097663
15      korean  0.096322
16  happy hour  0.095917
17     scallop  0.094326
18     edamame  0.082428
19      wasabi  0.080650
20  yellowtail  0.079980
21      entree  0.075848
22         soy  0.074491
23    cucumber  0.073072
24       raman  0.072510
```

Bikes
```
        feature     tfidf
0           rei  0.832503
1       cycling  0.436514
2      warranty  0.174837
3           bmx  0.122733
4     triathlon  0.100734
5        fender  0.078735
6    suspension  0.061367
7       electra  0.059051
8         fixie  0.057893
9       bateman  0.054420
10     curbside  0.053262
11     dividend  0.053262
12         fitz  0.035894
13     puncture  0.033578
14        marty  0.032420
15         spec  0.030104
16        durst  0.027789
17      fahrrad  0.026631
18        lever  0.026631
19    alignment  0.025473
20       skiing  0.025473
21         mead  0.025473
22  diamondback  0.025473
23        thorn  0.025473
24     freeride  0.024315
```

Dance Clubs
```
      feature     tfidf
0     bouncer  0.481651
1   bartender  0.449306
2   nightclub  0.344626
3         tao  0.267550
4     marquee  0.235435
5      dancer  0.208825
6    waitress  0.196208
7     dancing  0.168069
8       vodka  0.134884
9       tryst  0.129225
10   hakkasan  0.128766
11        edm  0.105827
12  guestlist  0.100551
13     cabana  0.089999
14  surrender  0.085182
15    hostess  0.065071
16      omnia  0.064613
17       wynn  0.064536
18   stripper  0.062472
19  appetizer  0.062013
20       limo  0.052914
21     calvin  0.052837
22    concert  0.051231
23     harris  0.048249
24     tiesto  0.047102
```

#### Insight
Note that this took ~30 minutes using the spaCy library.  Need to analyze more what defaults are in textacy for tfidf.  The "reviewy" words are gone from this list, and in it's place are objects that are much more specific to the Yelp categories.

Combining the argument defaults of `sklearn.text.TfidfVectorizer` with the keywords I provided, I came up with the following parameters set:

```
decode_error=’strict’, strip_accents=None, lowercase=True, preprocessor=None,
tokenizer=None, analyzer=’word’, stop_words=ENGLISH_STOP_WORDS, 
token_pattern=’(?u)\b\w\w+\b’, ngram_range=(1, 1), max_df=1.0, min_df=1, 
max_features=None, vocabulary=None, binary=False, dtype=<class ‘numpy.int64’>, 
norm=’l2’, use_idf=True, smooth_idf=True, sublinear_tf=False
```
Now, I'll compare the parameters used for this more successful iteration.

Combining the argument defaults of `textacy.Doc.to_terms_list`,

```
terms_list = (doc.to_terms_list(ngrams=1, as_strings=True, named_entities=True, normalize='lemma', lemmatize=None, lowercase=None)
              for doc in corpus)
```

Combining the argument defaults of `textacy.Vectorizer` with the keywords I provided, I came up with the following parameters set:

```
weighting='tfidf', normalize=True, sublinear_tf=False, smooth_idf=True,
vocabulary=None, min_df=2, max_df=0.95, min_ic=0.0, max_n_terms=None
```



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
