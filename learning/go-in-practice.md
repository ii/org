- [Objective](#sec-1)
  - [Buy Book](#sec-1-1)
  - [Access Book](#sec-1-2)
    - [ii pdf via nextcloud PDF viewer](#sec-1-2-1)
    - [pdf directly via docview](#sec-1-2-2)
  - [Access Source Examples](#sec-1-3)
- [Front Matter](#sec-2)
  - [Table of Contents](#sec-2-1)
- [Part 1. Background and fundamentals](#sec-3)
  - [Chapter 1. Getting into Go](#sec-3-1)
    - [1.1. What is Go?](#sec-3-1-1)
    - [1.2. Noteworthy aspects of Go](#sec-3-1-2)
    - [1.3. Go in the vast language landscape](#sec-3-1-3)
    - [1.4. Getting up and running in Go](#sec-3-1-4)
    - [1.5. Hello, Go](#sec-3-1-5)
    - [1.6. Summary](#sec-3-1-6)
  - [Chapter 2. A solid foundation](#sec-3-2)
    - [2.1. Working with CLI applications, the Go way](#sec-3-2-1)
    - [2.2. Handling configuration](#sec-3-2-2)
    - [2.3. Working with real-world web servers](#sec-3-2-3)
    - [2.4. Summary](#sec-3-2-4)
  - [Chapter 3. Concurrency in Go](#sec-3-3)
    - [3.1. Understanding Go’s concurrency model](#sec-3-3-1)
    - [3.2. Working with goroutines](#sec-3-3-2)
    - [3.3. Working with channels](#sec-3-3-3)
    - [3.4. Summary](#sec-3-3-4)
- [Part 2. Well-rounded applications](#sec-4)
  - [Chapter 4. Handling errors and panics](#sec-4-1)
    - [4.1. Error handling](#sec-4-1-1)
    - [4.2. The panic system](#sec-4-1-2)
    - [4.3. Summary](#sec-4-1-3)
  - [Chapter 5. Debugging and testing](#sec-4-2)
    - [5.1. Locating bugs](#sec-4-2-1)
    - [5.2. Logging](#sec-4-2-2)
    - [5.3. Accessing stack traces](#sec-4-2-3)
    - [5.4. Testing](#sec-4-2-4)
    - [5.5. Using performance tests and benchmarks](#sec-4-2-5)
    - [5.6. Summary](#sec-4-2-6)
- [Part 3. An interface for your applications](#sec-5)
  - [Chapter 6. HTML and email template patterns](#sec-5-1)
    - [6.1. Working with HTML templates](#sec-5-1-1)
    - [6.2. Using templates for email](#sec-5-1-2)
    - [6.3. Summary](#sec-5-1-3)
  - [Chapter 7. Serving and receiving assets and forms](#sec-5-2)
    - [7.1. Serving static content](#sec-5-2-1)
    - [7.2. Handling form posts](#sec-5-2-2)
    - [7.3. Summary](#sec-5-2-3)
  - [Chapter 8. Working with web services](#sec-5-3)
    - [8.1. Using REST APIs](#sec-5-3-1)
    - [8.2. Passing and handling errors over HTTP](#sec-5-3-2)
    - [8.3. Parsing and mapping JSON](#sec-5-3-3)
    - [8.4. Versioning REST APIs](#sec-5-3-4)
    - [8.5. Summary](#sec-5-3-5)
- [Part 4. Taking your applications to the cloud](#sec-6)
  - [Chapter 9. Using the cloud](#sec-6-1)
    - [9.1. What is cloud computing?](#sec-6-1-1)
    - [9.2. Managing cloud services](#sec-6-1-2)
    - [9.3. Running on cloud servers](#sec-6-1-3)
    - [9.4. Summary](#sec-6-1-4)
  - [Chapter 10. Communication between cloud services](#sec-6-2)
    - [10.1. Microservices and high availability](#sec-6-2-1)
    - [10.2. Communicating between services](#sec-6-2-2)
    - [10.3. Summary](#sec-6-2-3)
  - [Chapter 11. Reflection and code generation](#sec-6-3)
    - [11.1. Three features of reflection](#sec-6-3-1)
    - [11.2. Structs, tags, and annotations](#sec-6-3-2)
    - [11.3. Generating Go code with Go code](#sec-6-3-3)
    - [11.4. Summary](#sec-6-3-4)
- [End Matter](#sec-7)
  - [Index](#sec-7-1)
  - [List of Figures](#sec-7-2)
  - [List of Listings](#sec-7-3)
- [Extra Notes](#sec-8)
- [References](#sec-9)
  - [local pdf link to pages](#sec-9-1)
  - [write or find ob-golang so ,, works for org golang blocks](#sec-9-2)
  - [Delve](#sec-9-3)
  - [go-playground](#sec-9-4)
  - [look into gocheck](#sec-9-5)
  - [go-coverage](#sec-9-6)
  - [go-guru](#sec-9-7)
  - [gocode => gogetdoc](#sec-9-8)
  - [go-use-test-args](#sec-9-9)
  - [Go Spacemacs Layer Pre-requisites](#sec-9-10)


# Objective<a id="sec-1"></a>

Given a synopsis of *Go in Practice* with a focus on the code examples.

## Buy Book<a id="sec-1-1"></a>

Matt Farina and Matt Butcher wrote a helpful book that we use as the basis for our walkthrough. Please purchase this book from them. We bought a copies for our team.

<http://goinpracticebook.com/>

## Access Book<a id="sec-1-2"></a>

### ii pdf via nextcloud PDF viewer<a id="sec-1-2-1"></a>

<https://nextcloud.ii.nz/apps/files/?dir=/iiFiles/Books&fileid=5114#pdfviewer>

We might be able to skewer this for driving a web browser to follow the right links

### pdf directly via docview<a id="sec-1-2-2"></a>

```emacs-lisp
(setq nextcloud-login (read-string "Nextcloud Login : "))
(setq nextcloud-passwd (read-passwd "Nextcloud Pass : "))
```

<https://docs.nextcloud.com/server/13/user_manual/files/access_webdav.html>

```shell
rm -rf go-in-practive.pdf
curl -s -S -u "${LOGIN}:${PASS}" -L \
  http://nextcloud.ii.nz/remote.php/webdav/iiFiles/Books/Go_in_Practice.pdf \
  -o go-in-practice.pdf
ls -la go-in-practice.pdf
```

-rw-r&#x2013;r&#x2013; 1 hippie hippie 9528205 May 28 14:16 go-in-practice.pdf

<go-in-practice.pdf>

## Access Source Examples<a id="sec-1-3"></a>

```shell
git clone https://github.com/Masterminds/go-in-practice.git
```

# Front Matter<a id="sec-2"></a>

## Table of Contents<a id="sec-2-1"></a>

-   Foreword
-   Preface
-   Acknowledgments
-   About this Book
-   About the Authors
-   About the Cover Illustration
-   Part 1. Background and fundamentals
    -   Ch 1. Getting into Go
    -   Ch 2. A solid foundation
    -   Ch 3. Concurrency in Go
-   Part 2. Well-rounded applications
    -   Ch 4. Handling errors and panics
    -   Ch 5. Debugging and testing
-   Part 3. An interface for your applications
    -   Ch 6. HTML and email template patterns
    -   Ch 7. Serving and receiving assets and forms
    -   Ch 8. Working with web services
-   Part 4. Taking your applications to the cloud
    -   Ch 9. Using the cloud
    -   Ch 10. Communication between cloud services
    -   Ch 11. Reflection and code generation

# Part 1. Background and fundamentals<a id="sec-3"></a>

## Chapter 1. Getting into Go<a id="sec-3-1"></a>

### 1.1. What is Go?<a id="sec-3-1-1"></a>

### 1.2. Noteworthy aspects of Go<a id="sec-3-1-2"></a>

1.  1.2.1. Multiple return values

    [chapter1/returns.go](go-in-practice/chapter1/returns.go) [chapter1/returns2.go](go-in-practice/chapter1/returns2.go)
    
    1.  Direct Linking to code
    
        You can open these and type `, x x` to run `spacemacs/go-run-main` [chapter1/returns.go](go-in-practice/chapter1/returns.go)
    
    2.  INCLUDING the src
    
        `, '` to open this included file in a dedicated buffer. `, x x` to run `spacemacs/go-run-main` The file (and specific lines) will be included in the export.
        
        ```go
        func main() {
          n1, n2 := Names()
          fmt.Println(n1, n2)
        
          n3, _ := Names()
          fmt.Println(n3)
        }
        ```
    
    3.  Inline Code Execution and output
    
        ```go
        func Names() (string, string) {
        return "Foo", "Bar"
        }
        ```
        
        ```go
        
        ```
        
        ```go
        Foo Bar
        Foo
        ```
        
        -   The "underscore" character `_` is used to tell the compiler that "I don't care about this variable or it's content"

2.  1.2.2. A modern standard library

    [chapter1/read<sub>status.go</sub>](go-in-practice/chapter1/read_status.go)
    
    ```go
    package main
    
    import (
      "bufio"
      "fmt"
      "net"
    )
    
    func main() {
      conn, _ := net.Dial("tcp", "golang.org:80")
      fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
      status, _ := bufio.NewReader(conn).ReadString('\n')
      fmt.Println(status)
    }
    ```
    
    ```go
    conn, _ := net.Dial("tcp", "golang.org:80")
    fmt.Fprintf(conn, "GET / HTTP/1.0\r\n\r\n")
    status, _ := bufio.NewReader(conn).ReadString('\n')
    fmt.Println(status)
    ```
    
    -   Networking and HTTP
        -   (net package)
        -   TCP / UDP
        -   client or server role
        -   bufio package
    -   Package bufio implements buffered I/O. It wraps an io.Reader or io.Writer object, creating another object (Reader or Writer) that also implements the interface but provides buffering and some help for textual I/O.
    
    Go - encoding is UTF-8 internally
    
    -   interfaces (review more)
    
    -   HTML
        -   Includes support through `html` and `html/template` packages
    -   Cryptography
        -   Includes support for common cryptography protocols, SHA, TLS, AES and HMAC
    -   Data Encoding
        -   packages -> turn a JSON string into instantiated objects

3.  1.2.3. Concurrency with goroutines and channels

    -   Go scheduler
    -   "multiple processing cores is now the norm"
    -   Other languages (aka Ruby) have a "global thread lock" - which hampers running routines in parallel
    -   "goroutine" , a function that can be run concurrently to the main program or other goroutines. Sometimes dubbed lightweight threads"
        -   Figure 1.2 Goroutines running in threads distributed on the available processing cores
        -   Listing 1.5 Concurrent output
            -   two functions printing concurrently
            -   function `count()` is run in parallel using the keyword `go`, e.g. `go count()`
            -   This causes main to continue executing immediately without needing the count() function to finish first.
    
    [chapter1/goroutine.go](go-in-practice/chapter1/goroutine.go)
    
    ```go
    package main
    
    import (
      "fmt"
      "time"
    )
    
    func count() {
      for i := 0; i < 5; i++ {
        fmt.Println(i)
        time.Sleep(time.Millisecond * 1)
      }
    }
    
    func main() {
      go count()
      time.Sleep(time.Millisecond * 2)
      fmt.Println("Hello World")
      time.Sleep(time.Millisecond * 5)
    }
    ```
    
    ```go
    func count() {
      for i := 0; i < 5; i++ {
        fmt.Println(i)
        time.Sleep(time.Millisecond * 1)
      }
    }
    
    func main() {
      go count()
      time.Sleep(time.Millisecond * 2)
      fmt.Println("Hello World")
      time.Sleep(time.Millisecond * 5)
    }
    ```
    
    -   Concurrency: "channels"
        -   Channels provide a way for two goroutines to communicate with each other.
        -   Channels can be one-directional or bidirectional
    
    [chapter1/channel.go](go-in-practice/chapter1/channel.go)
    
    ```go
    package main
    
    import (
      "fmt"
      "time"
    )
    
    func printCount(c chan int) {
      num := 0
      for num >= 0 {
        num = <-c
        fmt.Print(num, " ")
      }
    }
    
    func main() {
      c := make(chan int)
      a := []int{8, 6, 7, 5, 3, 0, 9, -1}
    
      go printCount(c)
    
      for _, v := range a {
        c <- v
      }
      time.Sleep(time.Millisecond * 1)
      fmt.Println("End of main")
    }
    ```
    
    ```go
    func printCount(c chan int) {
      num := 0
      for num >= 0 {
        num = <-c
        fmt.Print(num, " ")
      }
    }
    
    func main() {
      c := make(chan int)
      a := []int{8, 6, 7, 5, 3, 0, 9, -1}
    
      go printCount(c)
    
      for _, v := range a {
        c <- v
      }
      time.Sleep(time.Millisecond * 1)
      fmt.Println("End of main")
    }
    ```

4.  1.2.4. Go the toolchain—more than a language

    -   go executable is a toolchain enabling more than a compiler
    
    -   package management
        -   lightweight
        -   built in from day one
        -   improve programmer productivity
        -   faster compile time
        -   syntax: `import "fmt"`
        -   syntax: `fmt.Println("Hello Word")`
        -   list packages in alphabetical order
        -   net/http << imports only http section? from the net package.
        -   external packages - reference by URL.
        -   command: `go get`
        -   can use most version-control systems ( git - mercurial - SVN and bazaar ) pg 14
        -   Go retrieves the codebase from Git and checks out the latest commit from the default branch.
        -   Go has no central repository and packages are fetched from their source location.
    
    -   testing
        -   Essential element of software development
        -   syntax: `import "testing"`
        -   testing package provides
            -   a command-line runner
            -   code-coverage reporting
            -   race-condition detection.
        -   naming convention for test files: end in `_test.go`
            -   excluded when the application is built
        -   Command: `go test`
            -   executes the function that begins with Test e.g. TestName
        -   Command: `go test ./...`
            -   Test the current package and the ones nested in subdirectories
        -   Test Results
            -   Listing 1.12 - PASS
            -   Listing 1.13 - FAIL
        -   Use other packages for BDD or other testing patterns
        -   Code Coverage
            -   Command `go test -cover`
            -   Reports the % of coverage provided
            -   Listing 1.14 - output
            -   Export results to files that be used by other tools (example?)
            -   <http://blog.golang.org/cover>
        -   More details on Testing in Chapter 4
    
    -   TODO Explore gocheck / go-use-gocheck-for-testing
    
    <https://github.com/syl20bnr/spacemacs/tree/master/layers/%2Blang/go#tests>
    
    [chapter1/hello/hello.go](go-in-practice/chapter1/hello/hello.go)
    
    ```go
    package main
    
    import "fmt"
    
    func getName() string {
      return "World!"
    }
    
    func main() {
      name := getName()
      fmt.Println("Hello ", name)
    }
    ```
    
    ```go
    func getName() string {
      return "World!"
    }
    
    func main() {
      name := getName()
      fmt.Println("Hello ", name)
    }
    ```
    
    To test, open this file and run `, t t` [chapter1/hello/hello<sub>test.go</sub>](go-in-practice/chapter1/hello/hello_test.go)
    
    ```go
    package main
    
    import "testing"
    
    func TestName(t *testing.T) {
      name := getName()
    
      if name != "World!" {
        t.Error("Respone from getName is unexpected value")
      }
    }
    ```
    
    ```shell
    go test
    ```
    
    ```shell
    go test -cover
    ```
    
    <http://blog.golang.org/cover>
    
    -   Formatting
        -   Tabs vs Spaces ? Style issues/discussions don't help with developer productivity
        -   Idiomatic Go - <https://golang.org/doc/effective_go.html> (Effective Go)
        -   Command: `go fmt`
        -   Rewrites all go files to canonical style.
        -   Use a hook on save to update the current format
        
        -   Explore: Emacs save hook / pre-git commit
        -   Explore: Convert tab to spaces view options
    
    We have some go-lang spacemacs settings to run go fmt on save etc. Might be interesting to see pre-git commit <http://spacemacs.org/layers/+lang/go/README.html> <https://github.com/syl20bnr/spacemacs/tree/master/layers/%2Blang/go>
    
    -   documentation generation
    -   compiler
    -   locate extra options - check: go &#x2013;help
    
    ```shell
    go --help
    ```

### 1.3. Go in the vast language landscape<a id="sec-3-1-3"></a>

-   Go design was for "systems language", with cloud computing a subset.
-   Not good focus for embedded systems due to the runtime and garbage collection.
-   Alternative to C
-   Go provides a runtime that includes features such as managing threads and garbage collection.
-   Go applications have a sweet spot that provides real productivity.
-   Go compiles to a single binary for an operating system to directly execute.
    -   The binary contains the Go runtime, all the imported packages and the entire application.
    -   everything needed to run the program is within a single binary
-   Performance between languages isn't straightforward
-   Go is a statically typed language with dynamic-like features.
    -   Statically typed languages do type checking based on static code analysis.
    -   Go has the ability to do some type switching. Under some circumstances, variables of one type can be turned into variables of a different type.
-   Go has a built-in web server, as illustrated in figure 1.6 (pg 20)

### 1.4. Getting up and running in Go<a id="sec-3-1-4"></a>

-   [http://tour.golang.org](http://tour.golang.org)
-   [https://play.golang.org](https://play.golang.org)

1.  1.4.1. Installing Go

    -   [https://golang.org/dl/](https://golang.org/dl/)

2.  1.4.2. Working with Git, Mercurial, and version control

3.  1.4.3. Exploring the workspace

    -   Go code is expected to be in a workspace.
    -   Base directory referenced by `GOPATH`
    -   workspace has a set directory hierarchy (
        -   bin
        -   pkg
        -   src
    -   Command `go install`
        -   manages the `bin` directory
    -   archive files ?
        -   file suffix .a
        -   stored in the `pkg` directory

4.  1.4.4. Working with environment variables

    -   go executable expect the variable to exist.
    -   `export PATH=$PATH:$GOPATH/bin`
    -   An optional environment variable `GOBIN` for installing binaries to an alternative location,

### 1.5. Hello, Go<a id="sec-3-1-5"></a>

-   Create a web server

[chapter1/hello/inigo.go](go-in-practice/chapter1/inigo.go)

```go
package main

import (
  "fmt"
  "net/http"
)

func hello(res http.ResponseWriter, req *http.Request) {
  fmt.Fprint(res, "Hello, my name is Inigo Montoya")
}

func main() {
  http.HandleFunc("/", hello)
  http.ListenAndServe("localhost:4000", nil)
}
```

```emacs-lisp
;; (setenv "GOPATH" (concat (file-name-directory (buffer-file-name))
            ;; "go-in-practice/chapter1/"))
;;(setenv "GOPATH" nil)
(compile "go run inigo.go") t)
(sleep-for 2)
(display-buffer-at-bottom (get-buffer "*compilation*") nil)
(browse-url-chromium "http:localhost:4000")  2
```

```shell
go build inigo.go
ls -la inigo
# ./inigo
```

-   Command: `go build`
    -   will build the current directory
    -   using a filename, set of filenames, only builds the selection.
    -   the built application needs to be executed

### 1.6. Summary<a id="sec-3-1-6"></a>

-   designed for modern hardware
-   advantage of recent advances in technology
-   provides a toolchain that makes the developer productive
-   goroutines enable concurrent execution

## Chapter 2. A solid foundation<a id="sec-3-2"></a>

### 2.1. Working with CLI applications, the Go way<a id="sec-3-2-1"></a>

-   2.1.1. Command-line flags
-   2.1.2. Command-line frameworks

### 2.2. Handling configuration<a id="sec-3-2-2"></a>

-   Technique 3 Using configuration files
-   Technique 4 Configuration via environment variables

### 2.3. Working with real-world web servers<a id="sec-3-2-3"></a>

-   2.3.1. Starting up and shutting down a server
-   2.3.2. Routing web requests

### 2.4. Summary<a id="sec-3-2-4"></a>

## Chapter 3. Concurrency in Go<a id="sec-3-3"></a>

### 3.1. Understanding Go’s concurrency model<a id="sec-3-3-1"></a>

### 3.2. Working with goroutines<a id="sec-3-3-2"></a>

-   Technique 10 Using goroutine closures
-   Technique 11 Waiting for goroutines
-   Technique 12 Locking with a mutex

### 3.3. Working with channels<a id="sec-3-3-3"></a>

-   Technique 13 Using multiple channels
-   Technique 14 Closing channels
-   Technique 15 Locking with buffered channels

### 3.4. Summary<a id="sec-3-3-4"></a>

# Part 2. Well-rounded applications<a id="sec-4"></a>

## Chapter 4. Handling errors and panics<a id="sec-4-1"></a>

### 4.1. Error handling<a id="sec-4-1-1"></a>

-   Technique 16 Minimize the nils
-   Technique 17 Custom error types
-   Technique 18 Error variables

### 4.2. The panic system<a id="sec-4-1-2"></a>

-   4.2.1. Differentiating panics from errors
-   4.2.2. Working with panics
-   4.2.3. Recovering from panics
-   4.2.4. Panics and goroutines

### 4.3. Summary<a id="sec-4-1-3"></a>

## Chapter 5. Debugging and testing<a id="sec-4-2"></a>

### 5.1. Locating bugs<a id="sec-4-2-1"></a>

-   5.1.1. Wait, where is my debugger?

### 5.2. Logging<a id="sec-4-2-2"></a>

-   5.2.1. Using Go’s logger
-   5.2.2. Working with system loggers

### 5.3. Accessing stack traces<a id="sec-4-2-3"></a>

-   Technique 26 Capturing stack traces

### 5.4. Testing<a id="sec-4-2-4"></a>

-   5.4.1. Unit testing
-   5.4.2. Generative testing

### 5.5. Using performance tests and benchmarks<a id="sec-4-2-5"></a>

-   Technique 29 Benchmarking Go code
-   Technique 30 Parallel benchmarks
-   Technique 31 Detecting race conditions

### 5.6. Summary<a id="sec-4-2-6"></a>

# Part 3. An interface for your applications<a id="sec-5"></a>

## Chapter 6. HTML and email template patterns<a id="sec-5-1"></a>

### 6.1. Working with HTML templates<a id="sec-5-1-1"></a>

-   6.1.1. Standard library HTML package overview
-   6.1.2. Adding functionality inside templates
-   6.1.3. Limiting template parsing
-   6.1.4. When template execution breaks
-   6.1.5. Mixing templates

### 6.2. Using templates for email<a id="sec-5-1-2"></a>

-   Technique 38 Generating email from templates

### 6.3. Summary<a id="sec-5-1-3"></a>

## Chapter 7. Serving and receiving assets and forms<a id="sec-5-2"></a>

### 7.1. Serving static content<a id="sec-5-2-1"></a>

-   Technique 39 Serving subdirectories
-   Technique 40 File server with custom error pages
-   Technique 41 Caching file server
-   Technique 42 Embedding files in a binary
-   Technique 43 Serving from an alternative location

### 7.2. Handling form posts<a id="sec-5-2-2"></a>

-   7.2.1. Introduction to form requests
-   7.2.2. Working with files and multipart submissions
-   7.2.3. Working with raw multipart data

### 7.3. Summary<a id="sec-5-2-3"></a>

## Chapter 8. Working with web services<a id="sec-5-3"></a>

### 8.1. Using REST APIs<a id="sec-5-3-1"></a>

-   8.1.1. Using the HTTP client
-   8.1.2. When faults happen

### 8.2. Passing and handling errors over HTTP<a id="sec-5-3-2"></a>

-   8.2.1. Generating custom errors
-   8.2.2. Reading and using custom errors

### 8.3. Parsing and mapping JSON<a id="sec-5-3-3"></a>

-   Technique 53 Parsing JSON without knowing the schema

### 8.4. Versioning REST APIs<a id="sec-5-3-4"></a>

-   Technique 54 API version in the URL
-   Technique 55 API version in content type

### 8.5. Summary<a id="sec-5-3-5"></a>

# Part 4. Taking your applications to the cloud<a id="sec-6"></a>

## Chapter 9. Using the cloud<a id="sec-6-1"></a>

### 9.1. What is cloud computing?<a id="sec-6-1-1"></a>

-   9.1.1. The types of cloud computing
-   9.1.2. Containers and cloud-native applications

### 9.2. Managing cloud services<a id="sec-6-1-2"></a>

-   9.2.1. Avoiding cloud provider lock-in
-   9.2.2. Dealing with divergent errors

### 9.3. Running on cloud servers<a id="sec-6-1-3"></a>

-   9.3.1. Performing runtime detection
-   9.3.2. Building for the cloud
-   9.3.3. Performing runtime monitoring

### 9.4. Summary<a id="sec-6-1-4"></a>

## Chapter 10. Communication between cloud services<a id="sec-6-2"></a>

### 10.1. Microservices and high availability<a id="sec-6-2-1"></a>

### 10.2. Communicating between services<a id="sec-6-2-2"></a>

1.  10.2.1. Making REST faster

    1.  TECHNIQUE 62: Reusing connections
    
    2.  TECHNIQUE 63: Faster JSON marshal and unmarshal
    
        -   <https://github.com/ugorji/go>

2.  10.2.2. Moving beyond REST

    1.  TECHNIQUE 64: Using protocol buffers
    
    2.  TECHNIQUE 65: Communicating over RPC with protocol buffers

### 10.3. Summary<a id="sec-6-2-3"></a>

## Chapter 11. Reflection and code generation<a id="sec-6-3"></a>

### 11.1. Three features of reflection<a id="sec-6-3-1"></a>

-   Technique 66 Switching based on type and kind
-   Technique 67 Discovering whether a value implements an interface
-   Technique 68 Accessing fields on a struct

### 11.2. Structs, tags, and annotations<a id="sec-6-3-2"></a>

-   11.2.1. Annotating structs
-   11.2.2. Using tag annotations

### 11.3. Generating Go code with Go code<a id="sec-6-3-3"></a>

-   Technique 70 Generating code with go generate

### 11.4. Summary<a id="sec-6-3-4"></a>

# End Matter<a id="sec-7"></a>

## Index<a id="sec-7-1"></a>

## List of Figures<a id="sec-7-2"></a>

## List of Listings<a id="sec-7-3"></a>

# Extra Notes<a id="sec-8"></a>

-   [gocode: An autocompletion daemon for the Go programming language](https://github.com/mdempsky/gocode)

# References<a id="sec-9"></a>

-   Test link to PDF: /home/hippie/ii/org/learning/go-in-practice.pdf
