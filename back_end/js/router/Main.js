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