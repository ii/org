+++
title = "Learning Update: Introduction to gRPC"
author = ["Zach Mandeville"]
date = 2021-03-09
lastmod = 2021-03-10T15:19:29+13:00
categories = ["learning"]
draft = false
weight = 2001
summary = "An update on an ii member's journey on learning gRPC"
[menu.main]
  weight = 2001
  identifier = "learning-update-introduction-to-grpc"
+++

## Prelude {#prelude}

As I continue my career in code, I've come to find the most important part of my
practice is also the least visible: how I learn. There are beautiful moments
when I know exactly how to do something and just need to implement it so I'll
pour myself a cup of coffee, put [Firestarter](https://www.youtube.com/watch?v=wmin5WkOuPw) on repeat, and watch my beautiful code
unfurl down the screen as fast as I can type it. These moments, though, are not
typical.

Most of the time, I am discovering a new problem I do not yet know how to solve,
within a domain or technology I have not yet experienced, and to solve the
problem i have to first understand it. Here my coding life is a bit quieter and
boring to watch: I'll pour myself a cup of tea, put Firestarter(lo-fi ambient
remix) on repeat, and start poring through reference docs and tutorials and
writing "TODO: FIGURE OUT WHAT {X} MEANS" in my expanding network of notes.

This work is crucial for code, but often unseen, happening silently in the space
between git commits. And so, to celebrate this work and make it more visible,
we'll be posting periodic learning updates on this blog. These are written as
honest checkpoints taken mid-understanding, so while they are hopefully
illuminating, they should not be read as any sort of authoratative guide.

Sweet as, let's set a checkpoint! Right now, I'm learning all about gRPC and
protocol buffers and am quite excited about everything I've found.


## gRPC: what's it mean? {#grpc-what-s-it-mean}

gRPC stands for (google)Remote Procedure Call. It is an evolution of Remote
Procedure Calls, which is one of the primary models of api design (the other
being REST). So RPC involves specifying how clients and servers should
communicate with one another, but using a completely different paradigm than
REST. One of the most immediate distinctions, for me, is with REST you have
paths on the server that you make requests to, whereas with RPC it's more like
methods of a server interface that you can call. This is the "remote procedure"
aspect of the design, where on the client's side, the communication feels like
running functions directly on the server.

The way gRPC operates, sort of the material of the design, is with protocol
buffers. And so to learn gRPC you want to have a good understanding of protocol
buffers (or protobuf) first.


## Protocol Buffers: What do they mean? {#protocol-buffers-what-do-they-mean}

Protocol Buffers are another creation of Google, and are a way to define and
serialize data. They tackle the same problem as XML or JSON, but in a much
different way.

Protocol buffers work by defining a fully typed contract for your API in a
.proto file, which is then used to generate source code and compile your data
into streamable bytes. So the data being passed along is binary instead of
text-based, but the specification of this data is extremely readable, and
can easily generate introspective tools and documentation.

Proto buffers also feel distinct in that they were designed with modern
technology and modern paradigms. So they work with HTTP/2 and work extremely
well for micro-services architectures utilizing streams of data. This HTTP/2
requirement also means, though, that they cannot be consumed direclty by a web
browser.


## Well-Known Advantages of gRPC and protobuf {#well-known-advantages-of-grpc-and-protobuf}

Many of the advantages of gRPC are articulated well on the grpc.io homepage and
other blogs and resources. I do not want to reiterate the same points, and will
have links to resources I find useful at the bottom of this post. In short,
gRPC:

-   saves network bandwidth
-   provides faster and more efficient communication
-   can be used by any language
-   offers client-streaming, server-streaming, and bidirectional streaming services
-   allows for easy evolution and iteration of your api, while keeping backward compatability.
-   has an api contract that is easy to write and understand.


## My favourite things so far about gRPC {#my-favourite-things-so-far-about-grpc}

Since I am just starting to explore gRPC, I cannot speak well to the system-wide
advantages of it and how I find it works in production. There are immediate
ergonomic and conceptual advantages to it though that I find quite exciting.


### Writing and Reading API's {#writing-and-reading-api-s}

For one, the type definitions makes writing your api, and understanding others,
quite simple. You can read a \`.proto\` file as if it were documentation (and
still generate documentation from it). For example, a service that takes a
subject and returns a poem would look like this:

```text
syntax = 'proto3';

