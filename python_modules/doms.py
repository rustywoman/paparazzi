#! /usr/bin/python
# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import Configuration Dir.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import constant
import textwrap


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def generateTextsInfo(textsInfo):
    u'''Generate Text Information
     @param  textsInfo - Texts Information
     @return String DOM for Text Information
    '''
    textInfoDOM = ''
    for textInfo in textsInfo:
        textInfoDOM = textInfoDOM + textwrap.dedent('''
            <div class="m_content__css_digest_table__row">
              <div class="m_content__css_digest_table__cell">{0}</div>
            </div>
        ''').format(textInfo).strip()
    return textInfoDOM


def generateImagesInfo(testName, imagesInfo):
    u'''Generate Image Information
     @param  testName   - Test name
     @param  imagesInfo - Images Information
     @return String DOM for Image Information
    '''
    imageInfoDOM = ''
    for imageInfo in imagesInfo:
        if imageInfo['status'] == 1:
            imageDownLoadStatus = 'o'
        elif imageInfo['status'] == 0:
            imageDownLoadStatus = 'x'
        else:
            imageDownLoadStatus = '-'
        imageInfoDOM = imageInfoDOM + textwrap.dedent('''
            <div class="m_content__image_digest_table__row">
              <div class="m_content__image_digest_table__cell">{path}</div>
              <div class="m_content__image_digest_table__cell">{status}</div>
              <div class="m_content__image_digest_table__cell j_async_image_load" data-async-src="{asyncSrc}"></div>
            </div>
        ''').format(
            path=imageInfo['path']['raw'],
            status=imageDownLoadStatus,
            asyncSrc='/assets/image/' + testName + '/' + imageInfo['path']['local']
        ).strip()
    return imageInfoDOM


def generateCssGeneralInfo(cssGeneralInfo):
    u'''Generate Css Information - [ general ]
     @param  cssGeneralInfo - Css Information
     @return String DOM for Css Information - [ general ]
    '''
    return textwrap.dedent('''
        <div class="m_content__css_digest_table__row">
          <div class="m_content__css_digest_table__cell">{total}</div>
          <div class="m_content__css_digest_table__cell">{okCount} ( {okRate} % )</div>
          <div class="m_content__css_digest_table__cell">{ngCount} ( {ngRate} % )</div>
          <div class="m_content__css_digest_table__cell">{unknownCount} ( {unknownRate} % )</div>
        </div>
    ''').format(
        total=cssGeneralInfo['total'],
        okCount=cssGeneralInfo['ok']['count'],
        okRate=cssGeneralInfo['ok']['rate'],
        ngCount=cssGeneralInfo['ng']['count'],
        ngRate=cssGeneralInfo['ng']['rate'],
        unknownCount=cssGeneralInfo['unknown']['count'],
        unknownRate=cssGeneralInfo['unknown']['rate']
    ).strip()


