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
        textInfoDOM = textInfoDOM + constant.BR.join(
            [
                '<div class="m_content__css_digest_table__row">',
                '<div class="m_content__css_digest_table__cell">{0}</div>'.format(textInfo),
                '</div>'
            ]
        )
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
        imageInfoDOM = imageInfoDOM + constant.BR.join(
            [
                '<div class="m_content__image_digest_table__row">',
                '<div class="m_content__image_digest_table__cell">{0}</div>'.format(imageInfo['path']['raw']),
                '<div class="m_content__image_digest_table__cell">{0}</div>'.format(imageDownLoadStatus),
                '<div class="m_content__image_digest_table__cell j_async_image_load" data-async-src="/{0}/{1}/{2}/{3}">'.format('assets', 'image', testName, imageInfo['path']['local']),
                '</div>',
                '</div>'
            ]
        )
    return imageInfoDOM


def generateCssGeneralInfo(cssGeneralInfo):
    u'''Generate Css Information - [ general ]
     @param  cssGeneralInfo - Css Information
     @return String DOM for Css Information - [ general ]
    '''
    return constant.BR.join(
        [
            '<div class="m_content__css_digest_table__row">',
            '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssGeneralInfo['total']),
            '<div class="m_content__css_digest_table__cell">{0} ( {1} % )</div>'.format(cssGeneralInfo['ok']['count'], cssGeneralInfo['ok']['rate']),
            '<div class="m_content__css_digest_table__cell">{0} ( {1} % )</div>'.format(cssGeneralInfo['ng']['count'], cssGeneralInfo['ng']['rate']),
            '<div class="m_content__css_digest_table__cell">{0} ( {1} % )</div>'.format(cssGeneralInfo['unknown']['count'], cssGeneralInfo['unknown']['rate']),
            '</div>'
        ]
    )


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
                cssSelectorInfoDOM = cssSelectorInfoDOM + constant.BR.join(
                    [
                        '<div class="m_content__css_table__row">',
                        '<div class="m_content__css_table__cell">{0}</div>'.format(cssSelectorInfo['selector']),
                        '<div class="m_content__css_table__cell">{0}</div>'.format(cssSelectorInfo['count']),
                        '</div>'
                    ]
                )
            inlineCssInfoDOM = inlineCssInfoDOM + constant.BR.join(
                [
                    '<li class="m_section__ref_css_list__item">',
                    '<p class="m_section__css_digest_detail_trigger_wrapper">',
                    '<a class="j_digest_detail_trigger marker" href="javascript:void(0);" data-target-url="inline_css">More</a>',
                    '</p>',
                    '<div class="j_toggle" data-target-url="inline_css">',
                    '<div class="m_section__css_digest_table">',
                    '<div class="m_content__css_digest_table__row">',
                    '<div class="m_content__css_digest_table__cell ___head">Total</div>',
                    '<div class="m_content__css_digest_table__cell ___head">OK</div>',
                    '<div class="m_content__css_digest_table__cell ___head">NG</div>',
                    '<div class="m_content__css_digest_table__cell ___head">Unknown</div>',
                    '</div>',
                    '<div class="m_content__css_digest_table__row">',
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['total']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['ok']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['ng']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['unknown']),
                    '</div>',
                    '</div>'
                    '<div class="m_content__css_table">',
                    '<div class="m_content__css_table__row">',
                    '<div class="m_content__css_table__cell ___head">Selector Definition</div>',
                    '<div class="m_content__css_table__cell ___head">Matched DOM Count</div>',
                    '</div>',
                    cssSelectorInfoDOM,
                    '</div>',
                    '</div>',
                    '</li>'
                ]
            )
        else:
            cssSelectorInfoDOM = ''
            for cssSelectorInfo in cssInfo['detail']:
                cssSelectorInfoDOM = cssSelectorInfoDOM + constant.BR.join(
                    [
                        '<div class="m_content__css_table__row">',
                        '<div class="m_content__css_table__cell">{0}</div>'.format(cssSelectorInfo['selector']),
                        '<div class="m_content__css_table__cell">{0}</div>'.format(cssSelectorInfo['count']),
                        '</div>'
                    ]
                )
            refCssInfoDOM = refCssInfoDOM + constant.BR.join(
                [
                    '<li class="m_section__ref_css_list__item">',
                    '<h4 class="m_section__ref_css__file_name">{0}</h4>'.format(cssInfo['path']),
                    '<p class="m_section__css_digest_detail_trigger_wrapper">',
                    '<a class="j_digest_detail_trigger marker" href="javascript:void(0);" data-target-url="{0}">More</a>'.format(cssInfo['path']),
                    '</p>',
                    '<div class="j_toggle" data-target-url="{0}">'.format(cssInfo['path']),
                    '<div class="m_section__css_digest_table">',
                    '<div class="m_content__css_digest_table__row">',
                    '<div class="m_content__css_digest_table__cell ___head">Total</div>',
                    '<div class="m_content__css_digest_table__cell ___head">OK</div>',
                    '<div class="m_content__css_digest_table__cell ___head">NG</div>',
                    '<div class="m_content__css_digest_table__cell ___head">Unknown</div>',
                    '</div>',
                    '<div class="m_content__css_digest_table__row">',
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['total']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['ok']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['ng']),
                    '<div class="m_content__css_digest_table__cell">{0}</div>'.format(cssInfo['digest']['unknown']),
                    '</div>',
                    '</div>'
                    '<div class="m_content__css_table">',
                    '<div class="m_content__css_table__row">',
                    '<div class="m_content__css_table__cell ___head">Selector Definition</div>',
                    '<div class="m_content__css_table__cell ___head">Matched DOM Count</div>',
                    '</div>',
                    cssSelectorInfoDOM,
                    '</div>',
                    '</div>',
                    '</li>'
                ]
            )
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
        refScriptInfoDOM = refScriptInfoDOM + constant.BR.join(
            [
                '<li class="m_section__ref_js_list__item">',
                '<h4 class="m_section__ref_js__file_name">{0}</h4>'.format(refScriptInfo),
                '<p class="m_section__css_digest_detail_trigger_wrapper">',
                '<a class="marker" href="{0}" target="_blank">More</a>'.format(refScriptInfo),
                '</p>',
                '</li>'
            ]
        )
    return refScriptInfoDOM
