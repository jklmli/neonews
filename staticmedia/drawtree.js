$(document).ready(function(){
	var items = jQuery.parseJSON(itemsJSON);
	childMap = {};
	for(var i=0; i < items.length;i++)
	{
		childMap[items[i].fields.messageID] = items[i];
	}
	
	var getRoot = function(currID){
		var curPost = childMap[currID];
		while(curPost.fields.in_reply_to != "")
		{
			curPost = childMap[curPost.fields.in_reply_to];
		}
		return curPost.fields.messageID;
	};
//It seems that sometimes the children are not seen. For example, try searching Course Average and Letter Grade and look at the map. Only 2 dots shown. Actually 3 posts in thread.
	var drawMap = function(root){
		var nodeQueue = [];
		nodeQueue.push(root);
		var width = 800;
		var height = 450;
		var heightDiv = 10;
		var canvas = $('canvas#canvas')[0]; 
		var context = canvas.getContext("2d");
		context.fillStyle= 'green';
		context.fillRect(width/2, 0, heightDiv, heightDiv);
		var currHeight = 1;
		while(nodeQueue.length != 0)
		{
			var curr = nodeQueue.shift();
			var children = childMap[curr].fields.children.split(" ");
			console.log(children);
			var widthDiv = width/(2*children.length);
			for (var i=1; i< children.length; i++){ //starting at 1 since first element is always empty string based on how we constructed children string
				context.fillRect(widthDiv + (2*(i-1)*widthDiv), 2* currHeight * heightDiv, heightDiv, heightDiv);
				nodeQueue.push(children[i]);
			}
			currHeight++;
		}
		var img = canvas.toDataURL("image/png");
		$('<img src="' + img + '" usemap=' + '"#testmap" ' + '/>').insertAfter('script');
		$('#canvas').remove();
	};

	var root = getRoot(postID);
	drawMap(root);
});
