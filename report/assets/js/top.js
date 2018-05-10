$(function(){
  var reportLinkRoot = $('#l_content__report_table');
  var loading = $('#loading__bg');
  var loadingStatus = $('#loading__status');
  var reportResultEmptyDOM = document.createDocumentFragment();
  var currentLoadingStatus = 0;
  var updateLoadingStatus = function(status){
    var dfd = new $.Deferred();
    var buffer = status * 40;
    setTimeout(
      function(){
        loadingStatus.text(status + '%').attr('data-text', status + '%');
        dfd.resolve();
      },
      buffer
    );
    return dfd.promise();
  };
  var loadingHandler = function(status){
    var dfd = new $.Deferred();
    var defs = [];
    if(currentLoadingStatus !== 0){
      for(var i = currentLoadingStatus; i <= status; i++){
        defs.push(updateLoadingStatus(i));
      }
    }else{
      for(var i = 1; i <= status; i++){
        defs.push(updateLoadingStatus(i));
      }
    }
    $.when.apply($, defs).done(
      function(){
        currentLoadingStatus = status;
        if(currentLoadingStatus === 100){
          setTimeout(
            function(){
              dfd.resolve();
            },
            1.2
          );
        }else{
          dfd.resolve();
        }
      }
    );
    return dfd.promise();
  };
  // Init
  $.ajax(
    {
      url      : '/index.json',
      type     : 'GET',
      dataType : 'json',
    }
  ).then(
    function(result){
      loadingHandler(60).then(
        function(){
          var tmpResultInfo = null;
          for(var i = 0, il = result.length; i < il; i++){
            tmpResultInfo = result[i];
            reportResultEmptyDOM.appendChild(
              $(
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
              ).get(0)
            );
          }
          reportLinkRoot.get(0).appendChild(reportResultEmptyDOM);
          loadingHandler(80).then(
            function(){
              loadingHandler(100).then(
                function(){
                  loading.addClass('___loaded');
                }
              );
            }
          );
        }
      );
    },
    function(){
      // ToDo
    }
  );
});