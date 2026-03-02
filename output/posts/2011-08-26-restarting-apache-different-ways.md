---
title: "Restarting Apache, different ways"
date: 2011-08-26
author: dparizek
categories:
  - Programming
  - unix
  - Website Development
original_url: http://parizek.com/2011/08/26/restarting-apache-different-ways/
---

# Restarting Apache, different ways

Just reference for restarting apache, different strokes for different servers: `# /etc/init.d/httpd restart # /etc/init.d/httpd start # /etc/init.d/httpd stop `# service httpd restart` `# apachectl -k graceful` sometimes you need sudo because it might only see the path from root