---
title: Towards Getting Drupal's WebForms Functionality in Angular JS
date: 2014-07-04
author: dparizek
categories:
  - Angular JS
  - Javascript
  - Programming
original_url: http://parizek.com/2014/07/04/towards-getting-drupals-webforms-functionality-in-angular-js/
---

# Towards Getting Drupal's WebForms Functionality in Angular JS

Drupal Webforms (<https://drupal.org/project/webform>) lets power users create their own forms through a web interface, choosing the types, labels, number, etc. of fields they want. It then can present the form to final end users to fill out, and collects the data in the database. Admins can then view the results tabularized online or download as CSV.

I want to see the same available for a Angular / Django stack. 

Already someone has form generation from simple json descriptions - this being a tool to make form code faster to write for developers:

<https://github.com/danhunsaker/angular-dynamic-forms>

Someone else has started on form creation by users: this app allows users to spec out their forms and then it generates most of the angular code for the form:

<http://selmanh.github.io/angularjs-form-builder/#/>

<https://github.com/selmanh/angularjs-form-builder/>

By most, I think it does not yet handle saving the form to your server database.

Which makes sense as that would vary by backend.

Perhaps even better, another similar effort but with drag and drop to build bootstrap forms:

<http://kelp404.github.io/angular-form-builder/>

Either of these would be excellent open source projects to contribute to if any student devs are looking for cool stuff to do in their free time.

Drupal Webform has one maybe "fault" - it saves results from one form submission all together in the database as one results field - as a long string of concatenated key/value pairs. Probably this is ok, maybe even best approach - you could still make the admin table of results sortable and filterable by just doing that fully on the client side.

So to get to Webforms, above needs to extended - add autogeneration to include code to send json of results to django database via restangular and django rest frameworks api/deserializer and then front end admin interface so that admins can have a tabular view of all submissions and then an option to download those submissions as CSV. So for the admin view you would just throw them into an ng-grid (<http://angular-ui.github.io/ng-grid/>) or better yet it would be nice to try ng-table <http://bazalt-cms.com/ng-table/> which has download as CSV already built in.