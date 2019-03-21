//Run on https://www.digi24.ro/
function downloadUrl(filename,data)
{    
    var link = document.createElement('a');
    mimeType = 'text/plain';
    link.setAttribute('download', filename);
    link.setAttribute('href', 'data:' + mimeType + ';charset=utf-8,' + data);
    link.click(); 

}
//https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro
function parseHTML(html) {
    var t = document.createElement('template');
    t.innerHTML = html;
    return t.content.cloneNode(true);
}


//Digi:

var arr = [], l = document.links;
for(var i=0; i<l.length; i++) {
  arr.push(l[i].href);
}
newarr=arr.filter( w => w.substring(0,"https://www.digi24.ro/".length)=="https://www.digi24.ro/" && !isNaN(w.substr(-6)))
newarr=$.unique(newarr)


//Articol


for(var i=0;i<newarr.length;i++)
{
	let ii=i;
	setTimeout(function()
	{
		url=newarr[ii]
		$.ajax({
			url:
				url,
				type:'GET',
				success: function(data){
					//https://stackoverflow.com/questions/6659351/removing-all-script-tags-from-html-with-js-regular-expression
					text = data.replace(/<script[^>]*>(?:(?!<\/script>)[^])*<\/script>/g, "")



					x=parseHTML(text).querySelector(".data-app-meta-article").innerText;
					
					downloadUrl('d'+ii+'.txt',x);
				}
		});
	},100);

}

