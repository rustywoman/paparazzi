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
  $('.j_async_image_load').each(
    function(idx, imgWrapper){
      var tmpImg = $(document.createElement('img'));
      $(imgWrapper).append(tmpImg);
      tmpImg.on(
        'load',
        function(){
          tmpImg.addClass('___loaded');
        }
      );
      tmpImg.attr('src', $(imgWrapper).attr('data-async-src'));
    }
  )
});