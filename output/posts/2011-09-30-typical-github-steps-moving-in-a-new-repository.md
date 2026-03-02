---
title: Typical github steps moving in a new repository
date: 2011-09-30
author: dparizek
categories:
  - git
  - Programming
  - Website Development
original_url: http://parizek.com/2011/09/30/typical-github-steps-moving-in-a-new-repository/
---

# Typical github steps moving in a new repository

Global setup: Set up git `git config --global user.name "Dave Parizek" git config --global user.email dude@wherever.com` Next steps: `mkdir UAC cd UAC git init touch README git add README git commit -m 'first commit' git remote add origin git@github.com:BioComputing/UAC.git git push -u origin master` Existing Git Repo? `cd existing_git_repo git remote add origin git@github.com:BioComputing/UAC.git git push -u origin master`