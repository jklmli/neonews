$(document).ready(function(){
	items = jQuery.parseJSON(itemsJSON);
	resultMap = {};
	var initList = $('li');
	resultMap[''] = initList;
	$('input').keyup(function(){
		var searchtext = $(this).val();
		if(resultMap[searchtext]==undefined)
		{
			var querymatch = "";
			$('li').remove();
			if(items[0].model == "groups.post")
			{
				for(var i =0; i<items.length;i++)
				{
					if(items[i].fields.subject.indexOf(searchtext)>-1 || items[i].fields.sender.indexOf(searchtext)>-1 || items[i].fields.message.indexOf(searchtext)>-1 || items[i].fields.date.indexOf(searchtext)>-1)
					{
						querymatch += "<li><a href=\"/groups/" + items[i].fields.group + "/" + items[i].pk + "\">" + items[i].fields.subject +"</a>\""+ items[i].fields.sender + " " +items[i].fields.date + "\"</li>";
					}
				}
			}
			else if(items[0].model == "groups.group")
			{
				for(var i =0; i<items.length;i++)
				{
					if(items[i].fields.name.indexOf(searchtext)>-1)
					{
						querymatch += "<li><a href=\"/groups/" + items[i].pk + "/\">" + items[i].fields.name + "</a></li>";
					}
				}
			}
			$('ul').after().html(querymatch);
			resultMap[searchtext] = querymatch;
		}
		else
		{
			$('li').remove();
			$('ul').after().html(resultMap[searchtext]);
		}
	});
});

/*
$(document).ready(function(){
	items = jQuery.parseJSON(itemsJSON);
	resultMap = {};
	var initHTML = "";

	if(items[0].model == "groups.post")
	{
		for(var i =0; i<items.length;i++)
		{
			initHTML += "<li><a href=\"/groups/" + items[i].fields.group + "/" + items[i].pk + "\">" + items[i].fields.subject +"</a>\""+ items[i].fields.sender + " " +items[i].fields.date + "\"</li>";
		}
	}
	else if(items[0].model == "groups.group")
	{
		for(var i =0; i<items.length;i++)
		{
			initHTML += "<li><a href=\"/groups/" + items[i].pk + "/\">" + items[i].fields.name + "</a></li>";
		}
	}
	resultMap[''] = initHTML;
	$('input').keyup(function(){
		var searchtext = $(this).val();
		if(resultMap[searchtext]==undefined)
		{
			var querymatchHTML = "";
			$('li').remove();
			if(items[0].model == "groups.post")
			{
				for(var i =0; i<items.length;i++)
				{
					if(items[i].fields.subject.indexOf(searchtext)>-1 || items[i].fields.sender.indexOf(searchtext)>-1 || items[i].fields.message.indexOf(searchtext)>-1 || items[i].fields.date.indexOf(searchtext)>-1)
					{
						querymatchHTML += "<li><a href=\"/groups/" + items[i].fields.group + "/" + items[i].pk + "\">" + items[i].fields.subject +"</a>\""+ items[i].fields.sender + " " +items[i].fields.date + "\"</li>";
					}
				}
			}
			else if(items[0].model == "groups.group")
			{
				for(var i =0; i<items.length;i++)
				{
					if(items[i].fields.name.indexOf(searchtext)>-1)
					{
						querymatchHTML += "<li><a href=\"/groups/" + items[i].pk + "/\">" + items[i].fields.name + "</a></li>";
					}
				}
			}
			$('ul').after().html(querymatchHTML);
			resultMap[searchtext] = querymatchHTML;
		}
		else
		{
			$('li').remove();
			$('ul').after().html(resultMap[searchtext]);
		}
	});
});
*/
