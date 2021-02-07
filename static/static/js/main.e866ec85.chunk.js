(this.webpackJsonpui=this.webpackJsonpui||[]).push([[0],{15:function(e,t,n){},17:function(e,t,n){},18:function(e,t,n){"use strict";n.r(t);var c=n(0),r=n(1),a=n.n(r),s=n(9),i=n.n(s),u=(n(15),n(5)),o=n(3),l=n.n(o),d=n(4),b=n(2),j=(n(17),function(e){var t=e.API_URL,n=e.resetState,r=e.setImageFilename,a=e.setIsLoading,s=function(){var e=Object(d.a)(l.a.mark((function e(c){var s,i,u;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return a(!0),n(),e.prev=2,e.next=5,fetch(t+"/upload",{method:"POST",body:c.target.files[0]});case 5:return s=e.sent,e.next=8,s.json();case 8:i=e.sent,u=i.filename,r(u),e.next=16;break;case 13:e.prev=13,e.t0=e.catch(2),console.error(e.t0);case 16:a(!1),c.preventDefault();case 18:case"end":return e.stop()}}),e,null,[[2,13]])})));return function(t){return e.apply(this,arguments)}}();return Object(c.jsxs)("div",{className:"uploader",children:[Object(c.jsx)("label",{htmlFor:"upload",children:"Load image"}),Object(c.jsx)("input",{id:"upload",onChange:s,type:"file"})]})}),h=function(e){var t=e.deleteShape,n=e.distances,r=e.hasVisibleBorders,a=e.savedShapes,s=e.setDistances,i=e.setHasVisibleBorders,o=e.setSteps,l=e.setSpeeds,d=e.speeds,b=e.steps,j=function(e,t,n){e&&n((function(n){return n[t]=Math.max(1,parseInt(e)),Object(u.a)(n)}))};return Object(c.jsxs)(c.Fragment,{children:[Object(c.jsx)("div",{className:"boxes",children:a.map((function(e,r){return Object(c.jsxs)("div",{className:"row",children:[Object(c.jsxs)("p",{className:"row-title",children:["Box ",r]}),Object(c.jsxs)("div",{className:"input-row",children:["Degradation speed",Object(c.jsx)("input",{type:"number",value:d[r],onChange:function(e){return j(e.target.value,r,l)}})]}),Object(c.jsxs)("div",{className:"input-row",children:["Step width divisor",Object(c.jsx)("input",{type:"number",value:n[r],onChange:function(e){return j(e.target.value,r,s)}})]}),Object(c.jsx)("button",{onClick:function(){return t(r)},children:"Delete"})]},"".concat(r,"_").concat(e.join("-")))}))}),Object(c.jsxs)("div",{className:"row options",children:[Object(c.jsx)("input",{type:"checkbox",checked:r,onChange:function(){return i(!r)}}),"Display borders"]}),Object(c.jsxs)("div",{className:"row options",children:[Object(c.jsx)("input",{type:"number",value:b,onChange:function(e){return o(e.target.value)}}),"Number of steps"]})]})},p=function(e){var t=e.addShape,n=e.canvasRef,a=e.imageUrl,s=e.savedShapes,i=e.setIsLoading,u=Object(r.useRef)([0,0,0,0]),o=Object(r.useState)(!1),j=Object(b.a)(o,2),h=j[0],p=j[1],f=Object(r.useState)(null),O=Object(b.a)(f,2),v=O[0],g=O[1];Object(r.useEffect)((function(){if(a){i(!0);var e=new Image;e.src=a,e.decoding="async",e.decode().then((function(){p(e.width<e.height),i(!1),g(e)}))}}),[n,a,i]);var x=Object(r.useState)(null),m=Object(b.a)(x,2),w=m[0],S=m[1],y=Object(r.useCallback)(function(){var e=Object(d.a)(l.a.mark((function e(t){return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(v){e.next=2;break}return e.abrupt("return");case 2:v.width>v.height?(p(!1),n.current.width=n.current.clientWidth,n.current.height=n.current.clientWidth/v.width*v.height):(p(!0),n.current.height=n.current.clientHeight,n.current.width=n.current.clientHeight/v.height*v.width),t.drawImage(v,0,0,n.current.width,n.current.height);case 4:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),[n,v]),k=Object(r.useCallback)((function(e){s.map((function(t,n){var c=Object(b.a)(t,4),r=c[0],a=c[1],s=c[2],i=c[3];return e.strokeStyle="transparent",e.strokeRect(r,a,s,i),!0}))}),[s]),N=Object(r.useCallback)(function(){var e=Object(d.a)(l.a.mark((function e(t){var c;return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(t||n.current){e.next=2;break}return e.abrupt("return");case 2:(c=null!==t&&void 0!==t?t:n.current.getContext("2d")).clearRect(0,0,n.current.width,n.current.height),y(c),k(c);case 6:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),[n,y,k]);Object(r.useEffect)((function(){N()}),[N,a]);var C=function(e,t){var c=n.current.getBoundingClientRect();return{x:e-c.left,y:t-c.top}},I=function(e){S(null),0!==!u.current[2]&&0!==u.current[3]&&t(u.current)};return Object(c.jsx)("canvas",{className:"canvas ".concat(h?"is-vertical":""),onMouseDown:a?function(e){var t=n.current.getContext("2d");S(t);var c=C(e.clientX,e.clientY);u.current=[c.x,c.y,0,0]}:null,onMouseUp:a?I:null,onMouseLeave:a?function(){w&&I()}:null,onMouseMove:a?function(e){if(w){N(w);var t=Object(b.a)(u.current,2),n=t[0],c=t[1],r=C(e.clientX,e.clientY),a=r.x-n,s=r.y-c;w.strokeStyle="blue",w.strokeRect(n,c,a,s),u.current=[n,c,a,s]}}:null,ref:n})};var f=function(){var e=Object(r.useRef)(),t=Object(r.useState)(null),n=Object(b.a)(t,2),a=n[0],s=n[1],i=Object(r.useState)(!1),o=Object(b.a)(i,2),f=o[0],O=o[1],v=Object(r.useState)([]),g=Object(b.a)(v,2),x=g[0],m=g[1],w=Object(r.useState)(!1),S=Object(b.a)(w,2),y=S[0],k=S[1],N=Object(r.useState)([]),C=Object(b.a)(N,2),I=C[0],L=C[1],R=Object(r.useState)(1),B=Object(b.a)(R,2),D=B[0],F=B[1],M=Object(r.useState)([]),_=Object(b.a)(M,2),J=_[0],P=_[1],U=function(){var e=Object(d.a)(l.a.mark((function e(t){return l.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:s(null),m([]),F(1),L([]),P([]);case 5:case"end":return e.stop()}}),e)})));return function(t){return e.apply(this,arguments)}}(),E=function(e,t){return e.map((function(e,n){return t!==n&&e})).filter((function(e){return e}))},H=function(){var t=!(arguments.length>0&&void 0!==arguments[0])||arguments[0];return x.length>0?"".concat("","/composition/").concat(t?"preview_":"").concat(a,"?boxes=").concat(JSON.stringify(x),"&width=").concat(e.current.width,"&showBorders=").concat(y,"&speeds=").concat(JSON.stringify(I),"&steps=").concat(D,"&distances=").concat(JSON.stringify(J)):"".concat("","/static/uploads/preview_").concat(a)};return Object(c.jsxs)("div",{className:"page",children:[Object(c.jsxs)("div",{className:"main ".concat(a?"":"is-empty"),children:[Object(c.jsx)(p,{addShape:function(e){m([].concat(Object(u.a)(x),[e])),P([].concat(Object(u.a)(J),[5])),F(5),L([].concat(Object(u.a)(I),[1]))},canvasRef:e,imageUrl:a?H():null,savedShapes:x,setIsLoading:O}),f&&Object(c.jsx)("div",{className:"loader"})]}),Object(c.jsxs)("div",{className:"sidebar",children:[Object(c.jsx)(h,{deleteShape:function(e){P(E(J,e)),L(E(I,e)),m(E(x,e))},distances:J,hasVisibleBorders:y,savedShapes:x,setDistances:P,setHasVisibleBorders:k,setSteps:F,setSpeeds:L,steps:D,speeds:I}),Object(c.jsx)(j,{API_URL:"",resetState:U,setImageFilename:s,setIsLoading:O}),Object(c.jsx)("a",{href:H(!1),target:"_blank",className:"downloader",children:"Export high quality"})]})]})},O=function(e){e&&e instanceof Function&&n.e(3).then(n.bind(null,19)).then((function(t){var n=t.getCLS,c=t.getFID,r=t.getFCP,a=t.getLCP,s=t.getTTFB;n(e),c(e),r(e),a(e),s(e)}))};i.a.render(Object(c.jsx)(a.a.StrictMode,{children:Object(c.jsx)(f,{})}),document.getElementById("root")),O()}},[[18,1,2]]]);
//# sourceMappingURL=main.e866ec85.chunk.js.map