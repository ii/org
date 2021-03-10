+++
title = "New Contributor Summit Session 01"
author = ["Zach Mandeville"]
date = 2021-02-05
lastmod = 2021-02-05T15:56:17+13:00
section = "post"
tags = ["kubernetes", "ncw", "testing"]
categories = ["guides"]
draft = true
weight = 2002
summary = "Intro to Testing for new K8s contributors"
[menu.main]
  weight = 2002
  identifier = "new-contributor-summit-session-01"
+++

## Introduction {#introduction}


## Agenda {#agenda}

In this session we will tackle

-   your hardware and OS requirements
-   installing all prerequisites
-   github and git configuration
-   forking and cloning kubernetes
-   the kubernetes git workflow


## Hardware and OS Requirements {#hardware-and-os-requirements}

Can run on linux, mac, and windows.


### Hardware Requirements {#hardware-requirements}

kubernetes is a large project, will require a lot of computing power

-   8GB of RAM
-   at least 50gb of free disk space
-   multiple core


#### If running kubernetes in docker {#if-running-kubernetes-in-docker}

If using Docker for Mac (or Windows), dedicate the Docker system multiple CPU cores and 6GB RAM


### Linux {#linux}

No additional considerations needed


### Mac {#mac}

<https://github.com/kubernetes/community/blob/master/contributors/devel/development.md#setting-up-macos>

-   will need to insstall <https://brew.sh>
-   Will need to install some command line tools

<!--listend-->

```shell
brew install coreutils ed findutils gawk gnu-sed gnu-tar grep make
```

-   set up some bashrc

<!--listend-->

```nil
GNUBINS="$(find /usr/local/opt -type d -follow -name gnubin -print)"

for bindir in ${GNUBINS[@]}
do
  export PATH=$bindir:$PATH
done

export PATH
```


### Windows {#windows}

additional steps, listed here
<https://github.com/kubernetes/community/blob/master/contributors/devel/development.md#setting-up-windows>

-   if using windows 10, then setup the linux subsystem
-   if on < windows 10, switch to a virtual machine running linux


## Software Prerequisites {#software-prerequisites}


### Docker {#docker}


#### What is docker {#what-is-docker}

Docker is a set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers.
Containers are isolated from one another and bundle their own software, libraries and configuration files; they can communicate with each other through well-defined channels.
All containers are run by a single operating system kernel and therefore use fewer resources than virtual machines.


#### Check if you have docker installed {#check-if-you-have-docker-installed}

The operating-system independent way to check whether Docker is running is to ask Docker, using the docker info command.
You can also use operating system utilities, such as

```nil
shell sudo systemctl is-active docker
```

or

```nil
sudo status docker
```

or

```nil
sudo service docker status
```

or checking the service status using Windows utilities.
Finally, you can check in the process list for the \`dockerd\` process, using commands like

```nil
 ps
```

or

```nil
 top
```


#### Installing docker {#installing-docker}

\*Docker Engine is available on a variety of Linux platforms, macOS and Windows 10 through Docker Desktop, and as a static binary installation.
Find your preferred operating system below.

<!--list-separator-->

-  MacOS

    Instruction for MacOS [install](https://docs.docker.com/docker-for-mac/install/)

<!--list-separator-->

-  Linux

    Instuctions for
    Debain [install](https://docs.docker.com/engine/install/debian/)
    Fedora [install](https://docs.docker.com/engine/install/fedora/)
    Ubuntu [install](https://docs.docker.com/engine/install/ubuntu/)

<!--list-separator-->

-  Windows

    Docker Desktop for Windows is the Community version of Docker for Microsoft Windows.
    You can download Docker Desktop for Windows from Docker Hub to [install](https://docs.docker.com/docker-for-windows/install/)


### Git {#git}


#### What is git {#what-is-git}

GitHub provides hosting for software development and version control using Git.
It offers the distributed version control and source code management (SCM) functionality of Git, plus its own features.
It provides access control and several collaboration features such as bug tracking, feature requests, task management and continuous integration.


#### Check if you have git installed {#check-if-you-have-git-installed}


#### Installing git {#installing-git}

In a terminal window run
\`git --version\`
If it is installed you will get a message like \`git version 2.25.1\`

<!--list-separator-->

-  Mac

    [Installing on macOS](https://github.com/git-guides/install-git#install-git-on-mac)

<!--list-separator-->

-  Linux

    [Installing on Linux](https://github.com/git-guides/install-git#install-git-on-linux)

<!--list-separator-->

-  Windows

    [Installing on Windows](https://github.com/git-guides/install-git#install-git-on-windows)


#### Configure git {#configure-git}

To use get you need a Github account.
If you do not have an account yet go to the [Github](https://github.com/) website to sign up.
You'll need:

-   name
-   email
-   password

preparing for working with the k8s repo.


### Go {#go}


#### What is go {#what-is-go}

Go or [Golang](https://golang.org/) as it is also known is an open source programming language that makes it easy to build simple, reliable, and efficient software.


#### Installing go {#installing-go}

We want to make check is Go is installed and what version.
Open Command Prompt / CMD ot Terminal window, execute the command to check the Go version. Make sure you have the latest version of Go.
$ go version

If you need to install Go the [official installation page](https://golang.org/doc/install) have struction for Linux, Mac and Windows


#### Adding go to your path {#adding-go-to-your-path}

and knowing how to find your $GOPATH -- We can look here: <https://golang.org/doc/gopath%5Fcode.html>


### SSH Keys {#ssh-keys}


#### what is ssh {#what-is-ssh}

SSH is a secure protocol used as the primary means of connecting to Linux servers remotely.
It provides a text-based interface by spawning a remote shell.
After connecting, all commands you type in your local terminal are sent to the remote server and executed there.
SSH keys are a matching set of cryptographic keys which can be used for authentication. Each set contains a public and a private key.
The public key can be shared freely without concern, while the private key must be vigilantly guarded and never exposed to anyone.


#### creating a new ssh key {#creating-a-new-ssh-key}

To generate an RSA key pair on your local computer, type:

-   ssh-keygen

This will create to files in the .ssh directory. Your private key id\_rsa. and public key id\_rsa.pub


## Github configuration {#github-configuration}


### Signing up for github account {#signing-up-for-github-account}


### Uploading your SSH Key {#uploading-your-ssh-key}


### Signing the CNCF CLA {#signing-the-cncf-cla}


## Forking and Cloning K8s {#forking-and-cloning-k8s}


### brief tour of k8s repo {#brief-tour-of-k8s-repo}


### forking to your own repo {#forking-to-your-own-repo}


### cloning k8s down to your own computer {#cloning-k8s-down-to-your-own-computer}


## The Kubernetes git workflow {#the-kubernetes-git-workflow}


### k8s/k8s is 'upstream' {#k8s-k8s-is-upstream}


### you create a branch on your fork, and push and make changes. {#you-create-a-branch-on-your-fork-and-push-and-make-changes-dot}


### then open a pr in upstream, comparing across forks. {#then-open-a-pr-in-upstream-comparing-across-forks-dot}


## Getting Additional Help {#getting-additional-help}

We won't be doing this live, but are there other resources we can offer for help?  perhaps a slack channel that we'd be moderating during NCW times?  A repo in which they can open issues for their questions?


## What's Next? {#what-s-next}

Outline of session 2.  You have all the requirements, now we will build and hack on kubernetes!
