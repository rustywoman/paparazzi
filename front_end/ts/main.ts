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
    let DOM_PARSER_INS = new DOMParser();
    let CONTENT_ROOT = document.querySelector('#wrapper');
    // Check Async Trigger
    let contentTriggers = document.querySelectorAll('.j_async_content_load');
    for(let i = 0, il = contentTriggers.length; i < il; i++){
      contentTriggers[i].addEventListener(
        'click',
        (evt:any) => {
          let contentURL = evt.currentTarget.getAttribute('data-async-href');
          window.history.pushState(
            {
              name : contentURL.replace('/', '')
            },
            null,
            contentURL
          );
          // Revive `Loading`
          customLoadingIns.reset();
          axios(contentURL)
            .then(
              (res) => {
                let doc = DOM_PARSER_INS.parseFromString(res.data, 'text/html');
                customLoadingIns
                  .init(80)
                  .then(
                    () => {
                      CONTENT_ROOT.innerHTML = doc.querySelector('#wrapper').innerHTML;
                      markerHandlerIns.reset();
                      customLoadingIns
                        .init(100)
                        .then(
                          () => {
                            markerHandlerIns
                              .init()
                              .then(
                                () => {
                                  console.warn('>>> Done <<<');
                                }
                              );
                          }
                        );
                    }
                  );
              }
            )
        },
        false
      )
    }

    // Check 'highlight'
    let rawCodes = document.querySelectorAll('pre code');
    for(let i = 0, il = rawCodes.length; i < il; i++){
      hljs.highlightBlock(rawCodes[i]);
    }

    // Check 'trigger'
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

    // Check Image Async-Loading
    let asyncImages = [].slice.call(document.querySelectorAll('.j_async_image_load'));
    let asyncImagesNum = asyncImages.length;
    let ASYNC_LOOP_START_INDEX = 0;
    let ASYNC_LOOP_RATE = 30;
    let ASYNC_LOOP_STOP_INDEX = 30;
    let DEFS = [];
    let asyncLoader = (wrapperDOM:HTMLElement) => {
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
              loadedImg.setAttribute(
                'src',
                'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACAAQMAAAD58POIAAAABlBMVEUAAAAAFx8t7DCsAAAAAXRSTlMAQObYZgAAACdJREFUSMdj+A8EDEjkqMCoADI5ClDAoImXUYHBKTAKRvPLqADRAgAGUnu9KI2EPgAAAABJRU5ErkJggg=='
              );
              resolve();
            },
            false
          );
          tmpImg.setAttribute('src', wrapperDOM.getAttribute('data-async-src'));
        }
      );
    }
    let asyncLoad = () => {
      DEFS = []
      let asyncLoadImages = asyncImages.slice(ASYNC_LOOP_START_INDEX, ASYNC_LOOP_STOP_INDEX);
      for(var i = 0, il = asyncLoadImages.length; i < il; i++){
        DEFS.push(asyncLoader(asyncLoadImages[i]));
      }
      Promise.all(DEFS)
        .then(
          () => {
            ASYNC_LOOP_START_INDEX = ASYNC_LOOP_START_INDEX + ASYNC_LOOP_RATE;
            ASYNC_LOOP_STOP_INDEX = ASYNC_LOOP_START_INDEX + ASYNC_LOOP_RATE;
            if(ASYNC_LOOP_START_INDEX >= asyncImagesNum){
              console.log('All Images Downloaded');
            }else{
              var asyncLoadStatus = Math.ceil((ASYNC_LOOP_START_INDEX / asyncImagesNum) * 100);
              if(asyncLoadStatus >= 80){
                asyncLoadStatus = 79;
              }
              console.log('Image Loading Status : [ ' + asyncLoadStatus + ' ]');
              asyncLoad();
            }
          }
        )
    }
    asyncLoad();

    // =============================================================================

    window.addEventListener(
      'popstate',
      (evt:any) => {
        console.dir(evt.state);
      },
      false
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
                    () => {
                      console.warn('>>> Done <<<');
                    }
                  );
              }
            );
        }
      );

  },
  false
);