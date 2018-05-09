$(function(){
  console.log('++ case ++');
  // Test
  $.ajax(
    {
      type     : 'GET',
      url      : '/assets/json/' + window.CONFIG_KEY + '.json',
      dataType : 'json'
    }
  ).then(
    function(result){
      console.dir(result);
    },
    function(err){
      console.error(err);
    }
  );
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
});