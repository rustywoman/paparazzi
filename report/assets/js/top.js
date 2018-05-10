$(function(){
  var reportLinkRoot = $('#l_content__report_table');
  var reportResultEmptyDOM = document.createDocumentFragment();
  $.ajax(
    {
      url      : '/index.json',
      type     : 'GET',
      dataType : 'json',
    }
  ).then(
    function(result){
      var tmpResultInfo = null;
      for(var i = 0, il = result.length; i < il; i++){
        tmpResultInfo = result[i];
        reportResultEmptyDOM.appendChild(
          $(
            [
              '<div class="m_content__report_table__row">',
                '<div class="m_content__report_table__cell">',
                  '<a class="marker" href="' + tmpResultInfo['path'] +  '">',
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
    },
    function(){
      // ToDo
    }
  );
});