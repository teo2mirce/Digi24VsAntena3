// run on https://www.antena3.ro/
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

//Antena
var arr = [], l = document.links;
for(var i=0; i<l.length; i++) {
  arr.push(l[i].href);
}
newarr=arr.filter( w => w.substring(0,"https://www.antena3.ro/".length)=="https://www.antena3.ro/" && w.substr(-5)==".html")
newarr=newarr.map( w=> w.slice(0,-5))//scoatem .html
newarr=newarr.filter( w =>  !isNaN(w.substr(-6)))
newarr=newarr.filter( w => w.indexOf("/tag/")==-1 )
newarr=newarr.map( w=> w+".html")//punem html inapoi
newarr=$.unique(newarr)



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

					x=parseHTML(text).querySelector(".text").innerText;
					
					downloadUrl('a'+ii+'.txt',x);
				}
		});
	},200);

}




