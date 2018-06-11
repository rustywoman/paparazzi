// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Original Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import CONSTANT from 'conf/CONSTANT';
import STATUS from 'conf/STATUS';
import LoadingHandler from 'klass/LoadingHandler';
import MarkerHandler from 'klass/MarkerHandler';
import DependencyTreeHandler from 'klass/DependencyTreeHandler';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module - Raw Library
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/**
 * @author      rustywoman
 * @description Custom Declarration - [ hljs ]
 * @type        {any}
 */
declare let hljs: any;
/**
 * @author      rustywoman
 * @description Custom Declarration - [ Ps ]
 * @type        {any}
 */
declare let Ps:any;
/**
 * @author      rustywoman
 * @description Custom Declarration - [ axios ]
 * @type        {any}
 */
declare let axios:any;


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Klass
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
/**
 * @classdesc   Main
 * @author      rustywoman
 * @description Main SPA
 */
class Main{
  customLoadingIns       : LoadingHandler;
  markerHandlerIns       : MarkerHandler;
  dependencyTreeIns      : DependencyTreeHandler;
  contentRootDOM         : HTMLElement;
  DOM_PARSER_INS         : any;
  ASYNC_LOOP_START_INDEX : number;
  ASYNC_LOOP_RATE        : number;
  ASYNC_LOOP_STOP_INDEX  : number;
  /**
   * @constructor Main
   * @param    {object} customLoadingIns       - Instance Of `LoadingHandler` class
   * @param    {object} markerHandlerIns       - Instance Of `MarkerHandler` class
   * @param    {object} dependencyTreeIns      - Instance Of `DependencyTreeHandler` class
   * @param    {object} contentRootDOM         - Content Root raw DOM
   * @property {object} customLoadingIns       - Instance Of `LoadingHandler` class
   * @property {object} markerHandlerIns       - Instance Of `MarkerHandler` class
   * @property {object} dependencyTreeIns      - Instance Of `DependencyTreeHandler` class
   * @property {object} contentRootDOM         - Content Root raw DOM
   * @property {object} DOM_PARSER_INS         - DOM raw Parser
   * @property {number} ASYNC_LOOP_START_INDEX - Async Load Start Index For Image
   * @property {number} ASYNC_LOOP_RATE        - Async Load Unit For Image
   * @property {number} ASYNC_LOOP_STOP_INDEX  - Async Load Stop Index For Image
   */
  constructor(customLoadingIns:LoadingHandler, markerHandlerIns:MarkerHandler, dependencyTreeIns:DependencyTreeHandler, contentRootDOM:HTMLElement){
    this.customLoadingIns = customLoadingIns;
    this.markerHandlerIns = markerHandlerIns;
    this.dependencyTreeIns = dependencyTreeIns;
    this.contentRootDOM = contentRootDOM;
    this.DOM_PARSER_INS = new DOMParser();
    this.ASYNC_LOOP_START_INDEX = 0;
    this.ASYNC_LOOP_RATE = 30;
    this.ASYNC_LOOP_STOP_INDEX = 30;
  };
  /**
   * Handler - [ Body Style ]
   * @description Handle Body Style
   * @param  {boolean} availableFlg - Available Flg
   * @return {void}
   */
  handleBodyStyle(availableFlg:boolean):void{
    document.body.setAttribute('style', availableFlg ? '' : 'overflow: hidden !important;');
  };
  /**
   * Handler - [ Async Loader for Content ]
   * @description Handle Async Loader for Content
   * @param  {string} asyncLoadURL - Async URL
   * @return {void}
   */
  handleAsyncContentLoader(asyncLoadURL:string):void{
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
      CONSTANT.DEFAULT_DELAY
    );
  };
  /**
   * Binder - [ Async Loader for Content ]
   * @description Bind Async Loader for Content
   * @return {void}
   */
  bindAsyncContentLoad():void{
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
  /**
   * Binder - [ HighLight ]
   * @description Bind HighLight.js
   * @return {void}
   */
  bindHighlight():void{
    let rawCodes = document.querySelectorAll('pre code');
    for(let i = 0, il = rawCodes.length; i < il; i++){
      hljs.highlightBlock(rawCodes[i]);
    }
  };
  /**
   * Handler - [ Async Loader for Image ]
   * @description Handle Async Loader for Image with Promise
   * @param  {object} wrapperDOM - Image Wrapper raw DOM
   * @return {any}
   */
  handleAsyncImageLoader(wrapperDOM:HTMLElement):any{
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
  /**
   * Binder - [ Custom Error ]
   * @description Bind Custom Error with redirect `/`
   * @return {void}
   */
  bindCustom404():void{
    let errorTitleDOM = document.querySelector('#error__title');
    if(errorTitleDOM !== null){
      setTimeout(
        () => {
          this.handleAsyncContentLoader('/');
        },
        CONSTANT.ERROR_DELAY
      )
    }
  };
  /**
   * Binder - [ Custom Scroll ]
   * @description Bind Custom Scroll
   * @return {void}
   */
  bindCustomScrollBar():void{
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
  /**
   * Binder - [ Async Loader for Image ]
   * @description Bind Async Loader for Image with Promise
   * @param  {object} callback - Last Callback Function
   * @return {void}
   */
  bindAsyncImageLoad(callback:any):void{
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
  /**
   * Binder - [ `popstate` ]
   * @description Bind `History Back` and `History Forward` Action
   * @return {void}
   */
  bindPopStateEvent():void{
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
  /**
   * Binder - [ Trigger for Dynamic Reporter ]
   * @description Bind Trigger for Dynamic Reporter
   * @return {void}
   */
  bindDynamicReporterTrigger():void{
    let dynamicResetTriggerDOM = document.querySelector('#j_api_trigger_for_reset');
    let dynamicCreateTriggerDOM = document.querySelector('#j_api_trigger_for_creatation');
    let dynamicExecuteTriggerDOM = document.querySelector('#j_api_trigger_for_execution');
    if(dynamicResetTriggerDOM !== null && dynamicCreateTriggerDOM !== null && dynamicExecuteTriggerDOM !== null){
      dynamicResetTriggerDOM.addEventListener(
        'click',
        (evt:any) => {
          let tmpElmDOM = evt.currentTarget;
          let tmpReportCreationTriggerDOM = document.querySelector('#j_api_trigger_for_creatation');
          let tmpReportNameDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_name'));
          let tmpReportURLDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_url'));
          let tmpReportExecTriggerDOM = document.querySelector('#j_api_trigger_for_execution');
          tmpReportNameDOM.value = '';
          tmpReportURLDOM.value = '';
          tmpReportCreationTriggerDOM.classList.remove(CONSTANT.COMMON_MARKER);
          tmpReportCreationTriggerDOM.innerHTML = '<span>Create</span>';
          tmpReportNameDOM.classList.remove(CONSTANT.ERROR_MARKER);
          tmpReportURLDOM.classList.remove(CONSTANT.ERROR_MARKER);
          tmpReportNameDOM.removeAttribute('disabled');
          tmpReportURLDOM.removeAttribute('disabled');
          tmpElmDOM.classList.remove(CONSTANT.COMMON_MARKER);
          tmpReportExecTriggerDOM.innerHTML = '<span>Execute</span>';
          tmpReportExecTriggerDOM.classList.add(CONSTANT.HIDDEN_MARKER);
        },
        false
      );
      dynamicCreateTriggerDOM.addEventListener(
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
            let tmpReportExecTriggerDOM = document.querySelector('#j_api_trigger_for_execution');
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
                      tmpReportNameDOM.setAttribute('disabled', '');
                      tmpReportURLDOM.setAttribute('disabled', '');
                      tmpElmDOM.innerHTML = '<span>Created</span>';
                      tmpReportExecTriggerDOM.classList.remove(CONSTANT.HIDDEN_MARKER);
                      tmpReportExecTriggerDOM.innerHTML = '<span>Execute [ ' + tmpReportName + ' ]</span>';
                    },
                    CONSTANT.DEFAULT_DELAY
                  );
                }
              );
            }else{
              tmpReportNameDOM.value = '';
              tmpReportURLDOM.value = '';
              tmpElmDOM.innerHTML = '<span>Create</span>';
              tmpReportNameDOM.classList.add(CONSTANT.ERROR_MARKER);
              tmpReportURLDOM.classList.add(CONSTANT.ERROR_MARKER);
              setTimeout(
                () => {
                  tmpReportNameDOM.classList.remove(CONSTANT.ERROR_MARKER);
                  tmpReportURLDOM.classList.remove(CONSTANT.ERROR_MARKER);
                  tmpElmDOM.classList.remove(CONSTANT.COMMON_MARKER);
                },
                CONSTANT.DEFAULT_DELAY
              );
            }
          }
        },
        false
      );
      dynamicExecuteTriggerDOM.addEventListener(
        'click',
        (evt:any) => {
          let tmpElmDOM = evt.currentTarget;
          if(!tmpElmDOM.classList.contains(CONSTANT.COMMON_MARKER) && !tmpElmDOM.classList.contains(CONSTANT.HIDDEN_MARKER)){
            tmpElmDOM.classList.add(CONSTANT.COMMON_MARKER);
            tmpElmDOM.innerHTML = '<span>Processing ...</span>';
            axios.post(
              '/execute',
              {
                'name' : (<HTMLInputElement>document.querySelector('#j_direct_report_name')).value
              }
            ).then(
              (res:any) => {
                let reporterStatus = res.data['status'];
                let reporterURL = res.data['reportURL'];
                setTimeout(
                  () => {
                    if(reporterStatus === 1){
                      this.handleAsyncContentLoader('/' + reporterURL);
                    }else{
                      let tmpReportCreationTriggerDOM = document.querySelector('#j_api_trigger_for_creatation');
                      let tmpReportNameDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_name'));
                      let tmpReportURLDOM = (<HTMLInputElement>document.querySelector('#j_direct_report_url'));
                      tmpElmDOM.innerHTML = '<span>Execute [ Error ]</span>';
                      setTimeout(
                        () => {
                          tmpReportNameDOM.value = '';
                          tmpReportURLDOM.value = '';
                          tmpReportCreationTriggerDOM.classList.remove(CONSTANT.COMMON_MARKER);
                          tmpReportCreationTriggerDOM.innerHTML = '<span>Create</span>';
                          tmpReportNameDOM.classList.remove(CONSTANT.ERROR_MARKER);
                          tmpReportURLDOM.classList.remove(CONSTANT.ERROR_MARKER);
                          tmpReportNameDOM.removeAttribute('disabled');
                          tmpReportURLDOM.removeAttribute('disabled');
                          tmpElmDOM.classList.remove(CONSTANT.COMMON_MARKER);
                          tmpElmDOM.innerHTML = '<span>Execute</span>';
                          tmpElmDOM.classList.add(CONSTANT.HIDDEN_MARKER);
                        },
                        CONSTANT.DEFAULT_DELAY
                      )
                    }
                  },
                  CONSTANT.DEFAULT_DELAY
                );
              }
            );
          }
        },
        false
      );
    }
  };
  /**
   * Binder - [ Sync Scroll for Screenshot ]
   * @description Bind Trigger for Screenshot Link
   * @return {void}
   */
  bindSyncScroll():void{
    let hoverTriggers = document.querySelectorAll('.j_hover');
    for(let i = 0, il = hoverTriggers.length; i < il; i++){
      hoverTriggers[i].addEventListener(
        'click',
        (evt:any) => {
          let tmpTriggerDOM = evt.currentTarget;
          let syncScrollWrapperDOM = document.querySelector('#j_sync_scroll');
          let syncScrollTargetDOM = (<HTMLElement>document.querySelector('#' + tmpTriggerDOM.getAttribute('data-scroll-pos')));
          syncScrollWrapperDOM.scrollTop = syncScrollTargetDOM.offsetTop - CONSTANT.DOM_DEFAULT_BUFFER;
        },
        false
      );
    }
  };
  /**
   * Handler - [ Init Loading ]
   * @description Handle Init Loading
   * @param  {string} doneMsgForDev - Console Message For Dev.
   * @return {void}
   */
  handleInitLoaing(doneMsgForDev:string){
    this.customLoadingIns
      .init(84)
      .then(
        () => {
          this.bindAsyncContentLoad();
          this.bindHighlight();
          this.bindCustomScrollBar();
          this.bindDynamicReporterTrigger();
          this.bindSyncScroll();
          this.markerHandlerIns.reset();
          this.customLoadingIns
            .init(100)
            .then(
              () => {
                this.handleBodyStyle(true);
                this.markerHandlerIns
                  .init()
                  .then(
                    () => {
                      this.bindCustom404();
                      console.warn('>>> Done [ Initial Access ] ' + doneMsgForDev + ' <<<');
                    }
                  );
              }
            );
        }
      );
  };
  /**
   * Init
   * @description Initialize
   * @param  {boolean} asyncFlg - Async or First Access
   * @return {void}
   */
  init(asyncFlg:boolean):void{
    if(!asyncFlg){
      this.bindPopStateEvent();
    }
    this.handleBodyStyle(false);
    let tmpTreeDOM = document.querySelector('#l_content__tree_container');
    if(tmpTreeDOM){
      this.dependencyTreeIns.init(
        '#l_content__tree_container',
        '#l_content__tree_detail_wrapper',
        '/assets/json/' + tmpTreeDOM.getAttribute('data-tree-dependency')
      ).then(
        () => {
          // Test
          // this.dependencyTreeIns.search('propertyA');
          this.handleInitLoaing('Dependency Tree');
        }
      )
    }else{
      if(document.querySelectorAll('.j_async_image_load').length > 0){
        this.bindAsyncImageLoad(
          () => {
            this.handleInitLoaing('with Images');
          }
        );
      }else{
        this.handleInitLoaing('without Images');
      }
    }
  };
};


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Init
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
document.addEventListener(
  'DOMContentLoaded',
  () => {
    let mainIns = new Main(
      new LoadingHandler(
        document.querySelector('#loading__bg'),
        document.querySelector('#loading__status'),
        CONSTANT.LOADED_MARKER
      ),
      new MarkerHandler('overlay'),
      new DependencyTreeHandler(),
      document.querySelector('#wrapper')
    );
    mainIns.init(false);
  },
  false
);