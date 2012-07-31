var macrolist = new Array();
macrolist.push("kx-basic");
// we can add more advanced kaixin test cases here

iimDisplay("Start kx Test");

/*
 * !!! CONFIGURATION REQUIRED !!!
 */
iimSet("USERNAME", "your_username");
iimSet("PASSWORD", "your_password");

iimSet("IGNORE_ERROR", "NO"); // 是否在遇到错误后不立即停止
iimSet("TIMEOUT", "25");
iimSet("REPLAY_SPEED", "MEDIUM"); // 重放的速度：FAST, MEDIUM, SLOW

iimSet("RANDOM", Math.random());

var i, retcode;
var report =  "";
var now = new Date();
for (i = 0; i < macrolist.length; i++) {
    iimDisplay("Step " + (i+1) + " of " + macrolist.length + "\nMacro: " + macrolist[i]);
    retcode = iimPlay(macrolist[i]);
    report += macrolist[i];
    if (retcode < 0) {
        report += ": " + iimGetLastError();
    } else {
        report += ": OK";
        /* display the FIRST extracted item in report*/
        s = iimGetLastExtract(1);
        if ( s != "" )  report += ", Extract: "+s;
    }
    report += "\n";
}
var elapsed = (new Date() - now) / 1000;
report = "Elapsed: " + elapsed + "s\n\n" + report;

iimDisplay("Test complete");

alert(report);

