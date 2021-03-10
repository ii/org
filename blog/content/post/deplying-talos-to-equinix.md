+++
title = "Deploying Talos to Equinix"
author = ["Caleb Woodbine", "Andrew Rynhard"]
date = 2021-02-03
lastmod = 2021-03-10T15:48:17+13:00
tags = ["kubernetes", "equinix", "talos", "org"]
categories = ["guides"]
draft = false
weight = 2001
summary = "From nodes to workloads on baremetal"
[menu.main]
  weight = 2001
  identifier = "deploying-talos-to-equinix"
+++

## Introduction {#introduction}

In this guide we will launch a highly-available three Node Kubernetes cluster on Equinix Metal using Talos as the Node OS, as well as bootstrap, and controlPlane provider for Cluster-API.

What is [Cluster-API](https://cluster-api.sigs.k8s.io/)?
:

> Cluster API is a Kubernetes sub-project focused on providing declarative APIs and tooling to simplify provisioning, upgrading, and operating multiple Kubernetes clusters.

What is [Talos](https://www.talos.dev/)?
:

> Talos is a modern OS designed to be secure, immutable, and minimal.

What is [Equinix Metal](https://metal.equinix.com/)?
:

> A globally-available bare metal “as-a-service” that can be deployed and interconnected in minutes.

The folks over at Equinix Metal have a wonderful heart for supporting Open Source communities.

Why is this important?
: In general: Orchestrating a container based OS such as Talos ([Flatcar](http://flatcar-linux.org/), [Fedora CoreOS](https://getfedora.org/coreos/), or [RancherOS](https://rancher.com/products/rancher/)) shifts focus from the Nodes to the workloads. In terms of Talos: Currently the documentation for running an OS such as Talos in Equinix Metal for Kubernetes with Cluster-API is not so well documented and therefore inaccessible. It's important to fill in the gaps of knowledge.


## Dependencies {#dependencies}

What you'll need for this guide:

-   [talosctl](https://github.com/talos-systems/talos/releases/tag/v0.8.1)

-   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

-   [packet-cli](https://github.com/packethost/packet-cli)

-   the ID and API token of existing Equinix Metal project

-   an existing Kubernetes cluster with a public IP (such as [kind](http://kind.sigs.k8s.io/), [minikube](https://minikube.sigs.k8s.io/), or a cluster already on Equinix Metal)


## Prelimiary steps {#prelimiary-steps}

In order to talk to Equinix Metal, we'll export environment variables to configure resources and talk via `packet-cli`.

Set the correct project to create and manage resources in:

```tmate
  read -p 'PACKET_PROJECT_ID: ' PACKET_PROJECT_ID
```

The API key for your account or project:

```tmate
  read -p 'PACKET_API_KEY: ' PACKET_API_KEY
```

Export the variables to be accessible from `packet-cli` and `clusterctl` later on:

```tmate
  export PACKET_PROJECT_ID PACKET_API_KEY PACKET_TOKEN=$PACKET_API_KEY
```

In the existing cluster, a public LoadBalancer IP will be needed. I have already installed nginx-ingress in this cluster, which has got a Service with the cluster's elastic IP.
We'll need this IP address later for use in booting the servers.
If you have set up your existing cluster differently, it'll just need to be an IP that we can use.

```tmate
  export LOAD_BALANCER_IP="$(kubectl -n nginx-ingress get svc nginx-ingress-ingress-nginx-controller -o=jsonpath='{.status.loadBalancer.ingress[0].ip}')"
```


## Setting up Cluster-API {#setting-up-cluster-api}

Install Talos providers for Cluster-API bootstrap and controlplane in your existing cluster:

```tmate
  clusterctl init -b talos -c talos -i packet
```

This will install Talos's bootstrap and controlPlane controllers as well as the Packet / Equinix Metal infrastructure provider.

****Important**** note:

-   the `bootstrap-talos` controller in the `cabpt-system` namespace must be running a version greater than `v0.2.0-alpha.8`. The version can be displayed in with `clusterctl upgrade plan` when it's installed.


## Setting up Matchbox {#setting-up-matchbox}

Currently, since Equinix Metal have ****not**** yet added support for Talos, it is necessary to install [Matchbox](https://matchbox.psdn.io/) to boot the servers (There is an [issue](https://github.com/packethost/packet-images/issues/26) in progress and [feedback](https://feedback.equinixmetal.com/operating-systems/p/talos-as-officially-supported-operating-system) for adding support).

What is Matchbox?
:

> Matchbox is a service that matches bare-metal machines to profiles that PXE boot and provision clusters.

Here is the manifest for a basic matchbox installation:

```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: matchbox
  spec:
    replicas: 1
    strategy:
      rollingUpdate:
        maxUnavailable: 1
    selector:
      matchLabels:
        name: matchbox
    template:
      metadata:
        labels:
          name: matchbox
      spec:
        containers:
          - name: matchbox
            image: quay.io/poseidon/matchbox:v0.9.0
            env:
              - name: MATCHBOX_ADDRESS
                value: "0.0.0.0:8080"
              - name: MATCHBOX_LOG_LEVEL
                value: "debug"
            ports:
              - name: http
                containerPort: 8080
            livenessProbe:
              initialDelaySeconds: 5
              httpGet:
                path: /
                port: 8080
            resources:
              requests:
                cpu: 30m
                memory: 20Mi
              limits:
                cpu: 50m
                memory: 50Mi
            volumeMounts:
              - name: data
                mountPath: /var/lib/matchbox
              - name: assets
                mountPath: /var/lib/matchbox/assets
        volumes:
          - name: data
            hostPath:
              path: /var/local/matchbox/data
          - name: assets
            hostPath:
              path: /var/local/matchbox/assets
  ---
  apiVersion: v1
  kind: Service
  metadata:
    name: matchbox
    annotations:
      metallb.universe.tf/allow-shared-ip: nginx-ingress
  spec:
    type: LoadBalancer
    selector:
      name: matchbox
    ports:
      - name: http
        protocol: TCP
        port: 8080
        targetPort: 8080
```

Save it as `matchbox.yaml`

The manifests above were inspired by the manifests in the [matchbox repo](https://github.com/poseidon/matchbox/tree/master/contrib/k8s).
For production it might be wise to use:

-   an Ingress with full TLS
-   a ReadWriteMany storage provider instead hostPath for scaling

With the manifests ready to go, we'll install Matchbox into the `matchbox` namespace on the existing cluster with the following commands:

```tmate
  kubectl create ns matchbox
  kubectl -n matchbox apply -f ./matchbox.yaml
```

You may need to patch the `Service.spec.externalIPs` to have an IP to access it from if one is not populated:

```tmate
  kubectl -n matchbox patch \
    service matchbox \
    -p "{\"spec\":{\"externalIPs\":[\"$LOAD_BALANCER_IP\"]}}"
```

Once the pod is live, We'll need to create a directory structure for storing Talos boot assets:

```tmate
  kubectl -n matchbox exec -it \
    deployment/matchbox -- \
    mkdir -p /var/lib/matchbox/{profiles,groups} /var/lib/matchbox/assets/talos
```

Inside the Matchbox container, we'll download the Talos boot assets for Talos version 0.8.1 into the assets folder:

```tmate
  kubectl -n matchbox exec -it \
    deployment/matchbox -- \
    wget -P /var/lib/matchbox/assets/talos \
    https://github.com/talos-systems/talos/releases/download/v0.8.1/initramfs-amd64.xz \
    https://github.com/talos-systems/talos/releases/download/v0.8.1/vmlinuz-amd64
```

Now that the assets have been downloaded, run a checksum against them to verify:

```tmate
  kubectl -n matchbox exec -it \
    deployment/matchbox -- \
    sh -c "cd /var/lib/matchbox/assets/talos && \
      wget -O- https://github.com/talos-systems/talos/releases/download/v0.8.1/sha512sum.txt 2> /dev/null \
      | sed 's,_out/,,g' \
      | grep 'initramfs-amd64.xz\|vmlinuz-amd64' \
      | sha512sum -c -"
```

Since there's only one Pod in the Matchbox deployment, we'll export it's name to copy files into it:

```tmate
  export MATCHBOX_POD_NAME=$(kubectl -n matchbox get pods -l name=matchbox -o=jsonpath='{.items[0].metadata.name}')
```

[Profiles in Matchbox](https://matchbox.psdn.io/matchbox/#profiles) are JSON configurations for how the servers should boot, where from, and their kernel args. Save this file as `profile-default-amd64.json`

```json
  {
    "id": "default-amd64",
    "name": "default-amd64",
    "boot": {
      "kernel": "/assets/talos/vmlinuz-amd64",
      "initrd": [
        "/assets/talos/initramfs-amd64.xz"
      ],
      "args": [
        "initrd=initramfs-amd64.xz",
        "init_on_alloc=1",
        "init_on_free=1",
        "slub_debug=P",
        "pti=on",
        "random.trust_cpu=on",
        "console=tty0",
        "console=ttyS1,115200n8",
        "slab_nomerge",
        "printk.devkmsg=on",
        "talos.platform=packet",
        "talos.config=none"
      ]
    }
  }
```

[Groups in Matchbox](https://matchbox.psdn.io/matchbox/#groups) are a way of letting servers pick up profiles based on selectors. Save this file as `group-default-amd64.json`

```json
  {
    "id": "default-amd64",
    "name": "default-amd64",
    "profile": "default-amd64",
    "selector": {
      "arch": "amd64"
    }
  }
```

We'll copy the profile and group into their respective folders:

```tmate
  kubectl -n matchbox \
    cp ./profile-default-amd64.json \
    $MATCHBOX_POD_NAME:/var/lib/matchbox/profiles/default-amd64.json
  kubectl -n matchbox \
    cp ./group-default-amd64.json \
    $MATCHBOX_POD_NAME:/var/lib/matchbox/groups/default-amd64.json
```

List the files to validate that they were written correctly:

```tmate
  kubectl -n matchbox exec -it \
    deployment/matchbox -- \
    sh -c 'ls -alh /var/lib/matchbox/*/'
```


### Testing Matchbox {#testing-matchbox}

Using `curl`, we can verify Matchbox's running state:

```tmate
  curl http://$LOAD_BALANCER_IP:8080
```

To test matchbox, we'll create an invalid userdata configuration for Talos, saving as `userdata.txt`:

```text
#!talos
```

Feel free to use a valid one.

Now let's talk to Equinix Metal to create a server pointing to the Matchbox server:

```tmate
   packet-cli device create \
    --hostname talos-pxe-boot-test-1 \
    --plan c1.small.x86 \
    --facility sjc1 \
    --operating-system custom_ipxe \
    --project-id "$PACKET_PROJECT_ID" \
    --ipxe-script-url "http://$LOAD_BALANCER_IP:8080/ipxe?arch=amd64" \
    --userdata-file=./userdata.txt
```

In the meanwhile, we can watch the logs to see how things are:

```tmate
  kubectl -n matchbox logs deployment/matchbox -f --tail=100
```

Looking at the logs, there should be some get requests of resources that will be used to boot the OS.

Notes:

-   fun fact: you can run Matchbox on Android using [Termux](https://f-droid.org/en/packages/com.termux/).


## The cluster {#the-cluster}


### Preparing the cluster {#preparing-the-cluster}

Here we will declare the template that we will shortly generate our usable cluster from:

```yaml
  kind: TalosControlPlane
  apiVersion: controlplane.cluster.x-k8s.io/v1alpha3
  metadata:
    name: "${CLUSTER_NAME}-control-plane"
  spec:
    version: ${KUBERNETES_VERSION}
    replicas: ${CONTROL_PLANE_MACHINE_COUNT}
    infrastructureTemplate:
      apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
      kind: PacketMachineTemplate
      name: "${CLUSTER_NAME}-control-plane"
    controlPlaneConfig:
      init:
        generateType: init
        configPatches:
          - op: replace
            path: /machine/install
            value:
              disk: /dev/sda
              image: ghcr.io/talos-systems/installer:v0.8.1
              bootloader: true
              wipe: false
              force: false
          - op: add
            path: /machine/kubelet/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/apiServer/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/controllerManager/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/extraManifests
            value:
            - https://github.com/packethost/packet-ccm/releases/download/v1.1.0/deployment.yaml
          - op: add
            path: /cluster/allowSchedulingOnMasters
            value: true
      controlplane:
        generateType: controlplane
        configPatches:
          - op: replace
            path: /machine/install
            value:
              disk: /dev/sda
              image: ghcr.io/talos-systems/installer:v0.8.1
              bootloader: true
              wipe: false
              force: false
          - op: add
            path: /machine/kubelet/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/apiServer/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/controllerManager/extraArgs
            value:
              cloud-provider: external
          - op: add
            path: /cluster/allowSchedulingOnMasters
            value: true
  ---
  apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
  kind: PacketMachineTemplate
  metadata:
    name: "${CLUSTER_NAME}-control-plane"
  spec:
    template:
      spec:
        OS: custom_ipxe
        ipxeURL: "http://${IPXE_SERVER_IP}:8080/ipxe?arch=amd64"
        billingCycle: hourly
        machineType: "${CONTROLPLANE_NODE_TYPE}"
        sshKeys:
          - "${SSH_KEY}"
        tags: []
  ---
  apiVersion: cluster.x-k8s.io/v1alpha3
  kind: Cluster
  metadata:
    name: "${CLUSTER_NAME}"
  spec:
    clusterNetwork:
      pods:
        cidrBlocks:
          - ${POD_CIDR:=192.168.0.0/16}
      services:
        cidrBlocks:
          - ${SERVICE_CIDR:=172.26.0.0/16}
    infrastructureRef:
      apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
      kind: PacketCluster
      name: "${CLUSTER_NAME}"
    controlPlaneRef:
      apiVersion: controlplane.cluster.x-k8s.io/v1alpha3
      kind: TalosControlPlane
      name: "${CLUSTER_NAME}-control-plane"
  ---
  apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
  kind: PacketCluster
  metadata:
    name: "${CLUSTER_NAME}"
  spec:
    projectID: "${PACKET_PROJECT_ID}"
    facility: "${FACILITY}"
  ---
  apiVersion: cluster.x-k8s.io/v1alpha3
  kind: MachineDeployment
  metadata:
    name: ${CLUSTER_NAME}-worker-a
    labels:
      cluster.x-k8s.io/cluster-name: ${CLUSTER_NAME}
      pool: worker-a
  spec:
    replicas: ${WORKER_MACHINE_COUNT}
    clusterName: ${CLUSTER_NAME}
    selector:
      matchLabels:
        cluster.x-k8s.io/cluster-name: ${CLUSTER_NAME}
        pool: worker-a
    template:
      metadata:
        labels:
          cluster.x-k8s.io/cluster-name: ${CLUSTER_NAME}
          pool: worker-a
      spec:
        version: ${KUBERNETES_VERSION}
        clusterName: ${CLUSTER_NAME}
        bootstrap:
          configRef:
            name: ${CLUSTER_NAME}-worker-a
            apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
            kind: TalosConfigTemplate
        infrastructureRef:
          name: ${CLUSTER_NAME}-worker-a
          apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
          kind: PacketMachineTemplate
  ---
  apiVersion: infrastructure.cluster.x-k8s.io/v1alpha3
  kind: PacketMachineTemplate
  metadata:
    name: ${CLUSTER_NAME}-worker-a
  spec:
    template:
      spec:
        OS: custom_ipxe
        ipxeURL: "http://${IPXE_SERVER_IP}:8080/ipxe?arch=amd64"
        billingCycle: hourly
        machineType: "${WORKER_NODE_TYPE}"
        sshKeys:
          - "${SSH_KEY}"
        tags: []
  ---
  apiVersion: bootstrap.cluster.x-k8s.io/v1alpha3
  kind: TalosConfigTemplate
  metadata:
    name: ${CLUSTER_NAME}-worker-a
    labels:
      cluster.x-k8s.io/cluster-name: ${CLUSTER_NAME}
  spec:
    template:
      spec:
        generateType: init
```

Inside of `TalosControlPlane.spec.controlPlaneConfig.init`, I'm very much liking the use of `generateType: init` paired with `configPatches`. This enables:

-   configuration to be generated;
-   management of certificates out of the cluster operator's hands;
-   another level of standardisation; and
-   overrides to be added where needed

Notes:

-   the ClusterAPI template above uses Packet-Cloud-Controller manager version 1.1.0


#### Templating your configuration {#templating-your-configuration}

Set environment variables for configuration:

<a id="code-snippet--cluster-config-env"></a>
```bash
    export CLUSTER_NAME="talos-metal"
  export FACILITY=sjc1
  export KUBERNETES_VERSION=v1.20.2
  export POD_CIDR=10.244.0.0/16
  export SERVICE_CIDR=10.96.0.0/12
  export CONTROLPLANE_NODE_TYPE=c1.small.x86
  export CONTROL_PLANE_MACHINE_COUNT=3
  export WORKER_NODE_TYPE=c1.small.x86
  export WORKER_MACHINE_COUNT=0
  export SSH_KEY=""
  export IPXE_URL=$LOAD_BALANCER_IP
```

In the variables above, we will create a cluster which has three small controlPlane nodes to run workloads.


#### Render the manifests {#render-the-manifests}

Render your cluster configuration from the template:

```tmate
  clusterctl config cluster "$CLUSTER_NAME" \
    --from ./talos-packet-cluster-template.yaml \
    -n "$CLUSTER_NAME" > "$CLUSTER_NAME"-cluster-capi.yaml
```


### Creating the cluster {#creating-the-cluster}

With the template for the cluster rendered to how wish to deploy it, it's now time to apply it:

```tmate
  kubectl create ns "$CLUSTER_NAME"
  kubectl -n "$CLUSTER_NAME" apply -f ./"$CLUSTER_NAME"-cluster-capi.yaml
```

The cluster will now be brought up, we can see the progress by taking a look at the resources:

```tmate
  kubectl -n "$CLUSTER_NAME" get machines,clusters,packetmachines,packetclusters
```

Note: As expected, the cluster may take some time to appear and be accessible.

Not long after applying, a KubeConfig is available. Fetch the KubeConfig from the existing cluster with:

```tmate
  kubectl -n "$CLUSTER_NAME" get secrets \
    "$CLUSTER_NAME"-kubeconfig -o=jsonpath='{.data.value}' \
    | base64 -d > $HOME/.kube/"$CLUSTER_NAME"
```

Using the KubeConfig from the new cluster, check out the status of it:

```tmate
  kubectl --kubeconfig $HOME/.kube/"$CLUSTER_NAME" cluster-info
```

Once the APIServer is reachable, create configuration for how the Packet-Cloud-Controller-Manager should talk to Equinix-Metal:

```tmate
  kubectl --kubeconfig $HOME/.kube/"$CLUSTER_NAME" -n kube-system \
    create secret generic packet-cloud-config \
    --from-literal=cloud-sa.json="{\"apiKey\": \"${PACKET_API_KEY}\",\"projectID\": \"${PACKET_PROJECT_ID}\"}"
```

Since we're able to talk to the APIServer, we can check how all Pods are doing:

<a id="code-snippet--list all Pods"></a>
```bash
    export CLUSTER_NAME="talos-metal"
  kubectl --kubeconfig $HOME/.kube/"$CLUSTER_NAME"\
    -n kube-system get pods
```

Listing Pods shows that everything is live and in a good state:

```bash
NAMESPACE     NAME                                                     READY   STATUS    RESTARTS   AGE
kube-system   coredns-5b55f9f688-fb2cb                                 1/1     Running   0          25m
kube-system   coredns-5b55f9f688-qsvg5                                 1/1     Running   0          25m
kube-system   kube-apiserver-665px                                     1/1     Running   0          19m
kube-system   kube-apiserver-mz68q                                     1/1     Running   0          19m
kube-system   kube-apiserver-qfklt                                     1/1     Running   2          19m
kube-system   kube-controller-manager-6grxd                            1/1     Running   0          19m
kube-system   kube-controller-manager-cf76h                            1/1     Running   0          19m
kube-system   kube-controller-manager-dsmgf                            1/1     Running   0          19m
kube-system   kube-flannel-brdxw                                       1/1     Running   0          24m
kube-system   kube-flannel-dm85d                                       1/1     Running   0          24m
kube-system   kube-flannel-sg6k9                                       1/1     Running   0          24m
kube-system   kube-proxy-flx59                                         1/1     Running   0          24m
kube-system   kube-proxy-gbn4l                                         1/1     Running   0          24m
kube-system   kube-proxy-ns84v                                         1/1     Running   0          24m
kube-system   kube-scheduler-4qhjw                                     1/1     Running   0          19m
kube-system   kube-scheduler-kbm5z                                     1/1     Running   0          19m
kube-system   kube-scheduler-klsmp                                     1/1     Running   0          19m
kube-system   packet-cloud-controller-manager-77cd8c9c7c-cdzfv         1/1     Running   0          20m
kube-system   pod-checkpointer-4szh6                                   1/1     Running   0          19m
kube-system   pod-checkpointer-4szh6-talos-metal-control-plane-j29lb   1/1     Running   0          19m
kube-system   pod-checkpointer-k7w8h                                   1/1     Running   0          19m
kube-system   pod-checkpointer-k7w8h-talos-metal-control-plane-lk9f2   1/1     Running   0          19m
kube-system   pod-checkpointer-m5wrh                                   1/1     Running   0          19m
kube-system   pod-checkpointer-m5wrh-talos-metal-control-plane-h9v4j   1/1     Running   0          19m
```

With the cluster live, it's now ready for workloads to be deployed!


## Talos Configuration {#talos-configuration}

In order to manage Talos Nodes outside of Kubernetes, we need to create and set up configuration to use.

Create the directory for the config:

```tmate
  mkdir -p $HOME/.talos
```

Discover the IP for the first controlPlane:

```tmate
  export TALOS_ENDPOINT=$(kubectl -n "$CLUSTER_NAME" \
    get machines \
    $(kubectl -n "$CLUSTER_NAME" \
      get machines -l cluster.x-k8s.io/control-plane='' \
      --no-headers --output=jsonpath='{.items[0].metadata.name}') \
      -o=jsonpath="{.status.addresses[?(@.type=='ExternalIP')].address}" | awk '{print $2}')
```

Fetch the `talosconfig` from the existing cluster:

```tmate
  kubectl get talosconfig \
    -n $CLUSTER_NAME \
    -l cluster.x-k8s.io/cluster-name=$CLUSTER_NAME \
    -o yaml -o jsonpath='{.items[0].status.talosConfig}' > $HOME/.talos/"$CLUSTER_NAME"-management-plane-talosconfig.yaml
```

Write in the configuration the endpoint IP and node IP:

```tmate
  talosctl \
    --talosconfig $HOME/.talos/"$CLUSTER_NAME"-management-plane-talosconfig.yaml \
    config endpoint $TALOS_ENDPOINT
  talosctl \
    --talosconfig $HOME/.talos/"$CLUSTER_NAME"-management-plane-talosconfig.yaml \
    config node $TALOS_ENDPOINT
```

Now that the `talosconfig` has been written, try listing all containers:

<a id="code-snippet--list-containers-on-containerd"></a>
```bash
    export CLUSTER_NAME="talos-metal"
  # removing ip; omit ` | sed ...` for regular use
  talosctl --talosconfig $HOME/.talos/"$CLUSTER_NAME"-management-plane-talosconfig.yaml containers | sed -r 's/(\b[0-9]{1,3}\.){3}[0-9]{1,3}\b'/"x.x.x.x      "/
```

Here's the containers running on this particular node, in containerd (not k8s related):

```bash
NODE            NAMESPACE   ID         IMAGE                                  PID    STATUS
x.x.x.x         system      apid       talos/apid                             3046   RUNNING
x.x.x.x         system      etcd       gcr.io/etcd-development/etcd:v3.4.14   3130   RUNNING
x.x.x.x         system      networkd   talos/networkd                         2879   RUNNING
x.x.x.x         system      routerd    talos/routerd                          2888   RUNNING
x.x.x.x         system      timed      talos/timed                            2976   RUNNING
x.x.x.x         system      trustd     talos/trustd                           3047   RUNNING
```


## Clean up {#clean-up}

Tearing down the entire cluster and resources associated with it, can be achieved by

1.  Deleting the cluster:

<!--listend-->

```tmate
  kubectl -n "$CLUSTER_NAME" delete cluster "$CLUSTER_NAME"
```

ii. Deleting the namespace:

```tmate
  kubectl delete ns "$CLUSTER_NAME"
```

iii. Removing local configurations:

```tmate
  rm \
    $HOME/.talos/"$CLUSTER_NAME"-management-plane-talosconfig.yaml \
    $HOME/.kube/"$CLUSTER_NAME"
```


## What have I learned from this? {#what-have-i-learned-from-this}

(always learning) how wonderful the Kubernetes community is
: there are so many knowledgable individuals who are so ready for collaboration and adoption - it doesn't matter the SIG or group.

how modular Cluster-API is
: Cluster-API components (bootstrap, controlPlane, core, infrastructure) can be swapped out and meshed together in very cool ways.


## Credits {#credits}

Integrating Talos into this project would not be possible without help from [Andrew Rynhard (Talos Systems)](https://github.com/andrewrynhard), huge thanks to him for reaching out for pairing and co-authoring.


## Notes and references {#notes-and-references}

-   with the new cluster's controlPlane live and available for deployment, the iPXE server could be moved into that cluster - meaning that new servers boot from the cluster that they'll join, making it almost self-contained
-   cluster configuration as based off of [cluster-template.yaml from the cluster-api-provider-packet repo](https://github.com/kubernetes-sigs/cluster-api-provider-packet/blob/479faf06e1337b1e979cb624ca8be015b2a89cde/templates/cluster-template.yaml)
-   this post has been made to [blog.calebwoodine.com](https://blog.calebwoodbine.com/deploying-talos-and-kubernetes-with-cluster-api-on-equinix-metal), and [talos-system.com/blog](https://ii.coop/deploying-talos-and-kubernetes-with-cluster-api-on-equinix-metal/), but is also available as an [Org file](https://github.com/ii/org/blob/master/ii/equinix-metal-capi-talos-kubernetes/README.org)

---

Hope you've enjoyed the output of this project!
Thank you!
