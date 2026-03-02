---
title: Exploring encryption / security in Django apps; dealing with PHI in web apps
date: 2014-07-04
author: dparizek
categories:
  - Programming
original_url: http://parizek.com/2014/07/04/exploring-encryption-security-in-django-apps-dealing-with-phi-in-web-apps/
---

# Exploring encryption / security in Django apps; dealing with PHI in web apps

review video: <http://pyvideo.org/video/1381/cryptography-for-django-applications>

general Django security: <http://www.djangobook.com/en/2.0/chapter20.html>

cryptographic signing - perhaps to generate one-time url for results download

<https://docs.djangoproject.com/en/dev/topics/signing/>

encrypted fields: <https://github.com/svetlyak40wt/django-fields>

more encrypted fields:

<https://github.com/defrex/django-encrypted-fields>,

<https://github.com/django-extensions/django-extensions>

<http://gpiot.com/blog/encrypted-fields-pythondjango-keyczar/>

but once encrypted, then cannot query or sort

so presumably use two stage system:

stage 1 - intake, more open access, collects data over https, encrypts into postgres, then transferred to stage 2 - only current data and only certain fields kept post transfer to stage 2

So if comprised, limited data exposed.

stage 2 - not encrypted, limited access

So quarantine and encryption doing the protection.

stage 2 could be encrypted, but then for client use all data would need to go to client and sorting / filtering happens in client. seems just as secure overall to just limit access in stage 2.

How to manage transfer process? Add a succession number to track which items have been transferred. do transfers on cron schedule, or everytime new data comes in to stage 1. need a policy for expiration at stage 1.

What about overall security model?

<http://security.stackexchange.com/questions/16939/is-it-generally-a-bad-idea-to-encrypt-database-fields>

another slightly more sophisticated approach:

<http://dspace.mit.edu/bitstream/handle/1721.1/82382/862075374.pdf?sequence=1>

From Client-side Encryption to Secure Web Applications by Emily Stark Submitted to the Department of Electrical Engineering and Computer Science on April 24, 2013, in partial fulfillment of the requirements for the degree of Master of Science in Computer Science and Engineering Abstract This thesis presents an approach for designing secure web applications that use client-side encryption to keep user data private in the face of arbitrary web server compromises, as well as a set of tools, called CryptFrame, that makes it easier to build such applications. Crypt- Frame allows developers to encrypt and decrypt confidential data in the user's browser. To ensure an adversary cannot gain access to the decryption keys or plaintext data, CryptFrame provides a browser extension that stores the keys and allows only sensitive regions in the web page to access them. CryptFrame performs templatized verification of sensitive regions to grant small amounts of trusted client-side code access to plaintext data in the browser. Finally, CryptFrame provides a principalgraph to help users safely change permissions on shared data in the presence of active adversaries. We use CryptFrameto modify several existing Django-based applications, requiring few source code modifications and incurring moderate performance overhead. Thesis Supervisor: Nickolai Zeldovich Title: Associate Professor