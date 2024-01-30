var isDevice = false;
if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ) {
	isDevice = true;
}
// khong the phong to cua so
function openPopUp(url, windowName, w, h, scrollbar) {
	var winl = (screen.width - w) / 2;
	var wint = (screen.height - h) / 2;
	winprops = 'height='+h+',width='+w+',top='+wint+',left='+winl+',scrollbars='+scrollbar ;
	win = window.open(url, windowName, winprops);
	if (parseInt(navigator.appVersion) >= 4) {
		win.window.focus();
	}
}

// co the phong to cua so
var win=null;
function NewWindow(mypage,myname,w,h,scroll,pos){
	if(pos=="random"){LeftPosition=(screen.width)?Math.floor(Math.random()*(screen.width-w)):100;TopPosition=(screen.height)?Math.floor(Math.random()*((screen.height-h)-75)):100;}
	if(pos=="center"){LeftPosition=(screen.width)?(screen.width-w)/2:100;TopPosition=(screen.height)?(screen.height-h)/2:100;}
	else if((pos!="center" && pos!="random") || pos==null){LeftPosition=0;TopPosition=20}
	settings='width='+w+',height='+h+',top='+TopPosition+',left='+LeftPosition+',scrollbars='+scroll+',location=no,directories=no,status=no,menubar=no,toolbar=no,resizable=yes';
	win=window.open(mypage,myname,settings);}

// is_num
function is_num(event,f){
	if (event.srcElement) {kc =  event.keyCode;} else {kc =  event.which;}
	if ((kc < 47 || kc > 57) && kc != 8 && kc != 0) return false;
	return true;
}


function format_number (num) {
	num = num.toString().replace(/\$|\./g,'');
	if(isNaN(num))
		num = "0";
	sign = (num == (num = Math.abs(num)));
	num = Math.round(num*100+0.50000000001);
	num = Math.round(num/100).toString();
	for (var i = 0; i < Math.floor((num.length-(1+i))/3); i++)
		num = num.substring(0,num.length-(4*i+3))+'.'+ num.substring(num.length-(4*i+3));
	return (((sign)?'':'-') + num);
}


function numberOnly (myfield, e){
	var key,keychar;
	if (window.event){key = window.event.keyCode}
	else if (e){key = e.which}
	else{return true}
	keychar = String.fromCharCode(key);
	if ((key==null) || (key==0) || (key==8) || (key==9) || (key==13) || (key==27)){return true}
	else if (("0123456789").indexOf(keychar) > -1){return true}
	return false;
};


/*--------------- Link advertise ----------------*/
window.rwt = function (obj, type, id) {
	try {
		if (obj === window) {
			obj = window.event.srcElement;
			while (obj) {
				if (obj.href) break;
				obj = obj.parentNode
			}
		}
		obj.href = ROOT+'?'+cmd+'=mod:advertise|type:'+type+'|lid:'+id;
		obj.onmousedown = ""
	} catch(o) {}
	return true ;
};

(function (jQuery) {
	jQuery.fn.clickoutside = function (callback) {
		var outside = 1,
			self = $(this);
		self.cb = callback;
		this.click(function () {
			outside = 0
		});
		$(document).click(function (event) {
			if (event.button == 0) {
				outside && self.cb();
				outside = 1
			}
		});
		return $(this)
	}
})(jQuery);

(function($) {
	$.fn.hoverDelay = function(f,g) {
		var cfg = {
			sensitivity: 7,
			delayOver: 150,
			delayOut: 0
		};
		cfg = $.extend(cfg, g ? { over: f, out: g } : f );
		var cX, cY, pX, pY;

		var track = function(ev) {
			cX = ev.pageX;
			cY = ev.pageY;
		};

		var compare = function(ev,ob) {
			ob.hoverDelay_t = clearTimeout(ob.hoverDelay_t);

			if ( ( Math.abs(pX-cX) + Math.abs(pY-cY) ) < cfg.sensitivity ) {
				$(ob).unbind("mousemove",track);

				ob.hoverDelay_s = 1;
				return cfg.over.apply(ob,[ev]);
			} else {

				pX = cX; pY = cY;

				ob.hoverDelay_t = setTimeout( function(){compare(ev, ob);} , cfg.delayOver );
			}
		};

		var delay = function(ev,ob) {
			ob.hoverDelay_t = clearTimeout(ob.hoverDelay_t);
			ob.hoverDelay_s = 0;
			return cfg.out.apply(ob,[ev]);
		};

		var handleHover = function(e) {
			var ev = jQuery.extend({},e);
			var ob = this;

			if (ob.hoverDelay_t) { ob.hoverDelay_t = clearTimeout(ob.hoverDelay_t); }

			// if e.type == "mouseenter"
			if (e.type == "mouseenter") {
				pX = ev.pageX; pY = ev.pageY;
				$(ob).bind("mousemove",track);
				if (ob.hoverDelay_s != 1) { ob.hoverDelay_t = setTimeout( function(){compare(ev,ob);} , cfg.delayOver );}

				// else e.type == "mouseleave"
			} else {
				// unbind expensive mousemove event
				$(ob).unbind("mousemove",track);
				if (ob.hoverDelay_s == 1) { ob.hoverDelay_t = setTimeout( function(){delay(ev,ob);} , cfg.delayOut );}
			}
		};
		return this.bind('mouseenter',handleHover).bind('mouseleave',handleHover);
	};
})(jQuery);


