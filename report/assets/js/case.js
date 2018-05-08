$(function(){
  console.log('++ case ++');
  $('pre code').each(
    function(idx, block){
      hljs.highlightBlock(block);
    }
  );
});