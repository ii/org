+++
title = "How ii makes APISnoop releases"
author = ["Berno Kleinhans"]
date = 2021-04-22
lastmod = 2021-04-24T08:56:49+12:00
tags = ["kubernetes", "apisnoop", "cncf"]
categories = ["guides"]
draft = false
weight = 2005
summary = "Document with intent on knowledge share: The process APISnoop goes through to build images and understanding tags role"
+++

## This is how ii makes apisnoop releases {#this-is-how-ii-makes-apisnoop-releases}

In this post we will capture the details involved in building and promoting a image from the apisnoop repo


## Repo and the tags we have: {#repo-and-the-tags-we-have}

<https://github.com/cncf/apisnoop/tags>


## Overview of image publish jobs and how we can use them to promote our images {#overview-of-image-publish-jobs-and-how-we-can-use-them-to-promote-our-images}

Documentation: [test-infra-config/jobs/image-pushing/README](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#image-pushing-jobs)

-   We set up a [GCR](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#managing-kubernetes-container-registries) to build our images
-   We set up a image [promoter](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#image-promoter)


## Prow definition of image-build for apisnoop: {#prow-definition-of-image-build-for-apisnoop}

-   Use this [documentation](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md), the  [prow-config-template](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#prow-config-template)  is very strict.
-   This the postsubmit job we defined in
    [test-infra/config/jobs/image/pushing/k8s-staging-apisnoop.yaml](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/k8s-staging-apisnoop.yaml)

<!--listend-->

```yaml
  decorate: true
      branches:
        - ^main$
```

```yaml
containers:
          - image: gcr.io/k8s-testimages/image-builder:v20210302-aa40187
            command:
              - /run.sh
            args:
              # this is the project GCB will run in, which is the same as the GCR images are pushed to.
              - --project=k8s-staging-apisnoop
              - --scratch-bucket=gs://k8s-staging-apisnoop-gcb
              - --env-passthrough=PULL_BASE_REF
              - apps/snoopdb
```


## The cloudbuild.yaml this job runs {#the-cloudbuild-dot-yaml-this-job-runs}

[cncf/apisnoop/apps/snoopdb/cloudbuild.yaml](https://github.com/cncf/apisnoop/blob/main/apps/snoopdb/cloudbuild.yaml)

```yaml
steps:
  - name: gcr.io/cloud-builders/docker
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/snoopdb:$_GIT_TAG',
           '--build-arg', 'IMAGE_ARG=gcr.io/$PROJECT_ID/snoopdb:$_GIT_TAG',
           './postgres']
images:
  - 'gcr.io/$PROJECT_ID/snoopdb:$_GIT_TAG'
substitutions:
  _GIT_TAG: '12345'
options:
  substitution_option: 'ALLOW_LOOSE'
```


## Prow jobs to build/push snoopdb: {#prow-jobs-to-build-push-snoopdb}

Where you can find the above job in prow: [prow-apisnoop-push-snoopdb-images](https://prow.k8s.io/?job=apisnoop-push-snoopdb-images)


## Logs {#logs}

Logs for the above [prow-logs-apisnoop-push-snoopdb-images](https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/apisnoop-push-snoopdb-images/1384977461019676672)


## GCB Requires a promotion process {#gcb-requires-a-promotion-process}

Some information om image [promotion process](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#readme)

-   Make changes to k8s.io.k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml
-   Create PR that will then trigger a check that k8s-ci-robot gets 'Job succeeded'
-   The merged PR will trigger the promotion 'post-k8sio-cip'
-   Promoted images can be viewed on [k8s-artifacts-prod](https://console.cloud.google.com/gcr/images/k8s-artifacts-prod)

Options for using tags [tags-custom-substitutions](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#custom-substitutions)
Apisnoop image file that holds our metadata: [k8s.io/k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml)


## Promotion Definitions {#promotion-definitions}

Infra promotor:


### [Presubmits](https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes/sig-release/cip/container-image-promoter.yaml#L1) {#presubmits}


### [Postsubmits](https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes/wg-k8s-infra/trusted/releng/releng-trusted.yaml#L3) {#postsubmits}


## Promotion Jobs {#promotion-jobs}

<https://prow.k8s.io/?job=post-k8sio-image-promo>
