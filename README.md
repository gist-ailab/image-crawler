# image-crawler

Crawling images with Python Script. 

---


## Getting Started

### Environment Setup
1. Check the version of Chrome(chrome://settings/help) and download [chrome driver](https://chromedriver.chromium.org/downloads)(chromedriver.exe)
 that fits the version. Make sure the "chromedriver.exe" and "crawl.py" are in same directory(folder).
2. Create Anaconda environment and install requirements to setup python environment.

    ``` shell
    conda create -n crawler python=3.8
    conda activate crawler
    pip install –r requirements.txt
    ```

---

Crawling is performed by collecting URLs for each image by keyword search and downloading the collected URLs.

### Crawling from Google
``` shell
# activate conda env
conda activate crawler

# run script
python crawl.py --web google --num_scroll {int, the number of scrolling} --keyword "{str, KEYWORD, "" are needed if keyword has blank}" --save_path /PATH/TO/SAVE/IMAGES 

# example
python crawl.py --web google --num_scroll 5 --keyword "토마토 피자" --save_path ./img_google
```


### Crawling from Instagram
``` shell
# activate conda env
conda activate crawler

# run script (without LOGIN in INSTAGRAM)
python crawl.py --web instagram --num_scroll {int, the number of scrolling} --keyword "{str, KEYWORD, keyword cannot have any blank}" --save_path /PATH/TO/SAVE/IMAGES 

# example
python crawl.py --web instagram --num_scroll 5 --keyword "토마토피자" --save_path ./img_instagram

# run script (with LOGIN in INSTAGRAM)
python crawl.py --web instagram --num_scroll {int, the number of scrolling} --keyword "{str, KEYWORD, keyword cannot have any blank}" --save_path /PATH/TO/SAVE/IMAGES --login_option {str, facebook or instagram} --login_id {std, LOGIN_ID} --login_pw {std, LOGIN_PW}
```
