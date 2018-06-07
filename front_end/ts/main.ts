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
/**
 * @author      rustywoman
 * @description Custom Declarration - [ d3 ]
 * @type        {any}
 */
declare let d3:any;


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
  contentRootDOM         : HTMLElement;
  DOM_PARSER_INS         : any;
  ASYNC_LOOP_START_INDEX : number;
  ASYNC_LOOP_RATE        : number;
  ASYNC_LOOP_STOP_INDEX  : number;
  /**
   * @constructor Main
   * @param    {object} customLoadingIns       - Instance Of `LoadingHandler` class
   * @param    {object} markerHandlerIns       - Instance Of `MarkerHandler` class
   * @param    {object} contentRootDOM         - Content Root raw DOM
   * @property {object} customLoadingIns       - Instance Of `LoadingHandler` class
   * @property {object} markerHandlerIns       - Instance Of `MarkerHandler` class
   * @property {object} contentRootDOM         - Content Root raw DOM
   * @property {object} DOM_PARSER_INS         - DOM raw Parser
   * @property {number} ASYNC_LOOP_START_INDEX - Async Load Start Index For Image
   * @property {number} ASYNC_LOOP_RATE        - Async Load Unit For Image
   * @property {number} ASYNC_LOOP_STOP_INDEX  - Async Load Stop Index For Image
   */
  constructor(customLoadingIns:LoadingHandler, markerHandlerIns:MarkerHandler, contentRootDOM:HTMLElement){
    this.customLoadingIns = customLoadingIns;
    this.markerHandlerIns = markerHandlerIns;
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
                        console.warn('>>> Done [ Initial Access ] without images <<<');
                      }
                    );
                }
              );
          }
        );
    }
  };
};


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

    let treeJSON = d3.json(
      'flare.json',
      (error:any, treeData:any) => {
        let totalNodes = 0;
        let maxLabelLength = 0;
        let selectedNode = null;
        let panSpeed = 200;
        let panTimer:any = null;
        let i = 0;
        let duration = 750;
        let root:any = null;
        let viewerWidth = window.innerWidth;
        let viewerHeight = window.innerHeight - 60 - 40;
        let tree = d3.layout.tree().size([viewerHeight, viewerWidth]);
        let diagonal = d3.svg.diagonal().projection(
          (d:any) => {
            return [d.y, d.x];
          }
        );
        function visit(parent:any, visitFn:any, childrenFn:any){
            if (!parent) return;
            visitFn(parent);
            let children = childrenFn(parent);
            if(children){
              let count = children.length;
              for(let i = 0; i < count; i++){
                visit(children[i], visitFn, childrenFn);
              }
            }
        };
        visit(
          treeData,
          function(d:any){
            totalNodes++;
            maxLabelLength = Math.max(d.name.length, maxLabelLength);
          },
          function(d:any){
            return d.children && d.children.length > 0 ? d.children : null;
          }
        );


        function sortTree(){
          tree.sort(
            (a:any, b:any) => {
              return b.name.toLowerCase() < a.name.toLowerCase() ? 1 : -1;
            }
          );
        };
        sortTree();


        function pan(domNode:any, direction:any){
          let speed = panSpeed;
          if(panTimer){
            clearTimeout(panTimer);
            let translateCoords = d3.transform(svgGroup.attr('transform'));
            let translateX = 0;
            let translateY = 0;
            if(direction == 'left' || direction == 'right'){
              translateX = direction == 'left' ? translateCoords.translate[0] + speed : translateCoords.translate[0] - speed;
              translateY = translateCoords.translate[1];
            }else if (direction == 'up' || direction == 'down'){
              translateX = translateCoords.translate[0];
              translateY = direction == 'up' ? translateCoords.translate[1] + speed : translateCoords.translate[1] - speed;
            }
            let scaleX = translateCoords.scale[0];
            let scaleY = translateCoords.scale[1];
            let scale = zoomListener.scale();
            svgGroup.transition().attr('transform', 'translate(' + translateX + ',' + translateY + ')scale(' + scale + ')');
            d3.select(domNode).select('g.node').attr('transform', 'translate(' + translateX + ',' + translateY + ')');
            zoomListener.scale(zoomListener.scale());
            zoomListener.translate([translateX, translateY]);
            panTimer = setTimeout(function() {
              pan(domNode, direction);
            }, 50);
          }
        };
        function zoom(){
          svgGroup.attr('transform', 'translate(' + d3.event.translate + ')scale(' + d3.event.scale + ')');
        };
        let zoomListener = d3.behavior.zoom().scaleExtent([1, 3.8]).on('zoom', zoom);


        let baseSvg = d3
          .select('#tree-container')
          .append('svg')
          .attr('id', 'xxx')
          .attr('width', viewerWidth)
          .attr('height', viewerHeight)
          .call(zoomListener);

        function centerNode(source:any){
          let scale = zoomListener.scale();
          let x = -source.y0;
          let y = -source.x0;
          x = x * scale + viewerWidth / 2;
          y = y * scale + viewerHeight / 2;
          d3.select('g').transition()
            .duration(duration)
            .attr('transform', 'translate(' + x + ',' + y + ')scale(' + scale + ')');
          zoomListener.scale(scale);
          zoomListener.translate([x, y]);
        };
        function toggleChildren(d:any){
          if(d.children){
            d._children = d.children;
            d.children = null;
          }else if(d._children){
            d.children = d._children;
            d._children = null;
          }
          return d;
        };
        function click(d:any){
          if (d3.event.defaultPrevented) return;
          let tmpNodes = toggleChildren(d);
          update(tmpNodes);
          centerNode(tmpNodes);
        };
        function update(source:any){
          let levelWidth = [1];
          let childCount = (level:any, n:any) => {
            if(n.children && n.children.length > 0){
              if(levelWidth.length <= level + 1) levelWidth.push(0);
              levelWidth[level + 1] += n.children.length;
              n.children.forEach(
                (d:any) => {
                  childCount(level + 1, d);
                }
              );
            }
          };
          childCount(0, root);
          let newHeight = d3.max(levelWidth) * 25;
          tree = tree.size([newHeight, viewerWidth]);
          let nodes = tree.nodes(root).reverse();
          let links = tree.links(nodes);
          nodes.forEach(
            (d:any) => {
              d.y = (d.depth * (maxLabelLength * 10));
            }
          );
          let node = svgGroup.selectAll('g.node')
            .data(
              nodes,
              (d:any) => {
                return d.id || (d.id = ++i);
              }
            );
          let nodeEnter = node.enter().append('g')
            .attr('class', 'node')
            .attr(
              'transform',
              (d:any) => {
                return 'translate(' + source.y0 + ',' + source.x0 + ')';
              }
            )
            .on('click', click);
          nodeEnter.append('circle')
            .attr('class', 'nodeCircle')
            .attr('r', 0)
            .style(
              'fill',
              (d:any) => {
                return d._children ? 'lightsteelblue' : '#fff';
              }
            );
          nodeEnter.append('text')
            .attr(
              'x',
              (d:any) => {
                return d.children || d._children ? -10 : 10;
              }
            )
            .attr('dy', '.35em')
            .attr('class', 'nodeText')
            .attr(
              'text-anchor',
              (d:any) => {
                return d.children || d._children ? 'end' : 'start';
              }
            )
            .text(
              (d:any) => {
                return d.name;
              }
            )
            .style('fill-opacity', 0);
          node.select('text')
            .attr(
              'x',
              (d:any) => {
                return d.children || d._children ? -10 : 10;
              }
            )
            .attr(
              'text-anchor',
              (d:any) => {
                return d.children || d._children ? 'end' : 'start';
              }
            )
            .text(
              (d:any) => {
                return d.name;
              }
            );
          node.select('circle.nodeCircle')
            .attr('r', 4.5)
            .style(
              'fill',
              (d:any) => {
                return d._children ? 'lightsteelblue' : '#fff';
              }
            );
          let nodeUpdate = node.transition()
            .duration(duration)
            .attr(
              'transform',
              (d:any) => {
                return 'translate(' + d.y + ',' + d.x + ')';
              }
            );
          nodeUpdate.select('text').style('fill-opacity', 1);
          let nodeExit = node.exit().transition()
            .duration(duration)
            .attr(
              'transform',
              (d:any) => {
                return 'translate(' + source.y + ',' + source.x + ')';
              }
            )
            .remove();
          nodeExit.select('circle').attr('r', 0);
          nodeExit.select('text').style('fill-opacity', 0);
          let link = svgGroup.selectAll('path.link')
            .data(
              links,
              (d:any) => {
                return d.target.id;
              }
            );
          link.enter().insert('path', 'g')
            .attr('class', 'link')
            .attr(
              'd',
              (d:any) => {
                let o = {
                  x: source.x0,
                  y: source.y0
                };
                return diagonal(
                  {
                    source: o,
                    target: o
                  }
                );
              }
            );
          link.transition()
            .duration(duration)
            .attr('d', diagonal);
          link.exit().transition()
            .duration(duration)
            .attr(
              'd',
              (d:any) => {
                let o = {
                  x: source.x,
                  y: source.y
                };
                return diagonal(
                  {
                    source: o,
                    target: o
                  }
                );
              }
            )
            .remove();
          nodes.forEach(
            (d:any) => {
              d.x0 = d.x;
              d.y0 = d.y;
            }
          );
        };
        let svgGroup = baseSvg.append('g');
        root = treeData;
        root.x0 = viewerHeight / 2;
        root.y0 = 0;
        update(root);
        centerNode(root);
      }
    );
  },
  false
);