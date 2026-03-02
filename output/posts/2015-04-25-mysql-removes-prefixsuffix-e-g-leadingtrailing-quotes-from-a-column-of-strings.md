---
title: MySQL how to remove prefix/suffix e.g. leading/trailing quotes from a column of strings
date: 2015-04-25
author: dparizek
categories:
  - SQL
original_url: http://parizek.com/2015/04/25/mysql-removes-prefixsuffix-e-g-leadingtrailing-quotes-from-a-column-of-strings/
---

# MySQL how to remove prefix/suffix e.g. leading/trailing quotes from a column of strings

`update table set column = trim(BOTH '"' FROM column);` For example, above removes the leading and trailing (prefix/suffic) quotes that excel adds upon csv export. You could Select records with a prefix that was a quote (") this way: `SELECT * FROM table WHERE column like '"%'` or a suffix quote (") this way: SELECT * FROM table WHERE column like '%"'