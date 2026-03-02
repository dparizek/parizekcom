---
title: git insufficient permission for adding an object to repository database ./objects
date: 2011-05-19
author: dparizek
categories:
  - git
  - Programming
  - unix
  - version control
  - Website Development
original_url: http://parizek.com/2011/05/19/git-insufficient-permission-for-adding-an-object-to-repository-database-objects/
---

# git insufficient permission for adding an object to repository database ./objects

strangely, I had been pushing to this repository for weeks no problems. Then one day I get the error message for the title above: ` $git push Counting objects: 9, done. Delta compression using up to 2 threads. Compressing objects: 100% (5/5), done. Writing objects: 100% (5/5), 506 bytes, done. Total 5 (delta 2), reused 0 (delta 0) error: insufficient permission for adding an object to repository database ./objects fatal: failed to write object error: unpack failed: unpack-objects abnormal exit ` I was a member of the group in question, checked via: `$ groups myusername` and verified that group had write permissions: `$ ls -la` Turned out a few files had shown up in the object directory with different permissions. **To fix:** `ssh to server cd your-repository.git` `sudo chmod -R g+ws * sudo chgrp -R yourgroup *` and maybe: `git repo-config core.sharedRepository true` and then try to push again
---

## Comments

**Dan Course** — 2011-08-04 10:13:32

Thanks, got me out of a kerfuffle with our new server!

**David Mann** — 2012-02-12 20:51:40

Thanks heaps mate, fixed it for me after my private Git repo stopped working out of no where.

**Fab** — 2012-08-17 02:15:36

Saved my day! 
Thanks !

Note: I had to do a chown -R also.
