---
title: Exploring Meteor JS
date: 2014-07-08
author: dparizek
categories:
  - Javascript
original_url: http://parizek.com/2014/07/08/exploring-meteor-js/
---

# Exploring Meteor JS

I studied meteor.js for about 10-12 hours last weekend.

Sharing my impressions:

FAST DEVELOPMENT - if it can work for your project, you can develop in maybe half the time as say angular/django or django by itself even. Maybe even faster than that. Seriously. Watch the short screencast on their home page to get a feel for it: <https://www.meteor.com/>

Basically it mirrors a lot of the datastore in the client and seamlessly keeps the two in sync. So you don't have to worry as a developer about the backend as much - no writing api endpoints, no writing the code gluing front and back together, etc. Validation code can be written once and used both client and server side. Cool latency compensation. User accounts already plug and play - no big hassle getting that set up, one liner and you are good to go, which is sweet time saver. Community contribs get you CRUD admin with a one liner, and reactive forms that save a lot of work. Read full list on their front page of cool features.

short learning curve - it is easy to learn and would be ideal for situations like BCF's where we need to get student programmers up to speed quick.

Based on Mongo - this is part of why it is fast dev. But also the big down point. Schema free document store for persistence makes things go faster in dev, but you really have to know your use cases, queries needed, etc up front. In some ways it is not as amenable to change as a relational data store (in other ways it is totally pliable). And can have issues with relational integrity.

See <http://www.sarahmei.com/blog/2013/11/11/why-you-should-never-use-mongodb/> but understand there are lots of valuable retorts in the comments and elsewhere.

Meteor is not at 1.0 yet. And they are adding support for other backends, like MySQL is likely usable now, and will get even more robust quickly. I think another 6 months and meteor is going to be getting huge attention when they release 1.0.

The ecosystem is surprisingly extensive with tons of community contributions. As extensive as angular's it seemed to me.

And there is a good book on it here <https://www.discovermeteor.com/>