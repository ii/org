+++
title = "Creating an e2e test for Conformance"
author = ["Stephen Heywood"]
date = 2021-05-11
lastmod = 2021-05-13T09:02:00+13:00
categories = ["kubernetes"]
draft = false
summary = "Finding untested stable endpoints and creating an e2e test for conformance."
+++

## Introduction

Since the 1.19 release of Kubernetes, the gap in e2e conformance tested endpoints has decreased due in part to the processes and tooling that the team at [ii.coop](https://ii.coop/) have developed.

![img](/images/2021/apisnoop-progress.png)

The process starts by using [APIsnoop](https://github.com/cncf/apisnoop) (which uses a postgres database containing audit logs from e2e test runs) to identify a set of untested endpoints that are part of the stable API endpoints. During this process various groups or patterns of endpoints are discovered. One such group of endpoints are &ldquo;DaemonSetStatus&rdquo;. Next we will explore these endpoints, create an e2e test that exercises each of them, then merge this test into the k8s repo.

APIsnoop results for untested &ldquo;DaemonSetStatus&rdquo; endpoints in [untested_stable_endpoints table](https://github.com/cncf/apisnoop/blob/main/apps/snoopdb/tables-views-functions.org#untested_stable_endpoints)

```sql
  select
    endpoint,
    path,
    kind
  from testing.untested_stable_endpoint
  where eligible is true
  and endpoint ilike '%DaemonSetStatus'
  order by kind, endpoint desc;
```


```
                endpoint                  |                           path                                |    kind
------------------------------------------+---------------------------------------------------------------+------------
   replaceAppsV1NamespacedDaemonSetStatus | /apis/apps/v1/namespaces/{namespace}/daemonsets/{name}/status | DaemonSet
   readAppsV1NamespacedDaemonSetStatus    | /apis/apps/v1/namespaces/{namespace}/daemonsets/{name}/status | DaemonSet
   patchAppsV1NamespacedDaemonSetStatus   | /apis/apps/v1/namespaces/{namespace}/daemonsets/{name}/status | DaemonSet
  (3 rows)
```


# Connecting an endpoint to a resource

Here are three possible ways use to connect an API endpoint to a resource in a cluster

1.  Some initial details about the endpoint can be found via the [API Reference](https://kubernetes.io/docs/reference/kubernetes-api/). For this example about Daemonset we can locate [read](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#get-read-status-of-the-specified-daemonset), [patch](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#patch-partially-update-status-of-the-specified-daemonset) and [replace](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/daemon-set-v1/#update-replace-status-of-the-specified-daemonset) for Daemonset Status.

2.  `kubectl` has an option to describe the fields associated with each supported API resource. The following example shows how it can provide details around &rsquo;status conditions&rsquo;.
    
    ```
       $ kubectl explain daemonset.status.conditions
       KIND:     DaemonSet
       VERSION:  apps/v1
    
       RESOURCE: conditions <[]Object>
    
       DESCRIPTION:
            Represents the latest available observations of a DaemonSet's current
            state.
    
            DaemonSetCondition describes the state of a DaemonSet at a certain point.
    
       FIELDS:
          lastTransitionTime   <string>
            Last time the condition transitioned from one status to another.
    
          message      <string>
            A human readable message indicating details about the transition.
    
          reason       <string>
            The reason for the condition's last transition.
    
          status       <string> -required-
            Status of the condition, one of True, False, Unknown.
    
          type <string> -required-
            Type of DaemonSet condition.
    ```

3.  Lastly, using both [APIsnoop in cluster](https://github.com/cncf/apisnoop/tree/main/kind) while reviewing the current [e2e test suite](https://github.com/kubernetes/kubernetes/tree/master/test/e2e) for existing conformance tests that test a similar set of endpoints. In this case we used [a Service Status test](https://github.com/kubernetes/kubernetes/blob/7b2776b89fb1be28d4e9203bdeec079be903c103/test/e2e/network/service.go#L2300-L2392) as a template for the new Daemonset test.

    ```sql
    with latest_release as (
    select release::semver as release
    from open_api
    order by release::semver desc
    limit 1
    )

    select ec.endpoint, ec.path, ec.kind
    from endpoint_coverage  ec
    join latest_release on(ec.release::semver = latest_release.release)
    where level = 'stable'
    and ec.endpoint ilike '%NamespacedServiceStatus'
    and tested is true
    ORDER BY endpoint desc;
    ```


    ```
                      endpoint               |                         path                          |  kind
       --------------------------------------+-------------------------------------------------------+---------
        replaceCoreV1NamespacedServiceStatus | /api/v1/namespaces/{namespace}/services/{name}/status | Service
        readCoreV1NamespacedServiceStatus    | /api/v1/namespaces/{namespace}/services/{name}/status | Service
        patchCoreV1NamespacedServiceStatus   | /api/v1/namespaces/{namespace}/services/{name}/status | Service
       (3 rows)
    ```
    
    The Service status e2e test followed similar ideas and patterns from [/test/e2e/auth/certificates.go](https://github.com/kubernetes/kubernetes/blob/31030820be979ea0b2c39e08eb18fddd71f353ed/test/e2e/auth/certificates.go#L356-L383) and [/test/e2e/network/ingress.go](https://github.com/kubernetes/kubernetes/blob/31030820be979ea0b2c39e08eb18fddd71f353ed/test/e2e/network/ingress.go#L1091-L1127)

# Writing an e2e test

## Initial Exploration

Using [literate programming](https://wiki.c2.com/?LiterateProgramming) we created [Appsv1DaemonSetStatusLifecycleTest.org](https://github.com/apisnoop/ticket-writing/blob/create-daemonset-status-lifecycle-test/Appsv1DaemonSetStatusLifecycleTest.org)
(via [pair](https://github.com/sharingio/pair)) to both test and document the explorations of the endpoints. This provides a clear outline that should be easily replicated and validated by others as needed.
Once completed, the document is converted into markdown which becomes a GitHub [issue](https://github.com/kubernetes/kubernetes/issues/100437).

The issue provides the following before a PR is opened:
- a starting point to discuss the endpoints
- the approach taken to test them
- whether they are [eligible for conformance](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/conformance-tests.md#conformance-test-requirements).

## Creating the e2e test

Utilizing the above document, the test is structured in to four parts;

1.  Creating the resources for the test, in this case a DaemonSet and a &rsquo;watch&rsquo;.

2.  Testing the first endpoint, `readAppsV1NamespacedReplicaSetStatus` via a [dynamic client](https://github.com/ii/kubernetes/blob/ca3aa6f5af1b545b116b52c717b866e43c79079b/test/e2e/apps/daemon_set.go#L841). This is due to the standard go client not being able to access the sub-resource. We also make sure there are no errors from either getting or decoding the response.

3.  The next endpoint tested is `replaceAppsV1NamespacedDaemonSetStatus` which replaces all status conditions at the same time. As the resource version of the DaemonSet may change before the new status conditions are updated we may need to [retry the request if there is a conflict](https://github.com/ii/kubernetes/blob/ca3aa6f5af1b545b116b52c717b866e43c79079b/test/e2e/apps/daemon_set.go#L854). Monitoring the watch events for the Daemonset we can confirm that the status conditions have been [replaced](https://github.com/ii/kubernetes/blob/ca3aa6f5af1b545b116b52c717b866e43c79079b/test/e2e/apps/daemon_set.go#L884-L886).

4.  The last endpoint tested is `patchAppsV1NamespacedReplicaSetStatus` which only patches a [single condition](https://github.com/ii/kubernetes/blob/ca3aa6f5af1b545b116b52c717b866e43c79079b/test/e2e/apps/daemon_set.go#L906) this time. Again, using the watch to monitor for events we can check that the single condition [has been updated](https://github.com/ii/kubernetes/blob/ca3aa6f5af1b545b116b52c717b866e43c79079b/test/e2e/apps/daemon_set.go#L931).

## Validating the e2e test

Using `go test` we can run a single test for quick feedback

```bash
cd ~/go/src/k8s.io/kubernetes
TEST_NAME="should verify changes to a daemon set status"
go test ./test/e2e/ -v -timeout=0  --report-dir=/tmp/ARTIFACTS -ginkgo.focus="$TEST_NAME"
```

Checking the e2e test logs we see that everything looks to be okay.

```
[It] should verify changes to a daemon set status  /home/ii/go/src/k8s.io/kubernetes/test/e2e/apps/daemon_set.go:812
STEP: Creating simple DaemonSet "daemon-set"
STEP: Check that daemon pods launch on every node of the cluster.
May 10 17:36:36.106: INFO: Number of nodes with available pods: 0
May 10 17:36:36.106: INFO: Node heyste-control-plane-fkjmr is running more than one daemon pod
May 10 17:36:37.123: INFO: Number of nodes with available pods: 0
May 10 17:36:37.123: INFO: Node heyste-control-plane-fkjmr is running more than one daemon pod
May 10 17:36:38.129: INFO: Number of nodes with available pods: 0
May 10 17:36:38.129: INFO: Node heyste-control-plane-fkjmr is running more than one daemon pod
May 10 17:36:39.122: INFO: Number of nodes with available pods: 1
May 10 17:36:39.122: INFO: Number of running nodes: 1, number of available pods: 1
STEP: Getting /status
May 10 17:36:39.142: INFO: Daemon Set daemon-set has Conditions: []
STEP: updating the DaemonSet Status
May 10 17:36:39.160: INFO: updatedStatus.Conditions: []v1.DaemonSetCondition{v1.DaemonSetCondition{Type:"StatusUpdate", Status:"True", LastTransitionTime:v1.Time{Time:time.Ti
me{wall:0x0, ext:0, loc:(*time.Location)(nil)}}, Reason:"E2E", Message:"Set from e2e test"}}
STEP: watching for the daemon set status to be updated
May 10 17:36:39.163: INFO: Observed event: ADDED
May 10 17:36:39.163: INFO: Observed event: MODIFIED
May 10 17:36:39.163: INFO: Observed event: MODIFIED
May 10 17:36:39.164: INFO: Observed event: MODIFIED
May 10 17:36:39.164: INFO: Found daemon set daemon-set in namespace daemonsets-2986 with labels: map[daemonset-name:daemon-set] annotations: map[deprecated.daemonset.template
.generation:1] & Conditions: [{StatusUpdate True 0001-01-01 00:00:00 +0000 UTC E2E Set from e2e test}]
May 10 17:36:39.164: INFO: Daemon set daemon-set has an updated status
STEP: patching the DaemonSet Status
STEP: watching for the daemon set status to be patched
May 10 17:36:39.180: INFO: Observed event: ADDED
May 10 17:36:39.180: INFO: Observed event: MODIFIED
May 10 17:36:39.181: INFO: Observed event: MODIFIED
May 10 17:36:39.181: INFO: Observed event: MODIFIED
May 10 17:36:39.181: INFO: Observed daemon set daemon-set in namespace daemonsets-2986 with annotations: map[deprecated.daemonset.template.generation:1] & Conditions: [{StatusUpdate True 0001-01-01 00:00:00 +0000 UTC E2E Set from e2e test}]
May 10 17:36:39.181: INFO: Found daemon set daemon-set in namespace daemonsets-2986 with labels: map[daemonset-name:daemon-set] annotations: map[deprecated.daemonset.template.generation:1] & Conditions: [{StatusPatched True 0001-01-01 00:00:00 +0000 UTC  }]
May 10 17:36:39.181: INFO: Daemon set daemon-set has a patched status
```

Verification that the test passed!

```
Ran 1 of 5745 Specs in 18.473 seconds
SUCCESS! -- 1 Passed | 0 Failed | 0 Pending | 5744 Skipped
--- PASS: TestE2E (18.62s)
```

Using APISnoop with the audit logger we can also confirm that the endpoints where hit during the test.

```sql
select distinct  endpoint, right(useragent,75) AS useragent
from testing.audit_event
where endpoint ilike '%DaemonSetStatus%'
and release_date::BIGINT > round(((EXTRACT(EPOCH FROM NOW()))::numeric)*1000,0) - 60000
and useragent like 'e2e%'
order by endpoint;
```

```
                endpoint                 |                             useragent
-----------------------------------------+-------------------------------------------------------------------
 patchAppsV1NamespacedReplicaSetStatus   | [sig-apps] ReplicaSet should validate Replicaset Status endpoints
 readAppsV1NamespacedReplicaSetStatus    | [sig-apps] ReplicaSet should validate Replicaset Status endpoints
 replaceAppsV1NamespacedReplicaSetStatus | [sig-apps] ReplicaSet should validate Replicaset Status endpoints
(3 rows)
```

Even though the test has passed here, once merged it will join other jobs on [TestGrid](https://testgrid.k8s.io/) to determine if the test is stable and after two weeks it can be [promoted to conformance](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/conformance-tests.md#promoting-tests-to-conformance).


# Final Thoughts

The current workflow and tooling provides a high level of confidence when working through each e2e test. Following agreed coding patterns, styles and processes helps to minimise possible issues and test flakes. There&rsquo;s always opportunities to get support through GitHub tickets, [various Kubernetes slack channels](https://kubernetes.slack.com/messages/k8s-conformance) and conformance meetings.

Every e2e test that&rsquo;s merged and then promoted to conformance requires the input from a wide range of people. It is thanks to the support from community reviewers, SIGs and the direction provided by SIG-Architecture this work is not just possible but rewarding.
