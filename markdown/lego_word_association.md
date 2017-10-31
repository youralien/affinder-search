# Defining “searchable/discoverable” word associations for legos #affordanceaware
This example is about the various activities related to user movement.

Imagine we have a movement detector, which tracks the context of a user 


## Finding word analogies and associations using Embeddings
```
kw: walking
[u'walk', u'jogging', u'walks', u'strolling', u'walked', u'stroll', u'walkin', u'biking', u'walkers', u'horseback']
kw: moving
[u'moved', u'move', u'relocating', u'moves', u'settling', u'turning', u'shifting', u'going', u'changing', u'transferring']
kw: sitting
[u'seated', u'sit', u'standing', u'sittings', u'staring', u'sits', u'benches', u'reclining', u'propped', u'sittin']
```

## Defining word utterances that should be associated with legos
##### Method
```
EMB = KeyedVectors.load_word2vec_format('wiki.en/wiki.en.vec',
                                        limit=100000)
print(map(lambda x: x[0], EMB.most_similar(raw_input("kw: "))))
```

```
{
	"outside": [
		"bicycling",
		"bike",
		"biking",
		"camp",
		"camping",
		"hike",
		"hiking",
		"race",
		"run"
	],
	"inside": [
		"run",
		"shop",
		"shopping",
	],
	"high-elevation": [
		"ski",
		"skiing"
	],
	"body-of-water": [
		"surf",
		"surfing",
		"swim",
		"swimming"
	],
	"snowing": [
		"ski",
		"skiing",
		"snowboard",
	],
	"moving": [
		"walking",
		"running",
      "going",
	],
	"not-moving": [
  	    "sitting",
		"seated",
		"standing"
		"staring"
	],
	"high-elevation": [
		"mountains"
	]
}
```

##### Insights, techniques for moving forward
This begs the question that if **someone defines the the “sitting” affordance** with a rule like “location not moving”, **we can generalize the rule** to other related non-moving words, like “seated”, “standing”, and “staring”. *Starting with some data, we can build out a larger set of affordances to start*

Case Based Reasoning — using solutions to similar problems, based on the history of what problems you solved.  In this context, using similar legos to define affordances that are similar to affordances the engine has encountered before (either by creator definition, or user definition)

I think “staring” is pretty fascinating, because “staring” at the TV also implies that you might be stationary, or “staring” at the the computer implies the same thing.

How do we define whether we are staring at the sunset vs staring at the TV?  One of them is outside one of them is inside.  We can have additional legos coming in that richen the context of what “action” or “staring” is happening.

How is this different than a user just saying “yes I want a moving” lego?  

### Case Study of using Embedding Expansions to find relevant matching legos:

```
Type a natural language affordance requirement:
workout
{'affordance.   ': 'workout',
 'expanded words': set([u'aerobic',
                        u'aerobics',
                        u'anorexia',
                        u'athleticism',
                        u'auditoriums',
                        u'ballrooms',
                        u'bicycling',
                        u'biking',
                        u'bodybuilding',
                        u'bulimia',
                        u'bungee',
                        u'cafeteria',
                        u'cafeterias',
                        u'calorie',
                        u'cardiac',
                        u'cardio',
                        u'cardiology',
                        u'cardiopulmonary',
                        u'cardiothoracic',
                        u'cardiovascular',
                        u'classrooms',
                        u'contraption',
                        u'deceleration',
                        u'diet',
                        u'dietary',
                        u'dieting',
                        u'diets',
                        u'eating',
                        u'fitness',
                        u'gym',
                        u'gymnasium',
                        u'gymnasiums',
                        u'gymnastic',
                        u'gymnastics',
                        u'gyms',
                        u'hiking',
                        u'hydrotherapy',
                        u'jogging',
                        u'locker',
                        u'lockers',
                        u'massage',
                        u'myocardial',
                        u'nutrition',
                        u'nutritional',
                        u'obesity',
                        u'offseason',
                        u'orthopedic',
                        u'orthopedics',
                        u'paddling',
                        u'physiotherapy',
                        u'picnicking',
                        u'pilates',
                        u'playgrounds',
                        u'pulley',
                        u'racquetball',
                        u'regimen',
                        u'sledding',
                        u'sprained',
                        u'sunbathing',
                        u'tether',
                        u'trampoline',
                        u'treadmill',
                        u'tryout',
                        u'tryouts',
                        u'unicycle',
                        u'walking',
                        u'weightless',
                        u'weightlessness',
                        u'wellness',
                        'workout',
                        u'workouts',
                        u'yoga']),
 'keywords      ': set([u'aerobic',
                        u'aerobics',
                        u'anorexia',
                        u'athleticism',
                        u'auditoriums',
                        u'ballrooms',
                        u'bicycling',
                        u'biking',
                        u'bodybuilding',
                        u'bulimia',
                        u'bungee',
                        u'cafeteria',
                        u'cafeterias',
                        u'calorie',
                        u'cardiac',
                        u'cardio',
                        u'cardiology',
                        u'cardiopulmonary',
                        u'cardiothoracic',
                        u'cardiovascular',
                        u'classrooms',
                        u'contraption',
                        u'deceleration',
                        u'diet',
                        u'dietary',
                        u'dieting',
                        u'diets',
                        u'eating',
                        u'fitness',
                        u'gym',
                        u'gymnasium',
                        u'gymnasiums',
                        u'gymnastic',
                        u'gymnastics',
                        u'gyms',
                        u'hiking',
                        u'hydrotherapy',
                        u'jogging',
                        u'locker',
                        u'lockers',
                        u'massage',
                        u'myocardial',
                        u'nutrition',
                        u'nutritional',
                        u'obesity',
                        u'offseason',
                        u'orthopedic',
                        u'orthopedics',
                        u'paddling',
                        u'physiotherapy',
                        u'picnicking',
                        u'pilates',
                        u'playgrounds',
                        u'pulley',
                        u'racquetball',
                        u'regimen',
                        u'sledding',
                        u'sprained',
                        u'sunbathing',
                        u'tether',
                        u'trampoline',
                        u'treadmill',
                        u'tryout',
                        u'tryouts',
                        u'unicycle',
                        u'walking',
                        u'weightless',
                        u'weightlessness',
                        u'wellness',
                        'workout',
                        u'workouts',
                        u'yoga']),
 'legos         ': ['moving', 'outside']}
```
## Using Dictionary Definitions
Affordance: someone at a stadium
or someone in crowd looking with anticipation

Stadium: a sports arena with tiers of seats for spectators.

