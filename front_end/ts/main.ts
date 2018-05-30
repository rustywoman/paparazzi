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
declare let hljs: any;
declare let Ps:any;
declare let axios:any;


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Klass
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Main{
  customLoadingIns : LoadingHandler;
  markerHandlerIns : MarkerHandler;
  contentRootDOM : HTMLElement;
  DOM_PARSER_INS : any;
  ASYNC_LOOP_START_INDEX : number;
  ASYNC_LOOP_RATE : number;
  ASYNC_LOOP_STOP_INDEX : number;
  constructor(customLoadingIns:LoadingHandler, markerHandlerIns:MarkerHandler, contentRootDOM:HTMLElement){
    this.customLoadingIns = customLoadingIns;
    this.markerHandlerIns = markerHandlerIns;
    this.contentRootDOM = contentRootDOM;
    this.DOM_PARSER_INS = new DOMParser();
    this.ASYNC_LOOP_START_INDEX = 0;
    this.ASYNC_LOOP_RATE = 30;
    this.ASYNC_LOOP_STOP_INDEX = 30;
  };
  handleAsyncContentLoader(asyncLoadURL:string){
    console.warn('Content URL : ' + asyncLoadURL);
    this.ASYNC_LOOP_START_INDEX = 0;
    this.ASYNC_LOOP_RATE = 30;
    this.ASYNC_LOOP_STOP_INDEX = 30;
    document.querySelector('#j_raw_url').innerHTML = '';
    this.customLoadingIns.reset();
    setTimeout(
      () => {
        window.history.pushState(
          {
            'name' : asyncLoadURL.replace('/', '')
          },
          null,
          asyncLoadURL
        );
        axios(asyncLoadURL)
          .then(
            (res:any) => {
              let doc = this.DOM_PARSER_INS.parseFromString(res.data, 'text/html');
              this.contentRootDOM.innerHTML = doc.querySelector('#wrapper').innerHTML;
              document.querySelector('#j_raw_url').innerHTML = doc.querySelector('#j_raw_url').innerHTML;
              this.init(true);
            }
          );
      },
      800
    );
  };
  bindAsyncContentLoad(){
    let contentTriggers = document.querySelectorAll('.j_async_content_load');
    for(let i = 0, il = contentTriggers.length; i < il; i++){
      if(!contentTriggers[i].classList.contains(CONSTANT.COMMON_MARKER)){
        contentTriggers[i].classList.add(CONSTANT.COMMON_MARKER);
        contentTriggers[i].addEventListener(
          'click',
          (evt:any) => {
            this.handleAsyncContentLoader(evt.currentTarget.getAttribute('data-async-href'));
          },
          false
        )
      }
    }
  };
  bindHighlight(){
    let rawCodes = document.querySelectorAll('pre code');
    for(let i = 0, il = rawCodes.length; i < il; i++){
      hljs.highlightBlock(rawCodes[i]);
    }
  };
  // bindCustomToggle(){
  //   let digestTriggerStack:any = {};
  //   let digestTriggers = document.querySelectorAll('.j_digest_detail_trigger');
  //   let digestToggleAreas = document.querySelectorAll('.j_toggle');
  //   if(
  //     (digestTriggers.length !== 0 && digestToggleAreas.length !== 0) &&
  //     (digestTriggers.length === digestToggleAreas.length)
  //   ){
  //     for(let i = 0, il = digestToggleAreas.length; i < il; i++){
  //       digestTriggerStack[digestToggleAreas[i].getAttribute('data-target-url')] = digestToggleAreas[i];
  //       digestToggleAreas[i].setAttribute('data-hidden-height', (digestToggleAreas[i].clientHeight + 20) + 'px');
  //       digestToggleAreas[i].setAttribute('style', 'height: 0px');
  //       digestTriggers[i].addEventListener(
  //         'click',
  //         (evt:any) => {
  //           let tmpToggledDOM = digestTriggerStack[evt.currentTarget.getAttribute('data-target-url')];
  //           tmpToggledDOM.setAttribute('style', 'height:' + tmpToggledDOM.getAttribute('data-hidden-height'));
  //         },
  //         false
  //       );
  //     }
  //   }
  // };
  handleAsyncImageLoader(wrapperDOM:HTMLElement){
    return new Promise(
      (resolve:any, reject:any) => {
        let tmpImg = document.createElement('img');
        wrapperDOM.appendChild(tmpImg);
        tmpImg.addEventListener(
          'load',
          (evt:any) => {
            let loadedImg = evt.target;
            loadedImg.classList.add(CONSTANT.LOADED_MARKER);
            resolve();
          },
          false
        );
        tmpImg.addEventListener(
          'error',
          (evt:any) => {
            let loadedImg = evt.target;
            loadedImg.classList.add(CONSTANT.ERROR_MARKER);
            loadedImg.setAttribute('src', CONSTANT.DUMMY_IMAGE_BASE64_SRC);
            resolve();
          },
          false
        );
        tmpImg.setAttribute('src', wrapperDOM.getAttribute('data-async-src'));
      }
    );
  };
  bindCustom404(){
    let errorTitleDOM = document.querySelector('#error__title');
    if(errorTitleDOM !== null){
      setTimeout(
        () => {
          this.handleAsyncContentLoader('/');
        },
        5000
      )
    }
  };
  bindCustomScrollBar(){
    let psDOM:any = {};
    let psWrapperDOM = document.querySelectorAll('.m_column_ps_wrapper');
    for(let i = 0, il = psWrapperDOM.length; i < il; i++){
      Ps.initialize(
        psWrapperDOM[i],
        {
          wheelSpeed         : 1,
          minScrollbarLength : 10
        }
      );
      let tmpYRailDOM = psWrapperDOM[i].querySelector('.ps__scrollbar-y-rail');
      let tmpYRailDOMStatus = tmpYRailDOM.clientHeight !== STATUS.NG ? STATUS.OK : STATUS.NG;
      if(tmpYRailDOMStatus === STATUS.NG){
        tmpYRailDOM.classList.add(CONSTANT.COMMON_MARKER);
      }
      psDOM[psWrapperDOM[i].getAttribute('data-handle-trigger')] = {
        'wrapper' : psWrapperDOM[i],
        'status'  : tmpYRailDOMStatus
      };
    }
    let psTriggerDOM = document.querySelectorAll('.j_to_scroll_trigger');
    for(let i = 0, il = psTriggerDOM.length; i < il; i++){
      if(psDOM[psTriggerDOM[i].getAttribute('data-handle-ps-wrapper')]['status'] === 1){
        psTriggerDOM[i].addEventListener(
          'click',
          (evt:any) => {
            let tmpDOM = psDOM[evt.currentTarget.getAttribute('data-handle-ps-wrapper')]['wrapper'];
            switch(evt.currentTarget.getAttribute('data-ps-direction')){
              case 'top':
                tmpDOM.scrollTop = 0;
                break;
              case 'bottom':
                tmpDOM.scrollTop = tmpDOM.scrollTopMax ? tmpDOM.scrollTopMax : tmpDOM.scrollHeight - tmpDOM.clientHeight;
                break;
            }
          },
          false
        );
      }
    }
  };
  bindAsyncImageLoad(callback:any){
    let asyncImages = [].slice.call(document.querySelectorAll('.j_async_image_load'));
    let asyncImagesNum = asyncImages.length;
    let DEFS = [];
    let asyncLoadImages = asyncImages.slice(this.ASYNC_LOOP_START_INDEX, this.ASYNC_LOOP_STOP_INDEX);
    for(var i = 0, il = asyncLoadImages.length; i < il; i++){
      DEFS.push(this.handleAsyncImageLoader(asyncLoadImages[i]));
    }
    Promise.all(DEFS)
      .then(
        () => {
          this.ASYNC_LOOP_START_INDEX = this.ASYNC_LOOP_START_INDEX + this.ASYNC_LOOP_RATE;
          this.ASYNC_LOOP_STOP_INDEX = this.ASYNC_LOOP_START_INDEX + this.ASYNC_LOOP_RATE;
          if(this.ASYNC_LOOP_START_INDEX >= asyncImagesNum){
            console.log('All Images Downloaded');
            callback();
          }else{
            var asyncLoadStatus = Math.ceil((this.ASYNC_LOOP_START_INDEX / asyncImagesNum) * 100);
            if(asyncLoadStatus >= 80){
              asyncLoadStatus = 79;
            }
            this.customLoadingIns
              .init(asyncLoadStatus)
              .then(
                () => {
                  this.bindAsyncImageLoad(callback);
                }
              );
          }
        }
      )
  };
  bindPopStateEvent(){
    window.addEventListener(
      'popstate',
      (evt:any) => {
        if(evt.state === null){
          this.handleAsyncContentLoader('/');
        }else{
          this.handleAsyncContentLoader(evt.state.name);
        }
      },
      false
    );
  };
  init(asyncFlg:boolean){
    if(!asyncFlg){
      this.bindPopStateEvent();
    }
    document.body.setAttribute('style', 'overflow: hidden !important;');
    if(document.querySelectorAll('.j_async_image_load').length > 0){
      this.bindAsyncImageLoad(
        () => {
          this.customLoadingIns
            .init(84)
            .then(
              () => {
                this.bindAsyncContentLoad();
                this.bindHighlight();
                this.bindCustomScrollBar();
                this.markerHandlerIns.reset();
                this.customLoadingIns
                  .init(100)
                  .then(
                    () => {
                      document.body.setAttribute('style', '');
                      this.markerHandlerIns
                        .init()
                        .then(
                          () => {
                            console.warn('>>> Done [ Initial Access ] with images <<<');
                          }
                        );
                    }
                  );
              }
            );
        }
      );
    }else{
      this.customLoadingIns
        .init(80)
        .then(
          () => {
            this.bindAsyncContentLoad();
            this.bindHighlight();
            this.bindCustomScrollBar();
            this.markerHandlerIns.reset();
            this.customLoadingIns
              .init(100)
              .then(
                () => {
                  document.body.setAttribute('style', '');
                  this.markerHandlerIns
                    .init()
                    .then(
                      () => {
                        this.bindCustom404();
                        console.warn('>>> Done [ Initial Access ] without images <<<');
                      }
                    );
                }
              );
          }
        );
    }
  }
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Init
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
document.addEventListener(
  'DOMContentLoaded',
  () => {
    // let mainIns = new Main(
    //   new LoadingHandler(
    //     document.querySelector('#loading__bg'),
    //     document.querySelector('#loading__status'),
    //     CONSTANT.LOADED_MARKER
    //   ),
    //   new MarkerHandler('overlay'),
    //   document.querySelector('#wrapper')
    // );
    // mainIns.init(false);
    document.querySelector('#j_api_trigger_for_creatation').addEventListener(
      'click',
      (evt:any) => {
        let tmpElmDOM = evt.currentTarget;
        if(!tmpElmDOM.classList.contains(CONSTANT.COMMON_MARKER)){
          tmpElmDOM.classList.add(CONSTANT.COMMON_MARKER);
          tmpElmDOM.innerHTML = '<span>Processing ...</span>';
          let tmpReportNameDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_name'));
          let tmpReportName = tmpReportNameDOM.value.trim();
          let tmpReportURLDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_url'));
          let tmpReportURL = tmpReportURLDOM.value.trim();
          if(tmpReportName !== '' && tmpReportURL !== ''){
            axios.post(
              '/create',
              {
                'name' : tmpReportName,
                'url'  : tmpReportURL
              }
            ).then(
              (res:any) => {
                setTimeout(
                  () => {
                    tmpElmDOM.classList.remove(CONSTANT.COMMON_MARKER);
                    tmpElmDOM.innerHTML = '<span>Create</span>';
                  },
                  2000
                );
              }
            );
          }else{
            console.error('>>> Invalid Input <<<');
            tmpReportNameDOM.value = '';
            tmpReportURLDOM.value = '';
            tmpElmDOM.classList.remove(CONSTANT.COMMON_MARKER);
            tmpElmDOM.innerHTML = '<span>Create</span>';
          }
        }
      },
      false
    );
    document.querySelector('#j_api_trigger_for_execution').addEventListener(
      'click',
      (evt:any) => {
        axios.post(
          '/execute',
          {
            'name' : (<HTMLInputElement>document.querySelector('#j_direct_report_name')).value
          }
        ).then(
          (res:any) => {
            console.log(res.data);
          }
        );
      },
      false
    );
  },
  false
);