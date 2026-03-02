---
title: Drupal Classified Ads Modules Options / Choices / Comparisons
date: 2010-01-04
author: dparizek
categories:
  - Drupal
  - Website Development
tags:
  - CCK
  - classified ads module
  - classifiQ
  - Views
  - website building
original_url: http://parizek.com/2010/01/03/drupal-classified-ads-modules-options-choices-comparisons/
---

# Drupal Classified Ads Modules Options / Choices / Comparisons

This post discusses the options / choices for having classified ads on Drupal websites. So it is a comparison of classified ad solutions for Drupal, if you will. Drupal is an open source content management system for building websites and it has lots of contributed modules that can often solve your needs without any custom programming on your own part. And luckily, there are at least two contributed modules for classified ads, plus the more jack of all trades modern solution of using the CCK and Views modules to roll it together. I want the ability for users to add and edit classified ads. There is a [Classified Ads drupal module](<http://drupal.org/project/ed_classified>) available, that allows just this functionality. The only problem is that it requires the ads to expire at some point, and then removes them from your site. I do not like this because I would rather have items marked "Sold" or "No Longer For Sale" instead of being deleted. Why? Because I want the content to stay forever, for SEO reasons. Webmasters developing content websites work so hard to get content, why give any of it up? I do like however that it integrates a "My Classified Ads" tab into the user profile "My Account" pages, and that it handles email notifications to remind customers when their ads are going to expire. Very nice features. Another alternative is just to create a new content type for ads (using CCK), and then create views to handle display. This does not give you a tab on the user profiles page, although they can view their ads from their "My account" page by clicking on the "Track" tab if you have enabled the Tracker module. Another alternative is the drupal module [Zipsads](<http://drupal.org/project/zipsads>). This was overkill for me, I did not want to link ads to zip codes, as I wanted all ads to be worldwide. There is one other classified ads Drupal module, called [classifiQ](<http://drupal.org/project/classifiQ>) but there is no published release for it. So oh well there. I think my solution will be to create the ads using the CCK / Views option, and down the line when I get time figure out how to code in a custom tab in the user profile. Well, but I like the idea of getting rid of old ads. But what about if people link to them? I do not want to lose the link juice. Maybe what is needed is a redirect solution for 404 errors in general, or else specifically for expired (and thus unpublished) ads... so that it redirects to the main classified ad page. Any ideas?