function load_Statistics ()
{
	$.ajax({
		async: true,
		dataType: 'json',
		url: ROOT+"load_ajax.php?do=statistics",
		type: 'POST',
		success: function (data) {
			$("#stats_online").html(data.online);
			$("#stats_totals").html(data.totals);
			$("#stats_member").html(data.mem_online);
		}
	}) ;

}


function LoadAjax(doAct,mydata,ext_display) {
	$.ajax({
		async: true,
		url: ROOT+'load_ajax.php?do='+doAct,
		type: 'POST',
		data: mydata ,
		success: function (data) {
			$("#"+ext_display).html(data)
		}
	}) ;
}

/** 01. Top Nav
 **************************************************************** **/
function _topNav() {

}

vnTRUST.do_Regsiter = function(form)
{

  var ok_submit = 1 ;   

  if(ok_submit){
    var params =  $("#formReg").serialize();
    $.ajax({
      /*url: ROOT + 'load_ajax.php?do=register',*/
      url: ROOT + 'load_ajax.php?do=receive',
      dataType: "json",
      type: "post",
      data: params,
      beforeSend: function(){
        var tpl_loading='<div class="loading loading-account" >\n' +
          '    <div class="black_overlay" id="fade"></div>\n' +
          '    <div class="spinner-container-forgot white_content" style="text-align: center;">\n' +
          '    <img src="'+DIR_IMAGE +'/ajax-loading.gif" alt="loading" width="150" />\n' +
          '    </div>\n' +
          '    </div>';
        $("#formReg").append(tpl_loading);
      },
      success: function (rs) {        
      	$("#formReg .loading").remove();
        if (rs.ok == 1){ 
        	$.fancybox.close();
          $("#formReg")[0].reset();          
          jAlert(rs.mess,js_lang['announce']);
        }else {
          jAlert(rs.mess,js_lang['error']);
        }
      }
    });
  }


  return true;
};

vnTRUST.do_Contact = function(form){
  var ok_submit = 1 ;
  var recaptcha = grecaptcha.getResponse();
  if(recaptcha.length==0){
    ok_submit = 0 ;
    jAlert('Vui lòng check Google Captcha',js_lang['error']);
    return false;
  }

  if(ok_submit){
  	$("#do_submit").addClass("disabled");
  	
    var params =  $("#formContact").serialize();
    $.ajax({
      /*url: ROOT+'load_ajax.php?do=contact',*/
      url: ROOT+'load_ajax.php?do=receive',
      dataType: "json",
      type: "post",
      data: params,
      beforeSend: function(){
        var tpl_loading='<div class="loading loading-account" >\n' +
          '    <div class="black_overlay" id="fade"></div>\n' +
          '    <div class="spinner-container-forgot white_content" style="text-align: center;">\n' +
          '    <img src="'+DIR_IMAGE +'/ajax-loading.gif" alt="loading" width="150" />\n' +
          '    </div>\n' +
          '    </div>';
        $("#ext_contact").append(tpl_loading);
      },
      success: function (rs) {
        grecaptcha.reset();
        $("#ext_contact").find('.loading').remove();
        if (rs.ok == 1){
          $("#formContact")[0].reset();

          $("#formContact .div_input ").removeClass('has-feedback has-success');
          $("#formContact .div_input").find('span.fa').remove();

          jAlert(rs.mess,js_lang['announce']);
        }else {
          jAlert(rs.mess,js_lang['error']);
        }
        $("#do_submit").removeClass("disabled");
      }
    });
  }


  return true;

};

vnTRUST.do_Agency = function(form){
  var ok_submit = 1 ;
  /*var recaptcha = grecaptcha.getResponse();
  if(recaptcha.length==0){
    ok_submit = 0 ;
    jAlert('Vui lòng check Google Captcha',js_lang['error']);
    return false;
  }*/

  if(ok_submit){
  	$("#do_agency").addClass("disabled");
  	
    var params =  $("#formAgency").serialize();
    $.ajax({
      // url: ROOT+'load_ajax.php?do=agency',
      url: ROOT+'load_ajax.php?do=receive',
      dataType: "json",
      type: "post",
      data: params,
      success: function (rs) {
        // grecaptcha.reset();
        if (rs.ok == 1){
          $("#formAgency")[0].reset();
          $("#formAgency .div_input ").removeClass('has-feedback has-success');
          $("#formAgency .div_input").find('span.fa').remove();

          jAlert(rs.mess,js_lang['announce']);
        }else {
          jAlert(rs.mess,js_lang['error']);
        }
        $("#do_agency").removeClass("disabled");
      }
    });
  }


  return true;

};

/** Core
 **************************************************************** **/
function TRUSTvn() {
	var Xwidth = $(window).width();

	if(Xwidth<1100){$(".floating-left").hide() ; $(".floating-right").hide()}
	_topNav();


	$(".fancybox").fancybox();

	$(".alert-autohide").delay(5000).slideUp(200, function() {
		$(this).alert('close');
	});
 
	load_Statistics();
	//vnTRUST.goTopStart();

}

/* Init */
jQuery(window).ready(function () {
	TRUSTvn();
});