$(function(){
  // Init - [ Highlight ]
  $('pre code').each(
    function(idx, block){
      hljs.highlightBlock(block);
    }
  );
  // Init - [ Digest Toggle ]
  var digestTriggerStack = {};
  var digestTriggers = $('.j_digest_detail_trigger');
  var digestToggleAreas = $('.j_toggle');
  digestToggleAreas.each(
    function(idx, digest){
      digestTriggerStack[$(digest).attr('data-target-url')] = $(digest);
    }
  );
  digestTriggers.each(
    function(idx, trigger){
      $(trigger).on(
        'click',
        function(){
          digestTriggerStack[$(this).attr('data-target-url')].slideToggle()
        }
      )
    }
  );
  // Init - Async Load
  var asyncImages = $('.j_async_image_load').toArray();
  var asyncImagesNum = asyncImages.length;
  console.warn('Total Image [ ' + asyncImagesNum + ' ]');
  var ASYNC_LOOP_START_INDEX = 0;
  var ASYNC_LOOP_STOP_INDEX = ASYNC_LOOP_RATE = 30;
  var DEFS = [];
  var asyncLoader = function(wrapperDOM){
    var dfd = new $.Deferred();
    var tmpImg = $(document.createElement('img'));
    wrapperDOM.append(tmpImg);
    tmpImg.on(
      'load',
      function(){
        var loadedImg = $(this);
        loadedImg.addClass('___loaded');
        dfd.resolve();
      }
    );
    tmpImg.on(
      'error',
      function(){
        var loadedImg = $(this);
        loadedImg
          .addClass('___error')
          .attr(
            'src',
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACAAQMAAAD58POIAAAABlBMVEUAAAAAFx8t7DCsAAAAAXRSTlMAQObYZgAAACdJREFUSMdj+A8EDEjkqMCoADI5ClDAoImXUYHBKTAKRvPLqADRAgAGUnu9KI2EPgAAAABJRU5ErkJggg=='
          )
        dfd.resolve();
      }
    )
    tmpImg.attr('src', wrapperDOM.attr('data-async-src'));
    return dfd.promise();
  }
  var asyncLoad = function(){
    DEFS = []
    var asyncLoadImages = asyncImages.slice(ASYNC_LOOP_START_INDEX, ASYNC_LOOP_STOP_INDEX);
    for(var i = 0, il = asyncLoadImages.length; i < il; i++){
      DEFS.push(asyncLoader($(asyncLoadImages[i])));
    }
    $.when.apply($, DEFS).done(
      function(){
        ASYNC_LOOP_START_INDEX = ASYNC_LOOP_START_INDEX + ASYNC_LOOP_RATE;
        ASYNC_LOOP_STOP_INDEX = ASYNC_LOOP_START_INDEX + ASYNC_LOOP_RATE;
        if(ASYNC_LOOP_START_INDEX >= asyncImagesNum){
          console.log('All Images Downloaded');
        }else{
          asyncLoad();
        }
      }
    );
  }
  asyncLoad();
});