<br />
<br />

<p align="center">
  <h1 align="center" style="color: #00171f">P A P A R A Z Z I</h1>
</p>
<br />

<p align="center">
  Auto Test Via Client Browser - Parse and Check HTML + Css, Download All Assets, etc ...
</p>

<br />

<p align="center">
  <img src="https://user-images.githubusercontent.com/4089628/41570263-ff516390-73a8-11e8-9269-fdc194d75792.png" alt="" width="80%">
</p>

<br />

#### How To Start

This Project Needs Python 3.x ( Anaconda 3.x recommended ), Node.js and Browser Driver.

---

_Python 3.x ( Anaconda 3.x recommended ) :_

> pip install -r requirements.txt

| Module           | Detail                     |
|:-----------------|:---------------------------|
| beautifulsoup4   | version 4.6.0              |
| jsbeautifier     | version 1.7.5              |
| htmlmin          | version 0.1.12             |
| selenium         | version 3.7.0              |
| tqdm             | version 4.19.4             |
| tinycss          | version 0.4                |
| pytz             | version 2017.2             |
| numpy            | any                        |

---

_Node.js :_

> npm install

| Module                      | Detail          |
|:----------------------------|:----------------|
| axios                       | version 0.18.0  |
| body-parser                 | version 1.18.3  |
| cookie-parser               | version 1.4.3   |
| css-loader                  | version 0.28.7  |
| ejs                         | version 2.6.1   |
| express                     | version 4.16.3  |
| express-session             | version 1.15.6  |
| extract-text-webpack-plugin | version 3.0.2   |
| node-sass                   | version 4.6.0   |
| sass-loader                 | version 7.0.1   |
| style-loader                | version 0.21.0  |
| ts-loader                   | version 3.1.1   |
| typescript                  | version 2.6.1   |
| webpack                     | version 3.8.1   |
| webpack-dev-middleware      | version 2.0.6   |
| webpack-dev-server          | version 2.9.4   |
| webpack-hot-middleware      | version 2.22.2  |
| webpack-livereload-plugin   | version 1.0.0   |

---

_Browser Driver :_

| Browser Name | Driver Link                                                                                        |
|:-------------|:---------------------------------------------------------------------------------------------------|
| Edge         | [https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/ 'Edge Driver') |
| Chrome       | [https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads 'Chrome Driver')    |
| Firefox      | [https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases 'Firefox Driver')                 |

<br />
<br />

#### How To Use @ Terminal

Execute :

| Command      | Detail                                            | Configuration      |
|:-------------|:--------------------------------------------------|:-------------------|
| sh main.sh   | Research Web Page ( crawl, log in-out, etc ... )  | case/*_main.json   |
| sh multi.sh  | Research Web Page in Multi-Process                | case/*_multi.json  |
| sh report.sh | Research Style ( css selector, image, etc ... )   | case/*_report.json |
| sh scan.sh   | Scanning All Links                                | case/*_scan.json   |
| sh search.sh | Searching Keywords                                | case/*_search.json |

<br />
<br />

#### How To Use @ Local Web Service - dev.

Execute :

> npm run start:dev

<br />
<br />

#### How To Use @ Local Web Service - prod.

Execute :

> npm run start:build

> npm run start:prod

<br />
<br />