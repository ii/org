+++
title = "New Contributor Summit Session 03"
author = ["Zach Mandeville"]
date = 2021-02-05
lastmod = 2021-02-05T16:00:03+13:00
tags = ["kubernetes", "ncw", "testing"]
categories = ["guides"]
draft = true
weight = 2004
summary = "Part Three to our intro to testing for new K8s contributors"
[menu.main]
  weight = 2004
  identifier = "new-contributor-summit-session-03"
+++

## Introduction {#introduction}

In this, we'll ramp up our abilities by adding testing into the mix!
Like session 2, we will edit, make, and run commands like kubectl, but now checking our builds with unit testing, using go test.
With these tests, we'll have increased confidence in contributing our work back upstream and so we'll also talk about pull requests, and the PR pre-submission practices.


## Agenda {#agenda}

-   Setup our Dev environments
-   introduce unit tests
-   testing with go test and make
-   PR's
-   An intro to prow and test grid


## Setup {#setup}


### Kind {#kind}


### a working kubectl binary of some sort {#a-working-kubectl-binary-of-some-sort}


### go {#go}


### make {#make}


## Edit our kubectl binary {#edit-our-kubectl-binary}

Adjust its message again, or have it do something in addition
don't build just yet


## Unit Tests {#unit-tests}


### what are they? {#what-are-they}


### why they important? {#why-they-important}


### how k8s uses them {#how-k8s-uses-them}


## Write a unit test for our kubectl binary {#write-a-unit-test-for-our-kubectl-binary}


## check our test with go test {#check-our-test-with-go-test}


## check our test with make {#check-our-test-with-make}


## Test scope {#test-scope}


### only run some tests {#only-run-some-tests}


### run all tests {#run-all-tests}


### time to run all tests {#time-to-run-all-tests}


## PR's {#pr-s}

-   review the pr flow again
-   review the PR pre-submission guidelines
-   review the style guidelines
-   show some of the checks done on an existing pr and the checks for the pre-submission and style
-   what is doing these checks?


## Prow {#prow}


### k8s git ops {#k8s-git-ops}


### helps manage these steps of the pr {#helps-manage-these-steps-of-the-pr}


### ensures yr pr follows the guidelines and passes all existing tests. {#ensures-yr-pr-follows-the-guidelines-and-passes-all-existing-tests-dot}


## Testgrid {#testgrid}


### show all the tests being run and their success {#show-all-the-tests-being-run-and-their-success}


### this can be optional, and so {#this-can-be-optional-and-so}


## Additional Help {#additional-help}


## What's Next? {#what-s-next}
