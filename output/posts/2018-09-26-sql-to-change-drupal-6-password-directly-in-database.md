---
title: SQL to change Drupal 6 password directly in database
date: 2018-09-26
author: dparizek
categories:
  - Uncategorized
original_url: http://parizek.com/2018/09/26/sql-to-change-drupal-6-password-directly-in-database/
---

# SQL to change Drupal 6 password directly in database

Need to change a Drupal 6 user password in your database using the command line or a tool like PhpMyAdmin or MySQL Workbench? Use SQL like this: 
    
    
    update `users` set `pass` = MD5('NewPassword') where `uid` = 1;
    

or 
    
    
    update `users` set `pass` = MD5('NewPassword') 
    where `mail` = 'useremailaddress';

In the first case I'm updating the password for the Drupal user whose uid is 1, and I'm making their new password 'NewPassword'. In the second case I'm updating the password for the Drupal user whose email address is 'useremailaddress', and I'm making their new password 'NewPassword'.