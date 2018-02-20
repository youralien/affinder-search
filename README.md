# Affinder Search 

### Data for TF-IDF of Yelp Categories

You can find the TF-IDF matrix and the corresponding metadata [via this Dropbox link](https://www.dropbox.com/sh/hn4t4k9zbppm6dd/AAArh08p3n6C0YQAfsDGqVxda?dl=0).  You'll create a folder called `tfidf` at the top-level directory of this repository, and then download those files into there.

### Installation

For production, certain packages are only needed.  They can be found in `requirements.txt`.

For local development, which includes training of the system, we list all supported packages in `dev-requirements.txt`

Recommend using virtiualenv, by creating both prod and dev virtualenvs.
#### Production
```
virtualenv prod
pip install -r requirements.txt
```
```

#### Development

```
virtualenv dev
brew install mysql
pip install -r dev-requirements.txt
```
