'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const fs = require('fs');
const path = require('path');


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Class
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Main{
  constructor(app, version){
    this.app = app;
    this.version = version;
    this.name = 'main';
    this.reportPrefix = '___';
    this.staticReportInfoDir = path.join(__dirname, '../../../report/');
  }
  render(){
    this.app.get(
      '*',
      (req, res) => {
        let baseResponse = {
          path    : req.path,
          version : this.version
        };
        let tmpResponse = {};
        let tmpRequestPath = req.path;
        if(tmpRequestPath.indexOf(this.reportPrefix) !== -1){
          let tmpReportName = tmpRequestPath.replace(this.reportPrefix, '');
          tmpResponse = {
            reportName       : tmpReportName,
            reportDetailInfo : JSON.parse(
              fs.readFileSync(
                this.staticReportInfoDir + 'assets/json/' + tmpReportName + '.json',
                'utf8'
              )
            ),
            status           : 1,
            title            : ' - ' + tmpReportName
          }
        }else{
          switch(tmpRequestPath){
            case '/' :
              tmpResponse = {
                reportList       : JSON.parse(
                  fs.readFileSync(
                    this.staticReportInfoDir + 'index.json',
                    'utf8'
                  )
                ),
                reportDetailInfo : null,
                status           : 1,
                title            : ''
              }
              break;
            default:
              tmpResponse = {
                reportDetailInfo : null,
                status           : 0,
                title            : ' - Error'
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