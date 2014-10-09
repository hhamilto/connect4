// Copyright 2013 Paul Brewer
// License: You may copy this file under the same terms as the MIT License
// located at http://opensource.org/licenses/MIT
// This file is provided AS IS WITH NO WARRANTY OF ANY KIND. All use is at your own risk.
//
// Status: July 13, 2013, Paul Brewer:  First version. Simple test case passed.  It needs to be more extensively tested.
//   It lacks escaping for odd characters in strings, though a workaround is possible as described in the comments.
// 
// July 14, 2013, Paul Brewer:  JSON.stringify() used to stringify basic
// types such as string, number, null/undefined.  This provides string
// escaping correctly, which is complex and important.
//
// .toJSON detected and called for objects like Date
//
// added indicator function for misc punctuation
// plan is now a list of items to stringify, so functions are used
// for punctuation since functions are not otherwise permitted in json
// Testing for particular punctuation is attempted with === for efficiency
// instead of evaluating the function. If an unknown function appears
// in plan, it came from the object directly, and so we ignore it.

function leftSquareBracket(){ return '[' }
function rightSquareBracket(){ return ']' }
function leftCurlyBracket(){ return '{' }
function rightCurlyBracket(){ return '}' }
function comma(){ return ',' }
function quote(){ return '"' }
function quoteColon(){ return '":' }
function colon(){ return ':' }


function stringifyToStream(obj, stream, onsuccess, onfail){
	var i,l, plan=[];

	function nextChunk(){
		var cursor,str='';
		try {
			if (plan.length === 0) return onsuccess();
			cursor = plan.shift();
			if (typeof cursor === 'undefined'){ 
				str = 'null' 
			} else if (typeof cursor === 'object'){
				if (cursor === null){ 
					str='null' 
				} else if (typeof cursor.toJSON === 'function'){
					str = '"'+cursor.toJSON()+'"';
				} else { 
					return stringifyToStream(cursor, stream, nextChunk, onfail)
				}
			} else if (typeof cursor === 'function'){
				if (cursor === comma){
					str = ",\n"; 
				} else if (cursor === colon){
					str = ':';
				} else if (cursor === leftSquareBracket){
					str = '[';
				} else if (cursor === rightSquareBracket){
					str = ']';
				} else if (cursor === leftCurlyBracket){
					str = '{';
				} else if (cursor === rightCurlyBracket){
					str = '}';
				} else if (cursor === quote){
					str = '"'; 
				} else if (cursor === quoteColon){
					str = '":';
				} else return nextChunk(); // ignore unknown funcs in plan
			} else str = JSON.stringify(cursor); // not a function,object,array
			return stream.write(str, nextChunk);
		} catch(e){ 
			return onfail(e); 
		}
	}

	if (typeof obj !== 'object'){
		return stream.write(JSON.stringify(obj), function(){setImmidiate(onsuccess)});
	}

	if (typeof obj.toJSON === 'function'){ 
		return stream.write(obj.toJSON(), function(){setImmidiate(onsuccess)});
	}

	if (Object.prototype.toString.call(obj)==='[object Array]'){
		plan.push(leftSquareBracket);
		if (obj.length > 0){ 
			for(i=0,l=obj.length;i<l;++i){
				plan.push(obj[i], comma);
			}
			plan.pop(); // extra comma
		}
		plan.push(rightSquareBracket);
	} else {
		plan.push(leftCurlyBracket);
		l = 0;
		for (i in obj){
			if (obj.hasOwnProperty(i)){
				plan.push(i,colon,obj[i],comma);
				++l;
			}
		}
		if (l>0) plan.pop(); // remove last comma
			plan.push(rightCurlyBracket);
	}

	return nextChunk();

}

exports.stringifyToStream = stringifyToStream;

