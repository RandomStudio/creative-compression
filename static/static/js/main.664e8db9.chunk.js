(this.webpackJsonpui=this.webpackJsonpui||[]).push([[0],{15:function(e,t,n){},17:function(e,t,n){},18:function(e,t,n){"use strict";n.r(t);var c=n(0),r=n(1),a=n.n(r),i=n(9),s=n.n(i),u=(n(15),n(2)),o=n.n(u),l=n(4),h=n(3),d=(n(17),function(e){var t=e.API_URL,n=e.resetState,r=e.setImageFilename,a=e.setIsLoading,i=function(){var e=Object(l.a)(o.a.mark((function e(c){var i,s,u;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a(!0),n(),e.prev=2,e.next=5,fetch(t+"/upload",{method:"POST",body:c.target.files[0]});case 5:return i=e.sent,e.next=8,i.json();case 8:s=e.sent,u=s.filename,r(u),e.next=16;break;case 13:e.prev=13,e.t0=e.catch(2),console.error(e.t0);case 16:a(!1),c.preventDefault();case 18:case"end":return e.stop()}}),e,null,[[2,13]])})));return function(t){return e.apply(this,arguments)}}();return Object(c.jsxs)("div",{className:"uploader",children:[Object(c.jsx)("label",{for:"upload",children:"Load image"}),Object(c.jsx)("input",{id:"upload",onChange:i,type:"file"})]})}),b=function(e){var t=e.savedShapes,n=e.shapeVisibilities,r=e.setSavedShapes,a=e.setShapeVisibilities,i=n.some((function(e){return!1!==e}));return Object(c.jsxs)(c.Fragment,{children:[n.map((function(e,i){return Object(c.jsxs)("div",{className:"row",children:[Object(c.jsxs)("p",{className:"row-title",children:["Box ",i]}),Object(c.jsx)("button",{onClick:function(){return function(e){r(t.map((function(t,n){return e!==n&&t})).filter((function(e){return e}))),a(n.map((function(t,n){return e===n?null:t})).filter((function(e){return null!==e})))}(i)},children:"Delete"})]})})),Object(c.jsxs)("div",{className:"row options",children:[Object(c.jsx)("input",{type:"checkbox",checked:i,onChange:function(){a(n.map((function(e){return!i})))}}),"Toggle guides"]})]})},f=n(8),j=function(e){var t=e.canvasRef,n=e.imageFilename,a=e.savedShapes,i=e.shapeVisibilities,s=e.setIsLoading,u=e.setSavedShapes,d=e.setShapeVisibilities,b=Object(r.useRef)([0,0,0,0]),j=Object(r.useState)(!1),p=Object(h.a)(j,2),v=p[0],O=p[1],g=Object(r.useState)(null),m=Object(h.a)(g,2),x=m[0],S=m[1];Object(r.useEffect)((function(){if(n){s(!0);var e=new Image;e.src=a.length>0?"".concat("","/composition/preview_").concat(n,"?boxes=").concat(JSON.stringify(a),"&width=").concat(t.current.width):"".concat("","/static/uploads/preview_").concat(n),e.decoding="async",e.decode().then((function(){O(e.width<e.height),s(!1),S(e)}))}}),[t,n,a,s]);var w=Object(r.useState)(null),k=Object(h.a)(w,2),y=k[0],C=k[1],I=Object(r.useCallback)(function(){var e=Object(l.a)(o.a.mark((function e(n){return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(x){e.next=2;break}return e.abrupt("return");case 2:x.width>x.height?(O(!1),t.current.width=t.current.clientWidth,t.current.height=t.current.clientWidth/x.width*x.height):(O(!0),t.current.height=t.current.clientHeight,t.current.width=t.current.clientHeight/x.height*x.width),n.drawImage(x,0,0,t.current.width,t.current.height);case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),[t,x]),N=Object(r.useCallback)((function(e){a.map((function(t,n){var c=Object(h.a)(t,4),r=c[0],a=c[1],s=c[2],u=c[3];return!!i[n]&&(e.strokeStyle="blue",e.strokeRect(r,a,s,u),!0)}))}),[a,i]),L=Object(r.useCallback)(function(){var e=Object(l.a)(o.a.mark((function e(n){var c;return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(n||t.current){e.next=2;break}return e.abrupt("return");case 2:(c=null!==n&&void 0!==n?n:t.current.getContext("2d")).clearRect(0,0,t.current.width,t.current.height),I(c),N(c);case 6:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),[t,I,N]);Object(r.useEffect)((function(){L()}),[L,a,i]);var R=function(e,n){var c=t.current.getBoundingClientRect();return{x:e-c.left,y:n-c.top}},F=function(e){C(null),0!==!b.current[2]&&0!==b.current[3]&&(u((function(e){return[].concat(Object(f.a)(e),[b.current])})),d((function(e){return[].concat(Object(f.a)(e),[!0])})))};return Object(c.jsx)("canvas",{className:"canvas ".concat(v?"is-vertical":""),onMouseDown:function(e){var n=t.current.getContext("2d");C(n);var c=R(e.clientX,e.clientY);b.current=[c.x,c.y,0,0]},onMouseUp:F,onMouseLeave:function(){y&&F()},onMouseMove:function(e){if(y){L(y);var t=Object(h.a)(b.current,2),n=t[0],c=t[1],r=R(e.clientX,e.clientY),a=r.x-n,i=r.y-c;y.strokeStyle="blue",y.strokeRect(n,c,a,i),b.current=[n,c,a,i]}},ref:t})};var p=function(){var e,t=Object(r.useRef)(),n=Object(r.useState)(null),a=Object(h.a)(n,2),i=a[0],s=a[1],u=Object(r.useState)(!1),f=Object(h.a)(u,2),p=f[0],v=f[1],O=Object(r.useState)([]),g=Object(h.a)(O,2),m=g[0],x=g[1],S=Object(r.useState)([]),w=Object(h.a)(S,2),k=w[0],y=w[1],C=function(){var e=Object(l.a)(o.a.mark((function e(t){return o.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:s(null),x([]),y([]);case 3:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}();return Object(c.jsxs)("div",{className:"page",children:[Object(c.jsxs)("div",{className:"main",children:[Object(c.jsx)(j,{canvasRef:t,imageFilename:i,savedShapes:m,shapeVisibilities:k,setIsLoading:v,setSavedShapes:x,setShapeVisibilities:y}),p&&Object(c.jsx)("div",{className:"loader"})]}),Object(c.jsxs)("div",{className:"sidebar",children:[Object(c.jsx)(b,{shapeVisibilities:k,setShapeVisibilities:y,savedShapes:m,setSavedShapes:x}),Object(c.jsx)(d,{API_URL:"",resetState:C,setImageFilename:s,setIsLoading:v}),Object(c.jsx)("a",{href:"".concat("","/composition/").concat(i,"?boxes=").concat(JSON.stringify(m),"&width=").concat(null===t||void 0===t||null===(e=t.current)||void 0===e?void 0:e.width),target:"_blank",className:"downloader",children:"Save high quality"})]})]})},v=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,19)).then((function(t){var n=t.getCLS,c=t.getFID,r=t.getFCP,a=t.getLCP,i=t.getTTFB;n(e),c(e),r(e),a(e),i(e)}))};s.a.render(Object(c.jsx)(a.a.StrictMode,{children:Object(c.jsx)(p,{})}),document.getElementById("root")),v()}},[[18,1,2]]]);
//# sourceMappingURL=main.664e8db9.chunk.js.map