def generateCssDetailInfo(parseResult):
    u'''Generate Css Information - [ detail ]
     @param  parseResult - Css Parsed Result
     @return String DOM for Css Information - [ detail ( inline + ref ) ]
    '''
    inlineCssInfoDOM = ''
    refCssInfoDOM = ''
    for cssInfo in parseResult:
        if cssInfo['path'] == 'inline':
            cssSelectorInfoDOM = ''
            for cssSelectorInfo in cssInfo['detail']:
                cssSelectorInfoDOM = cssSelectorInfoDOM + textwrap.dedent('''
                    <div class="m_content__css_table__row">
                      <div class="m_content__css_table__cell">{selector}</div>
                      <div class="m_content__css_table__cell">{count}</div>
                    </div>
                ''').format(
                    selector=cssSelectorInfo['selector'],
                    count=cssSelectorInfo['count']
                ).strip()
            inlineCssInfoDOM = inlineCssInfoDOM + textwrap.dedent('''
                <li class="m_section__ref_css_list__item">
                  <p class="m_section__css_digest_detail_trigger_wrapper">
                    <a class="j_digest_detail_trigger marker" href="javascript:void(0);" data-target-url="inline_css">More</a>
                  </p>
                  <div class="j_toggle" data-target-url="inline_css">
                    <div class="m_section__css_digest_table">
                      <div class="m_content__css_digest_table__row">
                        <div class="m_content__css_digest_table__cell ___head">Total</div>
                        <div class="m_content__css_digest_table__cell ___head">OK</div>
                        <div class="m_content__css_digest_table__cell ___head">NG</div>
                        <div class="m_content__css_digest_table__cell ___head">Unknown</div>
                      </div>
                      <div class="m_content__css_digest_table__row">
                        <div class="m_content__css_digest_table__cell">{total}</div>
                        <div class="m_content__css_digest_table__cell">{okCount}</div>
                        <div class="m_content__css_digest_table__cell">{ngCount}</div>
                        <div class="m_content__css_digest_table__cell">{unknownCount}</div>
                      </div>
                    </div>
                    <div class="m_content__css_table">
                      <div class="m_content__css_table__row">
                        <div class="m_content__css_table__cell ___head">Selector Definition</div>
                        <div class="m_content__css_table__cell ___head">Matched DOM Count</div>
                      </div>
                      {cssSelectorInfoDOM}
                    </div>
                  </div>
                </li>
            ''').format(
                total=cssInfo['digest']['total'],
                okCount=cssInfo['digest']['ok'],
                ngCount=cssInfo['digest']['ng'],
                unknownCount=cssInfo['digest']['unknown'],
                cssSelectorInfoDOM=cssSelectorInfoDOM
            ).strip()
        else:
            cssSelectorInfoDOM = ''
            for cssSelectorInfo in cssInfo['detail']:
                cssSelectorInfoDOM = cssSelectorInfoDOM + textwrap.dedent('''
                    <div class="m_content__css_table__row">
                      <div class="m_content__css_table__cell">{selector}</div>
                      <div class="m_content__css_table__cell">{count}</div>
                    </div>
                ''').format(
                    selector=cssSelectorInfo['selector'],
                    count=cssSelectorInfo['count']
                ).strip()

            refCssInfoDOM = refCssInfoDOM + textwrap.dedent('''
                <li class="m_section__ref_css_list__item">
                  <h4 class="m_section__ref_css__file_name">{path}</h4>
                  <p class="m_section__css_digest_detail_trigger_wrapper">
                    <a class="j_digest_detail_trigger marker" href="javascript:void(0);" data-target-url="{path}">More</a>
                  </p>
                  <div class="j_toggle" data-target-url="{path}">
                    <div class="m_section__css_digest_table">
                      <div class="m_content__css_digest_table__row">
                        <div class="m_content__css_digest_table__cell ___head">Total</div>
                        <div class="m_content__css_digest_table__cell ___head">OK</div>
                        <div class="m_content__css_digest_table__cell ___head">NG</div>
                        <div class="m_content__css_digest_table__cell ___head">Unknown</div>
                      </div>
                      <div class="m_content__css_digest_table__row">
                        <div class="m_content__css_digest_table__cell">{total}</div>
                        <div class="m_content__css_digest_table__cell">{okCount}</div>
                        <div class="m_content__css_digest_table__cell">{ngCount}</div>
                        <div class="m_content__css_digest_table__cell">{unknownCount}</div>
                      </div>
                    </div>
                    <div class="m_content__css_table">
                      <div class="m_content__css_table__row">
                        <div class="m_content__css_table__cell ___head">Selector Definition</div>
                        <div class="m_content__css_table__cell ___head">Matched DOM Count</div>
                      </div>
                      {cssSelectorInfoDOM}
                    </div>
                  </div>
                </li>
            ''').format(
                path=cssInfo['path'],
                total=cssInfo['digest']['total'],
                okCount=cssInfo['digest']['ok'],
                ngCount=cssInfo['digest']['ng'],
                unknownCount=cssInfo['digest']['unknown'],
                cssSelectorInfoDOM=cssSelectorInfoDOM
            ).strip()
    return {
        'refCssInfoDOM': refCssInfoDOM,
        'inlineCssInfoDOM': inlineCssInfoDOM
    }


def generateRefScriptInfo(refScriptsInfo):
    u'''Generate Ref. Script Information
     @param  refScriptsInfo - Script Result
     @return String DOM for Script Information
    '''
    refScriptInfoDOM = ''
    for refScriptInfo in refScriptsInfo:
        refScriptInfoDOM = refScriptInfoDOM + textwrap.dedent('''
            <li class="m_section__ref_js_list__item">
              <h4 class="m_section__ref_js__file_name">{refScript}</h4>
              <p class="m_section__css_digest_detail_trigger_wrapper">
                <a class="marker" href="{refScript}" target="_blank">More</a>
              </p>
            </li>
        ''').format(
            refScript=refScriptInfo
        ).strip()
    return refScriptInfoDOM
