---
title: "Oops, deleted super user Drupal 6, what to do?  maybe you emptied user table?"
date: 2011-06-04
author: dparizek
categories:
  - Drupal
  - Programming
  - Website Development
original_url: http://parizek.com/2011/06/04/oops-deleted-super-user-drupal-6-what-to-do-maybe-you-emptied-user-table/
---

# Oops, deleted super user Drupal 6, what to do?  maybe you emptied user table?

I left my thinking cap off and emptied the user table of a dev Drupal 6 site I was working on. If that happens to you, just access your database with phpMyAdmin or similar, and: `INSERT INTO users (uid, name, pass) VALUES ('1', 'yourname', md5('yourpassword')); ` then edit the users table further to add your email address and set status = 1.