
	var clockDisplay = new SegmentDisplay("canClock");
	clockDisplay.pattern         = "##:##";
	var CCOUNT = (60 * 2) +1;	// 10mins
	var timer, count;	

	var periode = new SegmentDisplay("canPeriode");
	periode.pattern		= "#";
	var periodeValue = 0;

	var vis =  new SegmentDisplay("canVis");
	vis.pattern         = "##";
	var visScore = 0;

	var home =  new SegmentDisplay("canHome");
	home.pattern        = "##";
	var homeScore = 0;
	
	var etat = {	//stucture pour transporter data vers python
		time	:"00:00",
		home	:"00",
		vis		:"00",
		per		:"0",
		toString: function(){
			return this.time + ":" +
			this.home + ":" +
			this.vis + ":" +
			this.per
			}
	}	

// Controls and buttons
// webiopi Calls

function setupWebiopi(){	
	count = CCOUNT;
	display();
}

function callMacroSerial(){
	var args = etat.toString(); 
	var d = $("#output").text() + args + " ; ";
	$("#output").text(d);
	webiopi().callMacro("serialTX",args, printSerial);
}
function printSerial(macro, args, data){
	var d = $("#output").text() + data + "\n";
	$("#output").text(d);
}

//web UI calls
function btnStopClick(){
	clearTimeout(timer);
}

function btnGoClick(){
	animate();
}
function btnPlusOneSecClick(){
	count++;
	display();
}

function btnMinusOneSecClick(){
	count--;
	display();
	}

function btnPeriodePlus(){
	periodeValue++;
	display();
}
function btnPeriodeMoins(){
	periodeValue--;
	display();
}
function btnHomePlus(){
	homeScore++;
	display();
}
function btnHomeMoins(){
	homeScore--;
	display();
}
function btnVisiteurPlus(){
	visScore++;
	display();
}
function btnVisiteurMoins(){
	visScore--;
	display();
}
function btntimerReset(){
	count = CCOUNT;
	display();
}
function timerReset(time){
	timerPause();
	count = time;
}
function timerPause(){
	clearTimeout(timer);
}

function parseTime(time){
	var second = time % 60;
	var minute = Math.floor(time / 60) % 60;

	var value   = ((minute < 10) ? '0' : '') + minute
	+ ((second % 2 ==0) ? ':' : ' ' )		// flashe ":"
		+ ((second < 10) ? '0' : '') + second;
	return value;
}
function parseScore(score){
	var value = ((score<10) ? '0' : '') + score;
	return value;
}	

function display(){
	//gather and parse vars
	var value = parseTime(count);
	
	//recupere data dans Etat pour TX
	etat.home = parseScore(homeScore);
	etat.vis = parseScore(visScore);
	etat.per = periodeValue;	
	etat.time = value.replace(" ",":");	
	
	//send to canvas
	clockDisplay.setValue(value);
	home.setValue(etat.home);
	vis.setValue(etat.vis);	
	periode.setValue("" + periodeValue);	
}

function animate(){

	display();

	if (count == 0){
		//time's up
		alert('Time out');
		}
	else {
		count--;
		timer = setTimeout("animate()", 1000);
	}
}
