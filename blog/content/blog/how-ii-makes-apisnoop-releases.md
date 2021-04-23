+++
title = "How ii makes APISnoop releases"
author = ["Berno Kleinhans"]
date = 2021-04-22
lastmod = 2021-04-24T08:30:07+12:00
tags = ["kubernetes", "apisnoop", "cncf"]
categories = ["guides"]
draft = false
weight = 2005
summary = "Document with intent on knowledge share: The process APISnoop goes through to build images and understanding tags role"
+++

## This is how ii makes apisnoop releases {#this-is-how-ii-makes-apisnoop-releases}


## Starting repo and the tags we have: {#starting-repo-and-the-tags-we-have}

<https://github.com/cncf/apisnoop/tags>


## Overview of image publish jobs and how we can use them to promote our images: [test-infra-config/jobs/image-pushing/README](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#image-pushing-jobs) {#overview-of-image-publish-jobs-and-how-we-can-use-them-to-promote-our-images-test-infra-config-jobs-image-pushing-readme}

<https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#image-pushing-jobs>

-   We set up a [GCR](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#managing-kubernetes-container-registries) to build our images in (<https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#managing-kubernetes-container-registries>)
-   We set up a image promoter [promoter](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#image-promoter)  (<https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/README.md#image-promoter>)


## Prow definition of image-build for apisnoop: {#prow-definition-of-image-build-for-apisnoop}

Use the [documentation](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md)
The use of this template is very restricted [prow-config-template](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#prow-config-template)  (<https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#prow-config-template>)

These are postsubmit jobs we defined [test-infra/config/jobs/image/pushing/k8s-staging-apisnoop.yaml](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/k8s-staging-apisnoop.yaml)
<https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/k8s-staging-apisnoop.yaml>

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
<https://github.com/cncf/apisnoop/blob/main/apps/snoopdb/cloudbuild.yaml>

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
<https://prow.k8s.io/?job=apisnoop-push-snoopdb-images>


## Logs {#logs}

Logs for the above [prow-logs-apisnoop-push-snoopdb-images](https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/apisnoop-push-snoopdb-images/1384977461019676672)
<https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/apisnoop-push-snoopdb-images/1384977461019676672>


## GCB Requires a promotion process {#gcb-requires-a-promotion-process}

Some information om image [promotion process](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#readme)
<https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io#readme>
Options for using tags [tags-custom-substitutions](https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#custom-substitutions)
<https://github.com/kubernetes/test-infra/blob/master/config/jobs/image-pushing/README.md#custom-substitutions>
This file contains the image metadata [k8s.io/k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml](https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml)
<https://github.com/kubernetes/k8s.io/blob/main/k8s.gcr.io/images/k8s-staging-apisnoop/images.yaml>


## Promotion Definitions {#promotion-definitions}


### Presubmits {#presubmits}

I am not 100% how this gets used
TODO: Get additional information
<https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes/sig-release/cip/container-image-promoter.yaml#L1>


### Postsubmits {#postsubmits}

<https://github.com/kubernetes/test-infra/blob/master/config/jobs/kubernetes/wg-k8s-infra/trusted/releng/releng-trusted.yaml#L3>


## Promotion Jobs {#promotion-jobs}

<https://prow.k8s.io/?job=post-k8sio-image-promo>
