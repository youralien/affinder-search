# Interface to creating Affordance Aware Engine Queries #affordanceaware
## What do I want to accomplish by end of quarter?

#### Storytime Example Affordances not satisfiable with just Yelp Places

Someone walking their dog
People who can catch falling leaves from trees on a windy day
Anyone in a rush
People at crowded locations
Someone on a crowded sidewalk
Someone in a group at dinnertime
People who have puddles to splash in and the rain boots to do it!
2 people on a bench
4 people together willing to act out a zombie scene
Someone who is preparing food
Someone in an empty space
Someone in a quiet space
A person who has access to a glass object
A scenic place with few toursists. Like a desserted island or something
A person in a backyard playing with their kids
Someone who just woke up out of a dream/daydream
(Where are you walking into/out of? - Class, commute to work, commute to home)
Is reading

#### Affordances that need to be built
*Is walking*  vs Is stationary
Is outside or do you want is near the outside?

#### Seeking New Understanding: Search Interface for Contextual Building Blocks

"Natural Language -> Keywords -> Context Building Blocks. Example: ""someone riding bike downtown"" -> (""riding"", ""bike"", ""downtown"") -> *Relevant Contextual Building Blocks* -> Use human-logic to compose them.

1) A search interface for contextual building blocks, rather than requiring composition of them directly from a list of available blocks (solved: the number of available contextual building blocks would be too numerous ot enter manually)

2) A way to find contextual building blocks that are about
* You image process areas that people walk to in their first day.  You compute  on Google Maps only on areas that they explore.  Cache things you have good bets on will pay off soon.
* Activities People are participating in
	* We can find verbs in the query and build “activity” legos instead of “location” legos.  
		* walk -> isWalking
	* We use derived context of course
		*  delta-location to see if someone is moving
		* i.e. where they are, based on their history
		* where are they going, based on what time it is in their schedule
		* where they are going, based on the semantics of a geofence we learn from history or they specify
	* *Activities run on Habits*
		* Walking your dog… we can infer that if we know that you usually go around this area, around this time, to walk your dog. 
		* “Everyone’s normal activities” if people are logging them, or we are learning from their habits and get uncertain labels like “a snap of them walking their dog” we can start building models.  
			* It’s like your friends knowing you went for a dog walk.  This is like the machine facilitating contextual interactions… like a friend now asking how was your dog walk?  Oh I didn’t go out today for that, I was actually out doing grocery shopping. Oh! But you usually go out now for walking… yes but.
* Based on people’s identity
* Social
	* Participants: If you take a group selfie, or if there are many people in a crowd around you, or if there’s lots of GPS dots densely clustered around you, you form potential for community. 
	* Creators: 
		* Interfaces for “people in crowds near each other” - through demonstrations of clusters?
		* Interfaces for “what I want to see in people’s Snap stories”
		* “Test cases” to see what flows through this composition, what fires. (Inspired by Zapier)
* Time, Weather
	* These are clear knobs, which don’t require “discovery”.
	* ^^^ I’d challenge that.  People who can sunbathe has some implicit meaning behind it, that it could only work in places in which it is daytime.
	* Controlling these knobs
		* Daytime, Sunrise (words that correspond to blocks of time)
		* 11 - 3 -> 11 or 12 or 1 or 2
	* Q: When to give user control over these knobs? 
		* Sunbathing, you probably want it to happen implicitly.  Beach vs (Beach && Sunny)
		* Riding bike downtown (do you want it day time so it’s crowded rush hour, or do you want an intimate scene with someone biking down a deserted, road?… or is time of day not a good feature for getting at this aspect you want in a scene?)
* General Place Categories
	* Finding the contextual building blocks
		* Words related to place categories
	* Composing them
		* Mostly OR’s right?  I want people at parks or beaches or outside  

### DESIGN CHARACTERISTICS

##### Natural Language Input
Riding Bikes Downtown (because I want to bring together people who care about bike safety in crowded neighborhoods)

##### Specifying Leggo’s myself as an Example
*Geography/Location*: Want to express… crowded places.  So… that could use some work on geography.  Downtowns, Chinatowns

### Reminding the user the user of the available options of decision blocks.
Inside/outside… moving/or not.  These are important building blocks!  If we make small predictions about them, but then surface them to the user, we can still make them aware of them.  They can still correct it (even if your predictions are inaccurate).

#### Predicting building blocks like activity, which aren’t from the same Yelp Places review data distribution
