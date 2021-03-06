# Deep Sentence

Deep Sentence is a deep learning based engine to summarize texts from multiple
sources into a single short summary.

## Table of contents

* [Setup](#setup)
* [Scraper](#scraper)
* [Development](#development)
* [DB Setup](#db-setup)
* [Deployment](#deployment)

## Setup

### Requirements

* Python 3.5
* [psycopg2 requirements](http://initd.org/psycopg/docs/install.html)

The scraper module also relies on [html-extractor-miniserver](https://github.com/tuvistavie/html-extractor-miniserver) which
is available at http://extractor.deepsentence.com

### Installing dependencies

Setup a new virtualenv environment if you want, then simply run

```
make
```

### Configuration

Copy `.env.example` to `.env`, and modify the variables to your needs.

## Scraper

### Usage

To start the scraper, run

```
scrapy crawl line_news
```

if you want a shell to play around with the responses, run

```
scrapy shell ARTICLE_URL --spider=line_news
```

## Learning

### Dependencies

To learn, you will first need to download the word embeddings for word2vec.
You can get them at the following URL: http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/entity_vector.tar.bz2

Or you can use `make download_models` to download them for you.

## Webapp

The web application lives in `deep_sentence/webapp`.

### Requirements

* NodeJS >= 4
* [yarn](https://yarnpkg.com/) (recommended)
* [foreman](https://github.com/ddollar/foreman) (recommended)

### Usage

To install dependencies, run `make prepare_web`.
You can then start the application by running `make dev_webapp`. If you do not
have foreman, you can start the app with `make debug_app` and start webpack
(in another shell) with `make webpack_watch`.

## Guidelines

### Adding dependencies

Run

```
make write_dependencies
```

to regenerate `requirements.txt`.
Please be sure to run this from a clean environment, and only add *needed* dependencies.

## DB setup

You can access the database as follow

```
psql -h public-db.claudetech.com -p 5433 -U deep_sentence
```

To be able to use it in from Python, set `DATABASE_URL` to the following value

```
postgres://deep_sentence:PASSWORD@public-db.claudetech.com:5433/deep_sentence
```

## Deployment

See [deployment/README.md](./deployment/README.md) for more information about how to setup a node.
