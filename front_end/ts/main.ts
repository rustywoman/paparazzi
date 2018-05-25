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
// ToDo : Rename 'node_modules/@types/highlight.js' ---> node_modules/@types/highlightjs
import * as hljs from 'highlightjs';
import axios from 'axios';


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
            (res) => {
              let doc = this.DOM_PARSER_INS.parseFromString(res.data, 'text/html');
              this.contentRootDOM.innerHTML = doc.querySelector('#wrapper').innerHTML;
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
  bindCustomToggle(){
    let digestTriggerStack:any = {};
    let digestTriggers = document.querySelectorAll('.j_digest_detail_trigger');
    let digestToggleAreas = document.querySelectorAll('.j_toggle');
    for(let i = 0, il = digestToggleAreas.length; i < il; i++){
      digestTriggerStack[digestToggleAreas[i].getAttribute('data-target-url')] = digestToggleAreas[i];
    }
    for(let i = 0, il = digestTriggers.length; i < il; i++){
      digestTriggers[i].addEventListener(
        'click',
        (evt:any) => {
          digestTriggerStack[evt.currentTarget.getAttribute('data-target-url')].setAttribute('style', 'display: block;');
        },
        false
      )
    }
  };
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
            console.log('Image Loading Status : [ ' + asyncLoadStatus + ' ]');
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
        this.handleAsyncContentLoader(evt.state.name);
      },
      false
    );
  };
  init(asyncFlg:boolean){
    if(!asyncFlg){
      this.bindPopStateEvent();
    }
    let tmpImages = document.querySelectorAll('.j_async_image_load');
    if(tmpImages.length > 0){
      this.bindAsyncImageLoad(
        () => {
          this.customLoadingIns
            .init(84)
            .then(
              () => {
                this.bindAsyncContentLoad();
                this.bindHighlight();
                this.bindCustomToggle();
                this.markerHandlerIns.reset();
                this.customLoadingIns
                  .init(100)
                  .then(
                    () => {
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
            this.bindCustomToggle();
            this.markerHandlerIns.reset();
            this.customLoadingIns
              .init(100)
              .then(
                () => {
                  this.markerHandlerIns
                    .init()
                    .then(
                      () => {
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
    let mainIns = new Main(
      new LoadingHandler(
        document.querySelector('#loading__bg'),
        document.querySelector('#loading__status'),
        CONSTANT.LOADED_MARKER
      ),
      new MarkerHandler('overlay'),
      document.querySelector('#wrapper')
    );
    mainIns.init(false);
  },
  false
);