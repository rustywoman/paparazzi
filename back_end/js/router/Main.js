'use strict';


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Load Module
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
const fs = require('fs');
const path = require('path');
const exec = require('child_process').exec;


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// Class
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
class Main{
  constructor(app, version, prodFlg){
    this.app = app;
    this.version = version;
    this.prodFlg = prodFlg;
    this.name = 'main';
    this.reportPrefix = '___';
    this.reportSuffix = '_report';
    this.mainSuffix = '_main';
    this.multiSuffix = '_multi';
    this.scanSuffix = '_scan';
    this.searchSuffix = '_search';
    this.staticReportInfoDir = path.join(__dirname, '../../../report/');
    this.caseInfoDir = path.join(__dirname, '../../../case/');
  }
  render(){
    this.app.post(
      '/execute',
      (req, res) => {
        res.header('Content-Type', 'application/json; charset=utf-8');
        let caseName = req.body['name'];
        console.info('=== [ API : execute ] - ' + caseName + ' - start ===');
        exec(
          'sh report_via_node.sh ' + this.reportPrefix + caseName + this.reportSuffix,
          // ToDo - Test
          // 'sh report_via_node.sh local_sample_report',
          (err, stdout, stderr) => {
            if(err){
              console.error('=== [ API : execute ] - ' + caseName + ' - ng end ===');
              res.send(
                {
                  status    : 0,
                  reportURL : this.reportPrefix + caseName,
                  error     : err
                }
              );
            }else{
              console.error('=== [ API : execute ] - ' + caseName + ' - ok end ===');
              res.send(
                {
                  status    : 1,
                  reportURL : this.reportPrefix + caseName,
                  error     : ''
                }
              );
            }
          }
        );
      }
    );
    this.app.post(
      '/create',
      (req, res) => {
        res.header('Content-Type', 'application/json; charset=utf-8');
        let caseName = req.body['name'];
        let caseURL = req.body['url'];
        let caseDetail = {
          'name' : caseName,
          'url'  : caseURL
        };
        console.info('=== [ API : create ] - ' + caseName + ' - start ===');
        fs.writeFile(
          this.caseInfoDir + this.reportPrefix + caseName + this.reportSuffix + '.json',
          JSON.stringify(caseDetail),
          (err) => {
            if(err){
              console.error('=== [ API : create ] - ' + caseName + ' - ng end ===');
              res.send(
                {
                  status : 0
                }
              );
            }else{
              console.info('=== [ API : create ] - ' + caseName + ' - ok end ===');
              res.send(
                {
                  status : 1
                }
              );
            }
          }
        );
      }
    );
    this.app.get(
      '*',
      (req, res) => {
        let baseResponse = {
          path    : req.path,
          version : this.version,
          prodFlg : this.prodFlg
        };
        let tmpResponse = {};
        let tmpRequestPath = req.path;
        if(tmpRequestPath.indexOf(this.reportPrefix) !== -1){
          try{
            let tmpReportName = tmpRequestPath.replace(this.reportPrefix, '');
            let tmpTemplateType = '';
            // "***_report"
            if(tmpRequestPath.indexOf(this.reportSuffix) !== -1){
              tmpTemplateType = 'report';
            }
            // "***_main"
            if(tmpRequestPath.indexOf(this.mainSuffix) !== -1){
              tmpTemplateType = 'main';
            }
            // "***_multi"
            if(tmpRequestPath.indexOf(this.multiSuffix) !== -1){
              tmpTemplateType = 'multi';
            }
            // "***_scan"
            if(tmpRequestPath.indexOf(this.scanSuffix) !== -1){
              tmpTemplateType = 'scan';
            }
            // "***_search"
            if(tmpRequestPath.indexOf(this.searchSuffix) !== -1){
              tmpTemplateType = 'search';
            }
            tmpResponse = {
              reportName       : tmpReportName,
              reportDetailInfo : JSON.parse(
                fs.readFileSync(
                  this.staticReportInfoDir + 'assets/json/' + tmpReportName + '.json',
                  'utf8'
                )
              ),
              status           : 1,
              title            : ' - ' + tmpReportName,
              templateType     : tmpTemplateType
            }
          }catch(ex){
            tmpResponse = {
              reportDetailInfo : null,
              status           : 0,
              title            : ' - Error'
            }
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