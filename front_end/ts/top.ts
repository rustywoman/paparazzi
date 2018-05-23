// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Original Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import CONSTANT from 'conf/CONSTANT';
import STATUS from 'conf/STATUS';
import LoadingHandler from 'klass/LoadingHandler';
import MarkerHandler from 'klass/MarkerHandler';

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Raw Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import axios from 'axios';


let generateReportLinkList = (reportLinkListRootDOM:HTMLElement, projectListJSON: Array<{ name : string, path : string, date : string }>) => {
  let tmpResultInfo = null;
  let reportResultEmptyDOM = [
    [
      '<div class="m_content__report_table__row">',
        '<div class="m_content__report_table__cell ___head">Project Name</div>',
        '<div class="m_content__report_table__cell ___head">Date</div>',
      '</div>'
    ].join('')
  ];
  for(var i = 0, il = projectListJSON.length; i < il; i++){
    tmpResultInfo = projectListJSON[i];
    reportResultEmptyDOM.push(
      [
        '<div class="m_content__report_table__row">',
          '<div class="m_content__report_table__cell">',
            '<a class="marker" href="' + tmpResultInfo['path'] +  '" target="_blank">',
              '<span>' + tmpResultInfo['name'] + '</span>',
            '</a>',
          '</div>',
          '<div class="m_content__report_table__cell">' + tmpResultInfo['date'] + '</div>',
        '</div>'
      ].join('')
    );
  }
  reportLinkListRootDOM.innerHTML = reportResultEmptyDOM.join('');
};


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Init
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
document.addEventListener(
  'DOMContentLoaded',
  () => {
    let customLoadingIns = new LoadingHandler(
      document.querySelector('#loading__bg'),
      document.querySelector('#loading__status'),
      CONSTANT.LOADED_MARKER
    );
    let markerHandlerIns = new MarkerHandler('marker');
    axios(
      {
        method : 'get',
        url    : '/index.json'
      }
    ).then(
      (res) => {
        customLoadingIns
          .init(60)
          .then(
            () => {
              generateReportLinkList(
                document.querySelector('#l_content__report_table'),
                res.data
              );
              customLoadingIns
                .init(80)
                .then(
                  () => {
                    markerHandlerIns.reset();
                    customLoadingIns
                      .init(100)
                      .then(
                        () => {
                          markerHandlerIns
                            .init()
                            .then(
                              function(){
                                console.info('>>> Initialized - Top [ / ] <<<');
                              }
                            );
                        }
                      );
                  }
                );
            }
          );
      }
    ).catch(
      (err) => {
        console.error(err);
      }
    );
  },
  false
);