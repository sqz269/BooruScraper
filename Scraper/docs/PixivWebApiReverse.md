# Search API

> Base URL: https://www.pixiv.net/ajax/search/artworks/{}?word={}&order={}&mode={}&scd={}&ecd={}&p={}&s_mode={}&type={}&wlt={}&wgt={}&hlt={}&hgt={}&ratio={}&tool={}


## PARAMETER DOCUMENTATION

#### URL Path \{string(space-separated)}
- /artworks/\<Tags>/  --> Specific tags to search for, "-" can be used to exclude certain words
- Configuration Cross-Reference: TAGS, TAGS_EXCLUDE

#### word \{string(space-separated)}
- so far it's the same as the \<Tags> fields in the url path
- Configuration Cross-Reference: TAGS, TAGS_EXCLUDE

#### order \{string(pre-defined)}
- 2 known values: [`date`, `date_d`]. 
- value `date` sort images from oldest to newest
- `date_d` sort it from new to old
- Configuration Cross-Reference: SORTED_BY


#### s_mode \{string(pre-defined)}
- 3 known values: [`s_tag_full`, `s_tag`, `s_tc`]
- `s_tag_full` will find exact match of tags 
- `s_tag` will partially match the tag
- `s_tc` will try to match the key words in: tags, description, and title of the submission
- Configuration Cross-Reference: SEARCH_MODE

#### mode \{string(pre-defined)}
- 3 known values: [`all`, `safe`, `r18`]
- `all` will return both explicit images and non-explicit images
- `safe` will only return non-explicit images
- `r18` will ony return explicit images
- Configuration Cross-Reference: RATING

#### p \{int}
- the current page number
- Configuration Cross-Reference: START_PAGE, END_PAGE

#### type \{string(pre-defined)}
- 5 known values [`all`, `illust_and_ugoira`, `illust`, `manga`, `ugoira`] for filtering submission content types
- `all` will return illustration, moving illustrations (basically gifs), and manga
- `illust_and_ugoira` will only return illustration and gifs
- `illust` will only return illustrations
- `manga` will only return manga
- `ugoira` will only return gifs
- Configuration Cross-Reference: SUBMISSION_TYPE

#### scd \{string(time-stamp)}
- `scd` probably stand for *start *** date*
- will return submissions in a time range, this parameter specific the start time of the time range.
- for example: scd=2020-03-08 will return all submissions between your current time to 2020-03-08 (assuming ecd is not present)
- Configuration Cross-Reference: SUBMISSION_AFTER

#### ecd \{string(time-stamp)}
- `ecd` probably stand for *end *** date*
- will return all submissions in a time range, this parameter specific the end time of the time range.
- for example: ecd=2020-03-08 will return all submissions from the beginning to 2020/03/08 (assuming scd not present)
- Configuration Cross-Reference: SUBMISSION_BEFORE

#### wlt \{int}
- `wlt` probably stand for *width larger than*
- will only return submissions with resolution that is higher than this width
- Configuration Cross-Reference: WIDTH_MIN

#### hlt \{int}
- `hlt` probably stand for *height larger than*
- will only return submissions with resolution that is higher than this height
- Configuration Cross-Reference: HEIGHT_MIN

#### wgt \{int}
- `wgt` probably stand for *width (not greater) than*
- will only return submissions with resolution that is lower than this width
- Configuration Cross-Reference: WIDTH_MAX

#### hgt \{int}
- `hgt` probably stand for *height (not greater) than*
- will only return submissions with resolution that is lower than this height
- Configuration Cross-Reference: HEIGHT_MAX

#### ratio \{float}
- will return the submissions with this very specific ratio
- range from 1 to -1, 0 means it's a square
- a number larger than 0 means the submission's width is larger than it's height
- a number smaller than 0 means the submission's width is less than it's height
- pixiv's search uses -0.5 to search for portrait and 0.5 for landscape images
- Configuration Cross-Reference: ORIENTATION

#### tool \{string}  ~~Probably the most useless field~~
- will only return submissions that is made using this tool
- idk what tools there are cuz im not an artist
- Configuration Cross-Reference: TOOL


## SAMPLE
### Sample Query And Explanation
> https://www.pixiv.net/ajax/search/artworks/%E8%89%A6%E9%9A%8A%E3%81%93%E3%82%8C%E3%81%8F%E3%81%97%E3%82%87%E3%82%93%20-R-18G?word=%E8%89%A6%E9%9A%8A%E3%81%93%E3%82%8C%E3%81%8F%E3%81%97%E3%82%87%E3%82%93%20-R-18G&order=date_d&mode=safe&scd=2019-04-02&ecd=2020-03-16&p=1&s_mode=s_tag&type=all&wlt=1000&wgt=2999&hlt=1000&hgt=2999&ratio=0.5&tool=SAI


- Search Submissions with tag that partially match: 艦隊これくしょん. **Key Param: {word, s_mode}**
- Display result from the newest submission to oldest. **Key Param: {order}**
- Search only non-explicit images. **Key Param: {mode}**
- Search submissions that's submitted only during 2019-04-02 to 2020-03-16 **Key Param: {scd, ecd}**
- Search the first page of the result. **Key Param: {p}**
- Search all of the submission type: manga, ugoira, and illust. **Key Param: {type}**
- Search only submissions with size between 1,000px - 2,999px wide and 1,000px - 2,999px high **Key Param: {wlt, hlt, wgt, hgt}**
- Search only submissions that have landscape orientation **Key Param: {ratio}**
- Search only submissions that is created by software SAI **Key Param: {tool}**

# SEARCH API RESPONSE
### **NOTE: RESPONSES HAS BEEN TRUNCATED TO REDUCE THE SIZE OF THE MARKDOWN FILE**
### Response Type: JSON

#### Response Sample: OK (Note: it does not contain bookmark count) [Valid as of 2020-03-15]
> {"error": false,
    "body": {
        "illustManga": {
            "data": [
                {
                    "illustId": "80156845",
                    "illustTitle": "I字クマ",
                    "id": "80156845",
                    "title": "I字クマ",
                    "illustType": 0,
                    "xRestrict": 0,
                    "restrict": 0,
                    "sl": 6,
                    "url": "https://i.pximg.net/c/250x250_80_a2/img-master/img/2020/03/16/13/01/18/80156845_p0_square1200.jpg",
                    "description": "",
                    "tags": [
                        "MikuMikuDance",
                        "MMD",
                        "MMD艦これ",
                        "艦これ",
                        "艦隊これくしょん",
                        "阿武隈(艦これ)",
                        "I字バランス"
                    ],
                    "userId": "67247",
                    "userName": "islander",
                    "width": 1666,
                    "height": 2000,
                    "pageCount": 1,
                    "isBookmarkable": true,
                    "bookmarkData": null,
                    "alt": "#MikuMikuDance I字クマ - islander的插画",
                    "isAdContainer": false,
                    "profileImageUrl": "https://i.pximg.net/user-profile/img/2017/09/02/21/00/18/13154027_cafdd4048e15127edb269b34fdc0b230_50.jpg"
                }, ...
            ],
            "total": 616931,
            "bookmarkRanges": [...]
        },
        "popular": {
            "recent": [...],
            "permanent": [...]
        },
        "relatedTags": [...],
        "tagTranslation": {...},
        "zoneConfig": {...},
        "extraData": {...}
    }
}
`
