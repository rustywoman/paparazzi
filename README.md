<br />
<br />

<p align="center">
  <h1 align="center" style="color: #00171f">P A P A R A Z Z I</h1>
</p>

<br />

#### How To Use

１． Download and Install Python (Anaconda3) in your own Machine.

２． Activate Terminal or Console and Change Directory to This Directory.

３． Execute Bellow:

```
  pip install -r paparazzi.pip.txt
```

４． Execute Sample:

```
  sh main.sh
```

<br />
<br />

#### How To Test

_./case/sample.json_

```
{
  "name" : "TEST CASE MAIN NAME",
  "case" : [
    {
      "url"  : "https://www.google.co.jp/",
      "name" : "TEST CASE SUB NAME == RESULT DIRECTORY NAME",
      "action" : [
        "input---xpath---//*[@id='lst-ib']---hogehogehoge",
        "PHOTO---google_xpath",
        "enter---xpath---//*[@id='lst-ib']",
        "WAIT"
      ]
    }
  ]
}
```

<br />
<br />

#### Environment

| Module                   | Version |
|:-------------------------|:--------|
| Windows 10 (64bit, 16GB) | 1709    |

<br />

#### Modules

| Module           | Detail                     |
|:-----------------|:---------------------------|
| beautifulsoup4   | version 4.6.0              |
| selenium         | version 3.7.0              |
| tqdm             | version 4.19.4             |

<br />
<br />