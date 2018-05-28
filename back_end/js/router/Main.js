'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Class
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Main{
  constructor(app){
    this.app = app;
    this.name = 'main';
    this.reportPrefix = '___';
    this.staticReportInfoDir = '../../../report/';
  }
  render(){
    this.app.get(
      '*',
      (req, res) => {
        let baseResponse = {
          path : req.path
        };
        let tmpResponse = {};
        let tmpRequestPath = req.path;
        if(tmpRequestPath.indexOf(this.reportPrefix) !== -1){
          let tmpReportName = tmpRequestPath.replace(this.reportPrefix, '');
          tmpResponse = {
            reportName       : tmpReportName,
            reportDetailInfo : require(this.staticReportInfoDir + 'assets/json/' + tmpReportName + '.json'),
            status           : 1,
            title            : ' - ' + tmpReportName
          }
        }else{
          switch(tmpRequestPath){
            case '/' :
              tmpResponse = {
                reportList : require(this.staticReportInfoDir + 'index.json'),
                status     : 1,
                title      : ''
              }
              break;
            // ToDo - Delete
            case '/test' :
              console.warn('=== TEST ===');
              tmpResponse = {
                reportName       : 'LOCAL-STYLE-SAMPLE',
                reportDetailInfo : require(this.staticReportInfoDir + 'assets/json/LOCAL-STYLE-SAMPLE.json'),
                status           : 0,
                title            : ' - ' + 'LOCAL-STYLE-SAMPLE'
              }
              break;
            default:
              tmpResponse = {
                status : 0,
                title  : ' - Error'
              }
              break;
          }
        }
        res.render(this.name, Object.assign(baseResponse, tmpResponse));
      }
    );
  }
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Export
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
module.exports = Main;