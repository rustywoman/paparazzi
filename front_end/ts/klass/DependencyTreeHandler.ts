/**
 * @author      rustywoman
 * @description Custom Declarration - [ d3 ]
 * @type        {any}
 */
declare let d3:any;
export default class DependencyTreeHandler{
  totalNodes     : number;
  maxLabelLength : number;
  selectedNode   : any;
  panSpeed       : any;
  panTimer       : any;
  idx            : number;
  duration       : number;
  nodeBuffer     : number;
  root           : any;
  treeJSON       : any;
  viewerWidth    : number;
  viewerHeight   : number;
  tree           : any;
  diagonal       : any;
  zoomListener   : any;
  baseSvg        : any;
  svgGroup       : any;
  detailDOM      : any;
  selectedId     : number;
  constructor(){
    this.totalNodes = 0;
    this.maxLabelLength = 0;
    this.selectedNode = null;
    this.panSpeed = 200;
    this.panTimer = null;
    this.idx = 0;
    this.duration = 750;
    this.nodeBuffer = 85;
    this.root = null;
    this.treeJSON = null;
    this.viewerWidth = window.innerWidth - 15;
    this.viewerHeight = window.innerHeight - 60 - 40 - 4;
    this.tree = d3.layout.tree().size([this.viewerHeight, this.viewerWidth]);
    this.diagonal = d3.svg.diagonal().projection(
      (d:any) => {
        return [d.y, d.x];
      }
    );
    this.zoomListener = null;
    this.baseSvg = null;
    this.svgGroup = null;
    this.detailDOM = null;
    this.selectedId = 0;
  };
  traceBranch(parent:any, traceBranchFn:any, childrenFn:any){
    if(!parent){
      return;
    }
    traceBranchFn(parent);
    let children = childrenFn(parent);
    if(children){
      for(let i = 0, il = children.length; i < il; i++){
        this.traceBranch(children[i], traceBranchFn, childrenFn);
      }
    }
  };
  sortTree(){
    this.tree.sort(
      (a:any, b:any) => {
        return b.name.toLowerCase() < a.name.toLowerCase() ? 1 : -1;
      }
    );
  };
  pan(domNode:any, direction:string){
    if(this.panTimer){
      clearTimeout(this.panTimer);
      let translateCoords = d3.transform(this.svgGroup.attr('transform'));
      let translateX = 0;
      let translateY = 0;
      if(direction == 'left' || direction == 'right'){
        translateX = direction == 'left' ? translateCoords.translate[0] + this.panSpeed : translateCoords.translate[0] - this.panSpeed;
        translateY = translateCoords.translate[1];
      }else if(direction == 'up' || direction == 'down'){
        translateX = translateCoords.translate[0];
        translateY = direction == 'up' ? translateCoords.translate[1] + this.panSpeed : translateCoords.translate[1] - this.panSpeed;
      }
      let scaleX = translateCoords.scale[0];
      let scaleY = translateCoords.scale[1];
      let scale = this.zoomListener.scale();
      this.svgGroup.transition().attr('transform', 'translate(' + translateX + ',' + translateY + ') scale(' + scale + ')');
      d3.select(domNode).select('g.node').attr('transform', 'translate(' + translateX + ',' + translateY + ')');
      this.zoomListener.scale(this.zoomListener.scale());
      this.zoomListener.translate([translateX, translateY]);
      this.panTimer = setTimeout(
        () => {
          this.pan(domNode, direction);
        },
        50
      );
    }
  };
  handleZoom(){
    this.svgGroup.attr('transform', 'translate(' + d3.event.translate + ') scale(' + d3.event.scale + ')');
  };
  centerNode(source:any){
    let scale = this.zoomListener.scale();
    let x = -source.y0;
    let y = -source.x0;
    x = x * scale + (this.viewerWidth / 4);
    y = y * scale + this.viewerHeight / 2;
    d3.select('g')
      .transition()
      .duration(this.duration)
      .attr('transform', 'translate(' + x + ',' + y + ') scale(' + scale + ')');
    this.zoomListener.scale(scale);
    this.zoomListener.translate([x, y]);
  };
  toggleChildren(d:any){
    if(d.children){
      d._children = d.children;
      d.children = null;
    }else if(d._children){
      d.children = d._children;
      d._children = null;
    }
    return d;
  };
  traceAncestor(d:any, ancestorResult:any[], relatedIdResult:any[]){
    ancestorResult.push(d['parent']['name']);
    relatedIdResult.push(d['id']);
    relatedIdResult.push(d['parent']['id']);
    if(d['parent']['parent']){
      this.traceAncestor(d['parent'], ancestorResult, relatedIdResult);
    }
    return {
      'ancestorResult' : ancestorResult,
      'relatedResult'  : relatedIdResult
    };
  };
  handleClick(d:any){
    if(d3.event.defaultPrevented){
      return;
    }
    this.selectedId = d.id;
    let tmpNodes = this.toggleChildren(d);
    this.update(tmpNodes);
    this.centerNode(tmpNodes);
    // Dynamic Info. - ToDo
    document.querySelector('#l_tree_target').innerHTML = d.name;
    let tmpAncestorInfo = this.traceAncestor(d, [], []);
    let tmpRelatedPathIds = tmpAncestorInfo['relatedResult'];
    let allVisibleLinks = document.querySelectorAll('.m_svg_dependency__link');
    for(let i = 0, il = allVisibleLinks.length; i < il; i++){
      allVisibleLinks[i].classList.remove('___marker');
    }
    for(let i = 0, il = tmpRelatedPathIds.length; i < il; i++){
      let tmpPath = document.querySelector('#l_path_' + tmpRelatedPathIds[i]);
      if(tmpPath){
        tmpPath.classList.add('___marker');
      }
    }
    let tmpAncestor = tmpAncestorInfo['ancestorResult'].reverse();
    let tmpAncestorListDOM = [];
    for(let i = 0, il = tmpAncestor.length; i < il; i++){
      tmpAncestorListDOM.push('<li class="m_tree_ancestor__list--item">' + tmpAncestor[i] + '</li>');
    }
    document.querySelector('#l_tree_ancestor__list').innerHTML = tmpAncestorListDOM.join('');
  };
  update(source:any){
    let levelWidth = [1];
    let childCount = (level:any, n:any) => {
      if(n.children && n.children.length > 0){
        if(levelWidth.length <= level + 1){
          levelWidth.push(0);
        }
        levelWidth[level + 1] += n.children.length;
        n.children.forEach(
          (d:any) => {
            childCount(level + 1, d);
          }
        );
      }
    };
    childCount(0, this.root);
    let newHeight = d3.max(levelWidth) * this.nodeBuffer;
    this.tree = this.tree.size([newHeight, this.viewerWidth]);
    let nodes = this.tree.nodes(this.root).reverse();
    let links = this.tree.links(nodes);
    nodes.forEach(
      (d:any) => {
        d.y = (d.depth * (this.maxLabelLength * 15));
      }
    );
    let node = this.svgGroup.selectAll('g.m_svg_dependency__node')
      .data(
        nodes,
        (d:any) => {
          return d.id || (d.id = ++this.idx);
        }
      );
    let nodeEnter = node.enter().append('g')
      .attr('class', 'm_svg_dependency__node')
      .attr(
        'transform',
        (d:any) => {
          return 'translate(' + source.y0 + ',' + source.x0 + ')';
        }
      )
      .on('click', this.handleClick.bind(this));
    nodeEnter.append('circle')
      .attr('class', 'm_svg_dependency__circle')
      .attr('r', 0)
      .style(
        'fill',
        (d:any) => {
          return d._children ? '#444' : '#fff';
        }
      );
    nodeEnter.append('text')
      .attr(
        'dx',
        (d:any) => {
          return d.children || d._children ? '' : '.7em';
        }
      )
      .attr(
        'dy',
        (d:any) => {
          return d.children || d._children ? '1.5em' : '.35em';
        }
      )
      .attr('class', 'm_svg_dependency__text')
      .attr(
        'text-anchor',
        (d:any) => {
          return d.children || d._children ? 'middle' : 'start';
        }
      )
      .text(
        (d:any) => {
          return d.name;
        }
      )
      .style('fill-opacity', 0);
    node.select('text')
      .attr(
        'class',
        (d:any) => {
          return d.id === this.selectedId ? '___marker' : '';
        }
      )
      .attr(
        'text-anchor',
        (d:any) => {
          return d.children || d._children ? 'middle' : 'start';
          // return 'middle';
        }
      )
      .text(
        (d:any) => {
          return d.name;
        }
      );
    node.select('circle.m_svg_dependency__circle')
      .attr('r', 4.8)
      .style(
        'fill',
        (d:any) => {
          return d._children ? '#444' : '#fff';
        }
      );
    let nodeUpdate = node.transition()
      .duration(this.duration)
      .attr(
        'transform',
        (d:any) => {
          return 'translate(' + d.y + ',' + d.x + ')';
        }
      );
    nodeUpdate.select('text').style('fill-opacity', 1);
    let nodeExit = node.exit().transition()
      .duration(this.duration)
      .attr(
        'transform',
        (d:any) => {
          return 'translate(' + source.y + ',' + source.x + ')';
        }
      )
      .remove();
    nodeExit.select('circle').attr('r', 0);
    nodeExit.select('text').style('fill-opacity', 0);
    let link = this.svgGroup.selectAll('path.m_svg_dependency__link')
      .data(
        links,
        (d:any) => {
          return d.target.id;
        }
      );
    link.enter().insert('path', 'g')
      .attr('class', 'm_svg_dependency__link')
      .attr(
        'id',
        (d:any) => {
          return 'l_path_' + d.target.id;
        }
      )
      .attr(
        'd',
        (d:any) => {
          let o = {
            x : source.x0,
            y : source.y0
          };
          return this.diagonal(
            {
              source : o,
              target : o
            }
          );
        }
      );
    link.transition()
      .duration(this.duration)
      .attr('d', this.diagonal);
    link.exit().transition()
      .duration(this.duration)
      .attr(
        'd',
        (d:any) => {
          let o = {
            x : source.x,
            y : source.y
          };
          return this.diagonal(
            {
              source : o,
              target : o
            }
          );
        }
      )
      .remove();
    nodes.forEach(
      (d:any) => {
        d.x0 = d.x;
        d.y0 = d.y;
      }
    );
  };
  init(wrapperDOMSelector:string, detailDOMSelector:string, treeDependencyData:string){
    let treeDOM = document.querySelector(wrapperDOMSelector);
    this.detailDOM = document.querySelector(detailDOMSelector);
    return new Promise(
      (resolve:any, reject:any) => {
        this.treeJSON = d3.json(
          treeDependencyData + '.json',
          (error:any, treeData:any) => {
            this.traceBranch(
              treeData,
              (d:any) => {
                this.totalNodes++;
                this.maxLabelLength = Math.max(d.name.length, this.maxLabelLength);
              },
              (d:any) => {
                return d.children && d.children.length > 0 ? d.children : null;
              }
            );
            this.sortTree();
            this.zoomListener = d3.behavior.zoom().scaleExtent([1, 2.4]).on('zoom', this.handleZoom.bind(this));
            this.baseSvg = d3
              .select(wrapperDOMSelector)
              .append('svg')
              .attr('width', this.viewerWidth)
              .attr('height', this.viewerHeight)
              .call(this.zoomListener);
            this.svgGroup = this.baseSvg.append('g');
            this.root = treeData;
            this.root.x0 = this.viewerHeight / 2;
            this.root.y0 = 0;
            this.update(this.root);
            this.centerNode(this.root);
            resolve();
          }
        );
      }
    );
  };
};