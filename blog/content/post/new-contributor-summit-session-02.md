+++
title = "New Contributor Summit Session 02"
author = ["Zach Mandeville"]
date = 2021-02-05
lastmod = 2021-02-05T15:58:25+13:00
tags = ["kubernetes", "ncw", "testing"]
categories = ["guides"]
draft = true
weight = 2003
summary = "Part Two to our intro to testing for new K8s contributors"
[menu.main]
  weight = 2003
  identifier = "new-contributor-summit-session-02"
+++

## Introduction {#introduction}

-   In this Session we will introduce you to the make command and kubernetes cmd folder.
-   You'll also learn about KinD (kubernetes in docker)
-   We'll learn more about how k8s buid process works

    By the end, you will edit and build a kubernetes command that you can run on your own kind cluster!
    ****This session continues on Session 1.  If you haven't done that one yet, do it first!****


## Agenda {#agenda}

-   Intro to make
-   Intro to CMD
-   The Build Process
-   Intro to KinD
-   Editing and Building
-   Running our command on KinD


## Make {#make}


### What it is {#what-it-is}


### Ensuring you have it on your computer {#ensuring-you-have-it-on-your-computer}


### How we use it {#how-we-use-it}


## The CMD Folder {#the-cmd-folder}


### Where to find it {#where-to-find-it}


### What it is {#what-it-is}


## Making in Parts {#making-in-parts}

Why do we not make all of kubernetes (no don't run make release)
What do we make in isolation?


## Verify Dev envrionment ready to go {#verify-dev-envrionment-ready-to-go}

_if needed, include instructions for each type of OS_


### Have Docker {#have-docker}


### Have git {#have-git}


### Have Go {#have-go}


#### GOPATH set {#gopath-set}


### Fork of k8s cloned to dev environment {#fork-of-k8s-cloned-to-dev-environment}


## Run a make command {#run-a-make-command}


### cd into k8s from yr terminal {#cd-into-k8s-from-yr-terminal}


### make WHAT=cmd/kubectl {#make-what-cmd-kubectl}

maybe edit the print output for fun, and see it change


## Make a KinD Cluster {#make-a-kind-cluster}


### What is kind? {#what-is-kind}


### Install Kind {#install-kind}


### kind create cluster {#kind-create-cluster}


## Use newly-built kubectl binary in the KinD cluster {#use-newly-built-kubectl-binary-in-the-kind-cluster}


## Additional Help {#additional-help}


## What's Next? {#what-s-next}
