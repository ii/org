# Our Blog

This directory holds the source and content for our site/blog, located at https://ii.coop
It is built with [hugo](https://gohugo.io), a static site generator.

## Running the site locally

If you are editing pages or styles, it is recommended to run the site locally to see the results of your changes before you push them.

To do this, first install hugo following their [installation instructions](https://gohugo.io/getting-started/installing)

If installed correctly, you can run this command:

``` sh
hugo version
```

which should return something similar to:

``` sh
hugo v0.81.0+extended darwin/amd64 BuildDate=unknown
```

Then clone this repo and navigate to the blog folder

``` sh
git clone git@github.com/ii/org && cd org/blog
```

from here, run the hugo server

``` sh
hugo server 
```

this will start the site up, viewable at http://localhost:1313

## Key Directory Structure for Contributors
In this directory, the main folders you are concerned about are `content` and `static`
- content :: holds all the text copy for the site, written in markdown
- static :: holds all assets (like images) and our custom CSS

## The Content Directory
The content maps to the pages of the site. So The file located at

`content/blog/deplying-talos-to-equinix.md` 

can be seen online at

https://ii.coop/blog/deplying-talos-to-equinix

Similarly `content/about.md` maps to https://ii.coop/about

## Referencing images in posts

You can reference images using the [hugo-flavoured markdown syntax](https://learn.netlify.app/en/cont/markdown/)

the syntax is:

``` md
![alt text](image_path "title text")
```
(alt text is what will appear if the image doesnt' load, and is used for accessibility.  title text is what shows upon hovering over the image.  It is optional)

Everying in our `static` folder gets put into the root of the website. So if I placed DOG_PICTURE.png at `static/images/DOG_PICTURE.png`, I would include it in my blog post with:

``` markdown
![picture of a dog](/images/DOG_PICTURE.png)
```

_Note that we start with a slash, and don't include /static/_

Alternatively, you can refernece a picture from the web, like so:

``` markdown
![picture of a cat](https://catpics.com/fluffy-cat.png)
```

`
