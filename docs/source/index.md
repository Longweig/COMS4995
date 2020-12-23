# Welcome to FreeFree's Documentation!

# FreeFree
[![Build Status](https://travis-ci.com/Longweig/FreeFree.svg?branch=master)](https://travis-ci.com/Longweig/FreeFree) 
![Codecov](https://img.shields.io/codecov/c/github/Longweig/FreeFree)
[![Documentation Status](https://readthedocs.org/projects/freefree/badge/?version=latest)](https://freefree.readthedocs.io/en/latest/?badge=latest)
![GitHub](https://img.shields.io/github/license/Longweig/FreeFree) 
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Longweig/freefree?include_prereleases)

## Motivations
There are always some books that we don't need anymore but someone may want them. Although we can use second-hand platform to sell the books, sometimes we may want to just give or even throw them away since there is no insufficient space to store them. Also, sometimes we want some books for temporary use but it's a waste to buy them. A free book give-way platform will help these people especially for students to get the books they need and give away the books then unwanted.

## What is it
This web applicaion that aims to help people to get books they want for free. People can sign up to be a user and get the notifications of the availibilities to the books they need. Also, based on their locations some items have higher priorities to be recommended. Uses can use wishlist of ISBN number or book info to note which books they need. It's a good way to help and benefit each other.

## More features
1. More items (like furniture, pet products) to be in the list
2. Based on the owners' intention, some items can be provided with a second-hand trading platform

## Release Status
There are two release (v0.1.0 and v0.1.1) of this project.
For specifi release notes, please redirect to the repo for more [details](https://github.com/Longweig/FreeFree/releases).

# API Documentation
```eval_rst
.. autoclass:: spider.book_item.Book
    :members:
.. autoclass:: view_models.book.BookViewModel
    :members:
.. autoclass:: view_models.book.BookCollection
    :members:
.. autoclass:: view_models.drift.DriftViewModel
    :members:
.. autoclass:: models.gift.Gift
    :members:
.. autoclass:: models.user.User
    :members:
.. autofunction:: models.user.get_user
.. autofunction:: libs.helper.is_isbn_or_key
.. autoclass:: libs.http_helper.HTTP
    :members:
.. autoclass:: libs.enums.PendingStatus
    :members:
```


