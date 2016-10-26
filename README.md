# vadskajagdricka

### Mashup service that recommends a beverage from Systembolaget based on visual attributes of a webcam picture.

### Get up and running
#### Create a virtual environment and install dependencies:

```bash
virtualenv --no-site-packages --distribute -p $(which python3) .env && source .env/bin/activate && pip install -r requirements.txt
```
#### Install Sass:

http://sass-lang.com/install

Make sass watch for changes:
```
sass --watch src/static/scss:src/static/css
```
