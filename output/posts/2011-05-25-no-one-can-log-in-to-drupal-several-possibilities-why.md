---
title: "No one can log in to Drupal, several possibilities why"
date: 2011-05-25
author: dparizek
categories:
  - Drupal
  - Programming
  - Website Development
original_url: http://parizek.com/2011/05/25/no-one-can-log-in-to-drupal-several-possibilities-why/
---

# No one can log in to Drupal, several possibilities why

You have a Drupal site that is working fine, and then you discover it seems like all of a sudden, no one can login. This happened to me, and it turned out to be connected to setting the cookie domain in the settings.php file. I set it at FCK Editor's bequest. And then all heck broke loose, no one could log in. Commenting out the cookie domain line in the settings.php file solved the problem. If you are moving between production and development versions of a site, then also check the cookie domain setting the sites/default/settings.php is correctly set for each installation. Another time, it was connected to a cookie domain issue in which Drupal had upgraded how cookies were handled, and if the cookie domain line was set, users had to delete their old cookies in order to be able to log in. I think this happened around the updates somewhere between Drupal 6.16 to 6.20. It looks in general like if you are experiencing this issue, no one can login, and it is not the cookie domain issue I had, then investigate as such: i.e. other things to potentially try: repair your database tables with phpMyAdmin or similar, in particular, the Sessions table. Empty your cache tables - this unlikely to be relevant, but heh I just like clearing them out, it makes me feel good, like everything feels neater and tidier that way :) Delete the browser cookies associated with the site in question. Most likely it is cookie related somehow. Any one else have this problem, and it be a different fix? Please comment and let us know...