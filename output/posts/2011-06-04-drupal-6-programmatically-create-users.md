---
title: Drupal 6 Programmatically Create Users
date: 2011-06-04
author: dparizek
categories:
  - Drupal
  - Programming
  - Website Development
original_url: http://parizek.com/2011/06/04/drupal-6-programmatically-create-users/
---

# Drupal 6 Programmatically Create Users

How to programmatically create new users in Drupal 6: ` 'username', 'pass' => 'password', // note: do not md5 the password 'mail' => 'email address', 'status' => 1, 'init' => 'email address' ); user_save(null, $newUser); ?>` To update an existing user: `some_property = 'what_you_want_to_set_it_to'; // save existing user user_save((object) array('uid' => $existingUser->uid), (array) $existingUser); ?>`