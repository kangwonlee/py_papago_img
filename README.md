# py_papago_img

## Objective
* To translate an image file using Papago Image Translator API

## Cost
* Expected 120 KRW per call

## Limits
| Item | Limit |
|:---|:---|
| formats | jpg, jpeg, png, tiff |
| Maximum image size | 20 MB |
| Maximum image width | 1960 px |
| Maximum image height | 1960 px |

## How to use
### Preparations
* Check following instructions
  * en https://guide.ncloud-docs.com/docs/en/papago-image-translation-overview
  * ko https://guide.ncloud-docs.com/docs/ko/papago-image-translation-overview
* Go to Papago Image Translator page
  * https://www.ncloud.com/product/aiService/papagoImageTranslation
* Apply for using the service
* May need to add payment method

### Procedure
* Fork this repository to your Github account
* Create a Google Driver folder containing PNG files to be translated (below 50 files)
  * Set permission to "Anyone with the link can view"
* Add following secrets under Settings/Secrets and variables/Actions
  * `NAVER_APPLICATION_ID` : Papago Image Translator API client ID
  * `NAVER_SECRET` : Papago Image Translator API client secret
  * `PNG_URL` : Google Drive folder containing PNG files to be translated
  * `SRC`, `TGT` : Source and target languages
* Create an (empty) issue at the forked Github repository
  * Close & reopen it to start the workflow
  * When the workflow is finished, download the artifacts

## Reference
* Papago Image Translator Overview<br>
English https://guide.ncloud-docs.com/docs/en/papago-image-translation-overview<br>
Korean https://guide.ncloud-docs.com/docs/ko/papago-image-translation-overview

* Papago Image Translator API Guide<br>
English https://api.ncloud-docs.com/docs/en/ai-naver-imagetoimageapi<br>
Korean https://api.ncloud-docs.com/docs/ai-naver-imagetoimageapi

## Copyright
* Korea Copyright Commision C-2023-046753