message Subject {
 string name = 1;
 string mood = 2;
 repeated string keywords = 3;
}

message Poem {
  string title = 1;
  string body = 2;
  int32 edition = 3;
}

message PoemGeneratorRequest {
  Subject subject = 1;
}

message PoemGeneratorResponse {
  Poem poem = 1;
}

service PoemService {
  rpc PoemGenerator(PoemGeneratorRequest) returns (PoemGeneratorResponse) {};
}
```

I found that, with no knowledge of the syntax of protocol buffers, I could
understand specs like this immediately. Much of the proto's syntax is
understanble through context clues. You define some messages that are made up of
fields with specific types, and then define a services for passing these
messages. With protobuf, you work from foundational types that then get
increasingly complex while maintaining consistent syntax. This is possible in a
REST API too through discipline and convention, but here that discipline is
baked into the structure itself.

Also, evolving an API is relatively simple. If I wanted to introduce a new field
in my poem subjects, it would look like so:

```text
message Subject {
 string name = 1;
 string mood = 2;
 repeated string keywords = 3;
 string season = 4;
}
```

Each field has a default value, which is used if no other value is provided. So
services set up for the older api would not pass along the `season` field, and
it'd be interpreted as an empty string. Similarly, if we send messages from the
new api to an old service, it will simply drop any field it doesn't understand.
Deprecating fields requires a bit more work, but is equally straightforward. So
while you will need to ensure your clients account for default values, gRPC
makes it simple to evolve your api without breaking changes.


### Code generation and tool integration {#code-generation-and-tool-integration}

One awesome part of protobuf and gRPC is its code generation. After you've
defined your API, you can use the program [protoc](https://github.com/protocolbuffers/protobuf) to generate code into several
languages. This means much of the logic for my server and client is taken care
of for me, and I could focus on the business logic.

protoc outputs to several different languages, but the one I've been working
with is Go. Go also originated in Google, and you can feel the shared principles
and purpose through how well integrated these three services are. The biggest
productivity boost for me was the LSP integration. I would define a new service,
generate the go code, switch over to my server code and as I started to type the
service's name, my editor would immediately start showing me the methods
available to this service and their signatures. It is like having a quiet, eager
assistant handing you all your tools as you need them. It also meant that I was
immediately working on my code at this strategic higher-level. I was concerned
with the structure and flow of data as so much of the implementation code was
generated for me.


### Reflection and Introspection {#reflection-and-introspection}

Lastly, a quality of gRPC that makes it real exciting to learn is in the ease of
its introspection. The typed nature of protobuf allows for easy, consistent
integration with a range of tools beyond your own services. I saw that
immediately with the LSP integration and emacs, but was truly chuffed when I
discovered the [Evans CLI](https://github.com/ktr0731/evans). If you have reflection enabled on your server, which
is straightforward to do, then you can immediately start communicating with it
using Evans. Evans reminded me a bit of the postgres client \`psql\`, which is one
of my favourite tools. With both, use a simple set of commands to investigate
and richly describe the service you're building in a repl environment. It turns
the development of your services into this dynamic, tangible experience that
rewards curiosity.

I know I have a lot to learn about gRPC, but I am immediately pleased, and
grateful, that the framework has so many features that makes the learning
experience rewarding and fun.


## Resources {#resources}

I've found the following online resources useful for getting into the why's and
how's of gRPC and protobuf:

-   [grpc.io's official docs](https://grpc.io/docs/what-is-grpc/introduction/) are quite good and a great introduction.
-   [The Developer Docs for Protocol Buffers](https://developers.google.com/protocol-buffers/docs/overview) is similarly good.
-   [Alan Shreve's Talk on gRPC](https://www.youtube.com/watch?v=RoXT%5FRkg8LA) is fun and engaging, and he offers a good
    high-level look at the framework, its historical context, and its benefits.
-   [Stephan Maarek's gRPC class on Udemy](https://www.udemy.com/course/grpc-golang/) is in-depth, patient, and hands-on. It is
    a good balance of theory and implementation, with enough footholds for you to
    go on and learn more.
-   [Lyft's Envoy: from Monolith to Service Mesh](https://www.youtube.com/watch?v=RVZX4CwKhGE&t=2915s) is a talk by Matt Klein about the
    Envoy proxy, which is a gRPC api. It's a good talk, that shows the exciting
    and complex things you can design with this framework.
