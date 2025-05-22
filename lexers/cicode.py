"""
Copyright (c) 2013-present Matic Kukovec. 
Released under the GNU GPL3 license.

For more information check the 'LICENSE.txt' file.
For complete license information of the dependencies, check the 'additional_licenses' directory.
"""

import keyword
import builtins
import re
import functions
import qt
import data
import time
import lexers


class CiCode(qt.QsciLexerCustom):
    """
    Custom lexer for the Citect CiCode programming language
    """
    class Sequence:
        def __init__(self, 
                     start, 
                     stop_sequences, 
                     stop_characters, 
                     style, 
                     add_to_style):
            self.start = start
            self.stop_sequences = stop_sequences
            self.stop_characters = stop_characters
            self.style = style
            self.add_to_style = add_to_style
    
    styles = {
        "Default" : 0,
        "Comment" : 1,
        "MultilineComment" : 2,
        "Keyword" : 3,
        "BuiltInFunction" : 4,
        "String" : 5,
        "Number" : 6,
        "Operator" : 7,
        "Function" : 8,
    }
    # Class variables
    keyword_list = [
        "function", "end", "if", "else", "do", "then",
        "while", "for", "mod", "bitand", "bitor", "bitxor",
        "and", "or", "not", "bitand", "bitor", "bitxor",
        "global", "public", "private", "return", 
    ]
    type_list = [
        "string", "object", "int", "real", "quality", "timestamp",
    ]
    builtin_function_list = [
        "abs", "acccontrol", "accumbrowseclose", "accumbrowsefirst", "accumbrowsegetfield", "accumbrowsenext", "accumbrowsenumrecords", 
        "accumbrowseopen", "accumbrowseprev", "alarmack", "alarmackrec", "alarmacktag", "alarmactive", "alarmcatgetformat", 
        "alarmclear", "alarmclearrec", "alarmcleartag", "alarmcomment", "alarmcount", "alarmcountequipment", "alarmcountlist", 
        "alarmdelete", "alarmdisable", "alarmdisablerec", "alarmdisabletag", "alarmdsp", "alarmdspclusteradd", "alarmdspclusterinuse", 
        "alarmdspclusterremove", "alarmdsplast", "alarmdspnext", "alarmdspprev", "alarmenable", "alarmenablerec", "alarmenabletag", 
        "alarmeventque", "alarmfilterclose", "alarmfiltereditappend", "alarmfiltereditclose", "alarmfiltereditcommit", "alarmfiltereditfirst", "alarmfiltereditlast", 
        "alarmfiltereditnext", "alarmfiltereditopen", "alarmfiltereditprev", "alarmfiltereditset", "alarmfilterform", "alarmfilteropen", "alarmfirstcatrec", 
        "alarmfirstprirec", "alarmfirsttagrec", "alarmgetdelay", "alarmgetdelayrec", "alarmgetdsp", "alarmgetfieldrec", "alarmgetfiltername", 
        "alarmgetinfo", "alarmgetorderbykey", "alarmgetthreshold", "alarmgetthresholdrec", "alarmhelp", "alarmnextcatrec", "alarmnextprirec", 
        "alarmnexttagrec", "alarmnotifyvarchange", "alarmqueryfirstrec", "alarmquerynextrec", "alarmresetquery", "alarmsetdelay", "alarmsetdelayrec", 
        "alarmsetinfo", "alarmsetquery", "alarmsetthreshold", "alarmsetthresholdrec", "alarmsplit", "alarmsumappend", "alarmsumcommit", 
        "alarmsumdelete", "alarmsumfind", "alarmsumfirst", "alarmsumget", "alarmsumlast", "alarmsumnext", "alarmsumprev", 
        "alarmsumset", "alarmsumsplit", "alarmsumtype", "almbrowseack", "almbrowseclear", "almbrowseclose", "almbrowsedisable", 
        "almbrowseenable", "almbrowsefirst", "almbrowsegetfield", "almbrowsenext", "almbrowsenumrecords", "almbrowseopen", "almbrowseprev", 
        "almsummaryack", "almsummaryclear", "almsummaryclose", "almsummarycommit", "almsummarydelete", "almsummarydeleteall", "almsummarydisable", 
        "almsummaryenable", "almsummaryfirst", "almsummarygetfield", "almsummarylast", "almsummarynext", "almsummarynumrecords", "almsummaryopen", 
        "almsummaryprev", "almsummarysetfieldvalue", "almtagsack", "almtagsclear", "almtagsclose", "almtagsdisable", "almtagsenable", 
        "almtagsfirst", "almtagsgetfield", "almtagsnext", "almtagsnumrecords", "almtagsopen", "almtagsprev", "anbyname", 
        "arccos", "arcsin", "arctan", "areacheck", "ass", "asschain", "asschainpage", 
        "asschainpopup", "asschainwin", "asschainwinfree", "assgetproperty", "assgetscale", "assinfo", "assinfoex", 
        "asspage", "asspopup", "assscalestr", "asstag", "asstitle", "assvartags", "asswin", 
        "assert", "beep", "callevent", "chainevent", "chartostr", "citectcolourtopackedrgb", "citectinfo", 
        "clipcopy", "clippaste", "clipreadln", "clipsetmode", "clipwriteln", "clusteractivate", "clusterdeactivate", 
        "clusterfirst", "clustergetname", "clusterisactive", "clusternext", "clusterservertypes", "clustersetname", "clusterstatus", 
        "clusterswapactive", "codesetmode", "codetrace", "comclose", "comopen", "comread", "comreset", 
        "comwrite", "cos", "createcontrolobject", "createobject", "ddeexec", "ddepost", "dderead", 
        "ddewrite", "ddehexecute", "ddehgetlasterror", "ddehinitiate", "ddehpoke", "ddehreadln", "ddehrequest", 
        "ddehsetmode", "ddehterminate", "ddehwriteln", "dllcall", "dllcallex", "dllclose", "dllopen", 
        "date", "dateadd", "dateday", "dateinfo", "datemonth", "datesub", "dateweekday", 
        "dateyear", "debugbreak", "debugmsg", "debugmsgset", "degtorad", "delayshutdown", "devappend", 
        "devclose", "devcontrol", "devcurr", "devdelete", "devdisable", "deveof", "devfind", 
        "devfirst", "devflush", "devgetfield", "devhistory", "devinfo", "devmodify", "devnext", 
        "devopen", "devopengrp", "devprev", "devprint", "devread", "devreadln", "devrecno", 
        "devseek", "devsetfield", "devsize", "devwrite", "devwriteln", "devzap", "displayruntimemanager", 
        "dllclasscallmethod", "dllclasscreate", "dllclassdispose", "dllclassgetproperty", "dllclassisvalid", "dllclasssetproperty", "driverinfo", 
        "dspancreatecontrolobject", "dspanfree", "dspangetarea", "dspangetmetadata", "dspangetmetadataat", "dspangetpos", "dspangetprivilege", 
        "dspaninrgn", "dspaninfo", "dspanmove", "dspanmoverel", "dspannew", "dspannewrel", "dspansetmetadata", 
        "dspansetmetadataat", "dspbar", "dspbmp", "dspbutton", "dspbuttonfn", "dspchart", "dspcol", 
        "dspdel", "dspdelayrenderbegin", "dspdelayrenderend", "dspdirty", "dsperror", "dspfile", "dspfilegetinfo", 
        "dspfilegetname", "dspfilescroll", "dspfilesetname", "dspfont", "dspfonthnd", "dspfullscreen", "dspgetanbottom", 
        "dspgetancur", "dspgetanextent", "dspgetanfirst", "dspgetanfrompoint", "dspgetanheight", "dspgetanleft", "dspgetannext", 
        "dspgetanright", "dspgetantop", "dspgetanwidth", "dspgetenv", "dspgetmouse", "dspgetmouseover", "dspgetnearestan", 
        "dspgetparentan", "dspgetslider", "dspgettip", "dspgraybutton", "dspinfo", "dspinfodestroy", "dspinfofield", 
        "dspinfonew", "dspinfovalid", "dspisbuttongray", "dspkernel", "dspmci", "dspmarkermove", "dspmarkernew", 
        "dspplaysound", "dsppopupconfigmenu", "dsppopupmenu", "dsprichtext", "dsprichtextedit", "dsprichtextenable", "dsprichtextgetinfo", 
        "dsprichtextload", "dsprichtextpgscroll", "dsprichtextprint", "dsprichtextsave", "dsprichtextscroll", "dsprubend", "dsprubmove", 
        "dsprubsetclip", "dsprubstart", "dspsetslider", "dspsettip", "dspsettooltipfont", "dspstatus", "dspstr", 
        "dspsym", "dspsymanm", "dspsymanmex", "dspsymatsize", "dsptext", "dsptipmode", "dsptrend", 
        "dsptrendinfo", "dumpkernel", "engtogeneric", "entercriticalsection", "equipbrowseclose", "equipbrowsefirst", "equipbrowsegetfield", 
        "equipbrowsenext", "equipbrowsenumrecords", "equipbrowseopen", "equipbrowseprev", "equipcheckupdate", "equipgetproperty", "equipsetproperty", 
        "equipstatebrowseclose", "equipstatebrowsefirst", "equipstatebrowsegetfield", "equipstatebrowsenext", "equipstatebrowsenumrecords", "equipstatebrowseopen", "equipstatebrowseprev", 
        "errcom", "errdrv", "errgethw", "errhelp", "errinfo", "errlog", "errmsg", 
        "errset", "errsethw", "errsetlevel", "errtrap", "exec", "executedtspkg", "exp", 
        "ftpclose", "ftpfilecopy", "ftpfilefind", "ftpfilefindclose", "ftpopen", "fact", "fileclose", 
        "filecopy", "filedelete", "fileeof", "fileexist", "filefind", "filefindclose", "filegettime", 
        "filemakepath", "fileopen", "fileprint", "fileread", "filereadblock", "filereadln", "filerename", 
        "filerichtextprint", "fileseek", "filesettime", "filesize", "filesplitpath", "filewrite", "filewriteblock", 
        "filewriteln", "fmtclose", "fmtfieldhnd", "fmtgetfield", "fmtgetfieldcount", "fmtgetfieldhnd", "fmtgetfieldname", 
        "fmtgetfieldwidth", "fmtopen", "fmtsetfield", "fmtsetfieldhnd", "fmttostr", "formactive", "formaddlist", 
        "formbutton", "formcheckbox", "formcombobox", "formcurr", "formdestroy", "formedit", "formfield", 
        "formgetcurrinst", "formgetdata", "formgetinst", "formgettext", "formgoto", "formgroupbox", "forminput", 
        "formlistaddtext", "formlistbox", "formlistdeletetext", "formlistselecttext", "formnew", "formnumpad", "formopenfile", 
        "formpassword", "formposition", "formprompt", "formradiobutton", "formread", "formsaveasfile", "formsecurepassword", 
        "formselectprinter", "formsetdata", "formsetinst", "formsettext", "formwndhnd", "fullname", "fuzzyclose", 
        "fuzzygetcodevalue", "fuzzygetshellvalue", "fuzzyopen", "fuzzysetcodevalue", "fuzzysetshellvalue", "fuzzytrace", "getarea", 
        "getbluevalue", "getenv", "getevent", "getgreenvalue", "getlanguage", "getlogging", "getpriv", 
        "getredvalue", "getwintitle", "grpclose", "grpdelete", "grpfirst", "grpin", "grpinsert", 
        "grpmath", "grpname", "grpnext", "grpopen", "grptostr", "halt", "hextostr", 
        "highbyte", "highword", "htmlhelp", "hwalarmque", "iodevicecontrol", "iodeviceinfo", "iodevicestats", 
        "infoform", "infoforman", "input", "inttoreal", "inttostr", "iserror", "kercmd", 
        "kernelqueuelength", "kerneltableinfo", "kerneltableitemcount", "keyallowcursor", "keybs", "keydown", "keyget", 
        "keygetcursor", "keyleft", "keymove", "keypeek", "keyput", "keyputstr", "keyreplay", 
        "keyreplayall", "keyright", "keysetcursor", "keysetseq", "keyup", "languagefiletranslate", "leavecriticalsection", 
        "libalarmfilterform", "ln", "log", "login", "loginform", "logout", "logoutidle", 
        "lowbyte", "lowword", "mailerror", "maillogoff", "maillogon", "mailread", "mailsend", 
        "makecitectcolour", "max", "menugetchild", "menugetfirstchild", "menugetgenericnode", "menugetnextchild", "menugetpagenode", 
        "menugetparent", "menugetprevchild", "menugetwindownode", "menunodeaddchild", "menunodegetproperty", "menunodehascommand", "menunodeisdisabled", 
        "menunodeishidden", "menunoderemove", "menunoderuncommand", "menunodesetdisabledwhen", "menunodesethiddenwhen", "menunodesetproperty", "menureload", 
        "message", "min", "msgbrdcst", "msgclose", "msggetcurr", "msgopen", "msgrpc", 
        "msgread", "msgstate", "msgwrite", "multimonitorstart", "multisignatureform", "multisignaturetagwrite", "name", 
        "oledatetotime", "objectassociateevents", "objectassociatepropertywithtag", "objectbyname", "objecthasinterface", "objectisvalid", "objecttostr", 
        "onevent", "packedrgb", "packedrgbtocitectcolour", "pagealarm", "pageback", "pagedisabled", "pagedisplay", 
        "pageexists", "pagefile", "pagefileinfo", "pageforward", "pagegetint", "pagegetstr", "pagegoto", 
        "pagehardware", "pagehistorydspmenu", "pagehistoryempty", "pagehome", "pageinfo", "pagelast", "pagelistcount", 
        "pagelistcurrent", "pagelistdelete", "pagelistdisplay", "pagelistinfo", "pagemenu", "pagenext", "pagepeekcurrent", 
        "pagepeeklast", "pagepoplast", "pagepopup", "pageprev", "pageprocessanalyst", "pageprocessanalystpens", "pagepushlast", 
        "pagerecall", "pagerichtextfile", "pagesoe", "pageselect", "pagesetint", "pagesetstr", "pagesummary", 
        "pagetask", "pagetransformcoords", "pagetrend", "pagetrendex", "parameterget", "parameterput", "pathtostr", 
        "pi", "plotclose", "plotdraw", "plotfile", "plotgetmarker", "plotgrid", "plotinfo", 
        "plotline", "plotmarker", "plotopen", "plotscalemarker", "plotsetmarker", "plottext", "plotxyline", 
        "pow", "print", "printfont", "println", "processanalystloadfile", "processanalystpopup", "processanalystselect", 
        "processanalystsetpen", "processanalystwin", "processisclient", "processisserver", "processrestart", "productinfo", "projectinfo", 
        "projectrestartget", "projectrestartset", "projectset", "prompt", "pulse", "qualitycreate", "qualitygetpart", 
        "qualityisbad", "qualityiscontrolinhibit", "qualityisgood", "qualityisoverride", "qualityisuncertain", "qualitysetpart", "qualitytostr", 
        "queclose", "quelength", "queopen", "quepeek", "queread", "quewrite", "radtodeg", 
        "rand", "reread", "realtostr", "repgetcluster", "repgetcontrol", "repsetcontrol", "report", 
        "round", "soearchive", "soedismount", "soeeventadd", "soemount", "spcalarms", "spcclientinfo", 
        "spcgethistogramtable", "spcgetsubgrouptable", "spcplot", "spcprocessxrsget", "spcprocessxrsset", "spcsetlimit", "spcspeclimitget", 
        "spcspeclimitset", "spcsubgroupsizeget", "spcsubgroupsizeset", "sqlappend", "sqlbegintran", "sqlcall", "sqlcancel", 
        "sqlclose", "sqlcommit", "sqlconnect", "sqlcreate", "sqldisconnect", "sqldispose", "sqlend", 
        "sqlerrmsg", "sqlexec", "sqlfieldinfo", "sqlgetfield", "sqlgetrecordset", "sqlgetscalar", "sqlinfo", 
        "sqlisnullfield", "sqlnext", "sqlnofields", "sqlnumchange", "sqlnumfields", "sqlopen", "sqlparamsclearall", 
        "sqlparamssetasint", "sqlparamssetasreal", "sqlparamssetasstring", "sqlprev", "sqlquerycreate", "sqlquerydispose", "sqlrollback", 
        "sqlrowcount", "sqlset", "sqltraceoff", "sqltraceon", "schdclose", "schdconfigclose", "schdconfigfirst", 
        "schdconfiggetfield", "schdconfignext", "schdconfignumrecords", "schdconfigopen", "schdconfigprev", "schdfirst", "schdnext", 
        "schdnumrecords", "schdopen", "schdprev", "schdspecialadd", "schdspecialclose", "schdspecialdelete", "schdspecialfirst", 
        "schdspecialgetfield", "schdspecialitemadd", "schdspecialitemclose", "schdspecialitemdelete", "schdspecialitemfirst", "schdspecialitemgetfield", "schdspecialitemmodify", 
        "schdspecialitemnext", "schdspecialitemnumrecords", "schdspecialitemopen", "schdspecialitemprev", "schdspecialmodify", "schdspecialnext", "schdspecialnumrecords", 
        "schdspecialopen", "schdspecialprev", "scheduleitemadd", "scheduleitemdelete", "scheduleitemmodify", "scheduleitemsetrepeat", "semclose", 
        "semopen", "semsignal", "semwait", "sendkeys", "serialkey", "serverbrowseclose", "serverbrowsefirst", 
        "serverbrowsegetfield", "serverbrowsenext", "serverbrowsenumrecords", "serverbrowseopen", "serverbrowseprev", "serverdumpkernel", "servergetproperty", 
        "serverinfo", "serverinfoex", "serverisonline", "serverrpc", "serverreload", "serverrestart", "servicegetlist", 
        "setarea", "setevent", "setlanguage", "setlogging", "shutdown", "shutdownform", "shutdownmode", 
        "sign", "sin", "sleep", "sleepms", "sqrt", "strcalcwidth", "strclean", 
        "strfill", "strformat", "strgetchar", "strleft", "strlength", "strlower", "strmid", 
        "strpad", "strright", "strsearch", "strsetchar", "strtochar", "strtodate", "strtofmt", 
        "strtogrp", "strtohex", "strtoint", "strtolines", "strtolocaltext", "strtoperiod", "strtoreal", 
        "strtotime", "strtotimestamp", "strtovalue", "strtrim", "strtruncfont", "strtruncfonthnd", "strupper", 
        "strword", "subscriptionaddcallback", "subscriptiongetattribute", "subscriptiongetinfo", "subscriptiongetquality", "subscriptiongettag", "subscriptiongettimestamp", 
        "subscriptiongetvalue", "subscriptionremovecallback", "switchconfig", "systime", "systimedelta", "tablelookup", "tablemath", 
        "tableshift", "tagbrowseclose", "tagbrowsefirst", "tagbrowsegetfield", "tagbrowsenext", "tagbrowsenumrecords", "tagbrowseopen", 
        "tagbrowseprev", "tagdebug", "tagdebugform", "tageventformat", "tageventqueue", "taggetproperty", "taggetscale", 
        "taginfo", "taginfoex", "tagrdbreload", "tagramp", "tagread", "tagreadex", "tagresolve", 
        "tagscalestr", "tagsetoverridebad", "tagsetoverridegood", "tagsetoverridequality", "tagsetoverrideuncertain", "tagsubscribe", "tagunresolve", 
        "tagunsubscribe", "tagwrite", "tagwriteeventque", "tagwriteintarray", "tagwriterealarray", "tan", "taskcluster", 
        "taskgetsignal", "taskhnd", "taskkill", "tasknew", "tasknewex", "taskresume", "tasksetsignal", 
        "tasksuspend", "testrandomwave", "testsawwave", "testsinwave", "testsquarewave", "testtriangwave", "time", 
        "timecurrent", "timehour", "timeinfo", "timeinttotimestamp", "timemidnight", "timemin", "timesec", 
        "timeset", "timetostr", "timeutcoffset", "timestampadd", "timestampcreate", "timestampcurrent", "timestampdifference", 
        "timestampformat", "timestampgetpart", "timestampsub", "timestamptostr", "timestamptotimeint", "toggle", "tracemsg", 
        "trenddspcursorcomment", "trenddspcursorscale", "trenddspcursortag", "trenddspcursortime", "trenddspcursorvalue", "trendgetan", "trendpopup", 
        "trendrun", "trendsetdate", "trendsetscale", "trendsetspan", "trendsettime", "trendsettimebase", "trendwin", 
        "trendzoom", "trnaddhistory", "trnbrowseclose", "trnbrowsefirst", "trnbrowsegetfield", "trnbrowsenext", "trnbrowsenumrecords", 
        "trnbrowseopen", "trnbrowseprev", "trnclientinfo", "trncompareplot", "trndelhistory", "trndelete", "trnecho", 
        "trneventgettable", "trneventgettablems", "trneventsettable", "trneventsettablems", "trnexportcsv", "trnexportclip", "trnexportdbf", 
        "trnexportdde", "trnflush", "trngetbufevent", "trngetbuftime", "trngetbufvalue", "trngetcluster", "trngetcursorevent", 
        "trngetcursormstime", "trngetcursorpos", "trngetcursortime", "trngetcursorvalue", "trngetcursorvaluestr", "trngetdefscale", "trngetdisplaymode", 
        "trngetevent", "trngetformat", "trngetgatedvalue", "trngetinvalidvalue", "trngetmstime", "trngetmode", "trngetpen", 
        "trngetpencomment", "trngetpenfocus", "trngetpenno", "trngetperiod", "trngetscale", "trngetscalestr", "trngetspan", 
        "trngettable", "trngettime", "trngetunits", "trninfo", "trnisvalidvalue", "trnnew", "trnplot", 
        "trnprint", "trnsamplesconfigured", "trnscroll", "trnselect", "trnsetcursor", "trnsetcursorpos", "trnsetdisplaymode", 
        "trnsetevent", "trnsetpen", "trnsetpenfocus", "trnsetperiod", "trnsetscale", "trnsetspan", "trnsettable", 
        "trnsettime", "usercreate", "usercreateform", "userdelete", "usereditform", "userinfo", "userlogin", 
        "userpassword", "userpasswordexpirydays", "userpasswordform", "usersetstr", "userupdaterecord", "userverify", "variablequality", 
        "variabletimestamp", "verifyprivilegeform", "verifyprivilegetagwrite", "version", "whoami", "wincopy", "winfile", 
        "winfree", "wingetfocus", "wingetwndhnd", "wingoto", "winmode", "winmove", "winnew", 
        "winnewat", "winnext", "winnumber", "winpos", "winprev", "winprint", "winprintfile", 
        "winselect", "winsetname", "winsize", "winstyle", "wintitle", "wndfind", "wndgetfileprofile", 
        "wndgetprofile", "wndhelp", "wndinfo", "wndmonitorinfo", "wndputfileprofile", "wndputprofile", "wndshow", 
        "wndviewer", "xmlclose", "xmlcreate", "xmlgetattribute", "xmlgetattributecount", "xmlgetattributename", "xmlgetattributevalue", 
        "xmlgetchild", "xmlgetchildcount", "xmlgetparent", "xmlgetroot", "xmlnodeaddchild", "xmlnodefind", "xmlnodegetname", 
        "xmlnodegetvalue", "xmlnoderemove", "xmlnodesetvalue", "xmlopen", "xmlsave", "xmlsetattribute", "_objectcallmethod", 
        "_objectgetproperty", "_objectsetproperty", 
    ]
    operator_list = [
        "=", "+", "-", "*", "/", "<", ">", "@", "$", ".",
        "~", "&", "%", "|", "!", "?", "^", ".", ":", "\"",
    ]
    func = Sequence('function', [], ['(', '\n'], styles["Function"], False)
    strseq = Sequence('"', ['"', '\n'], [], styles["String"], True)
    comment = Sequence('//', [], ['\n'], styles["Comment"], True)
    mcomment = Sequence('/*', ['*/'], [], styles["MultilineComment"], True)
    sequence_lists = [strseq, comment, mcomment, func]
    multiline_sequence_list = [mcomment]
    sequence_start_chrs = [x.start for x in sequence_lists]
#    splitter = re.compile(r"(/\*|\*/|\\\"|\(\*|\*\)|//|\n|\"+|\'+|\#+|\s+|\w+|\W)")
    splitter = re.compile(r"(/\*|\*/|\(\*|\*\)|//|\n|\"+|\'+|\#+|\s+|\w+|\W)")
    # Characters that autoindent one level on pressing Return/Enter
    autoindent_characters = ["then", "do", ")"]

    def __init__(self, parent=None):
        """
        Overridden initialization
        """
        # Initialize superclass
        super().__init__()
        # Set the default style values
        self.setDefaultColor(qt.QColor(data.theme["fonts"]["default"]["color"]))
        self.setDefaultPaper(qt.QColor(data.theme["fonts"]["default"]["background"]))
        self.setDefaultFont(data.get_editor_font())
        # Reset autoindentation style
        self.setAutoIndentStyle(0)
        # Set the theme
        self.set_theme(data.theme)
    
    def language(self):
        return "CiCode"
    
    def description(self, style):
        if style < len(self.styles):
            description = "Custom lexer for the CiCode programming languages"
        else:
            description = ""
        return description
    
    def defaultStyle(self):
        return self.styles["Default"]
    
    def braceStyle(self):
        return self.styles["Default"]
    
    def defaultFont(self, style):
        return qt.QFont(data.current_font_name, data.current_font_size)
    
    def set_theme(self, theme):
        for style in self.styles:
            # Papers
            self.setPaper(
                qt.QColor(data.theme["fonts"][style.lower()]["background"]), 
                self.styles[style]
            )
            # Fonts
            lexers.set_font(self, style, theme["fonts"][style.lower()])
    
    def styleText(self, start, end):
        """
        Overloaded method for styling text.
        """
        # Style in pure Python, VERY SLOW!
        editor = self.editor()
        if editor is None:
            return
        # Initialize the styling
        self.startStyling(start)
        # Scintilla works with bytes, so we have to adjust
        # the start and end boundaries
        text = bytearray(editor.text().lower(), "utf-8")[start:end].decode("utf-8")
        # Loop optimizations
        setStyling      = self.setStyling
        DEFAULT         = self.styles["Default"]
        COMMENT         = self.styles["Comment"]
        KEYWORD         = self.styles["Keyword"]
        BUILTINFUNCTION = self.styles["BuiltInFunction"]
        STRING          = self.styles["String"]
        NUMBER          = self.styles["Number"]
        OPERATOR        = self.styles["Operator"]
        # Initialize various states and split the text into tokens
        stringing = False
        commenting = False
        multiline_commenting = False
        sequence = None
        tokens = [
            (token.lower(), len(bytearray(token, "utf-8"))) 
                for token in self.splitter.findall(text)
        ]
        
        # Check if there is a style(comment, string, ...) stretching on from the previous line
        if start != 0:
            previous_style = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            for i in self.multiline_sequence_list:
                if previous_style == i.style:
                    sequence = i
                    break
        
        # Style the tokens accordingly
        for i, token in enumerate(tokens):
            token_name = token[0]
            token_length = token[1]
            if sequence != None:
                if token_name in sequence.stop_sequences:
                    if sequence.add_to_style == True:
                        setStyling(token_length, sequence.style)
                    else:
                        setStyling(token_length, self.styles["Default"])
                    sequence = None
                elif any(ch in token_name for ch in sequence.stop_characters):
                    if sequence.add_to_style == True:
                        setStyling(token_length, sequence.style)
                    else:
                        setStyling(token_length, self.styles["Default"])
                    sequence = None
                else:
                    setStyling(token_length, sequence.style)
            elif token_name in self.sequence_start_chrs:
                for i in self.sequence_lists:
                    if token_name == i.start:
                        if i.stop_sequences == [] and i.stop_characters == []:
                            # Skip styling if both stop sequences and stop characters are empty
                            setStyling(token_length, i.style)
                        else:
                            # Style the sequence and store the reference to it
                            sequence = i
                            if i.add_to_style == True:
                                setStyling(token_length, sequence.style)
                            else:
                                if token_name in self.keyword_list:
                                    setStyling(token_length, KEYWORD)
                                elif token_name in self.type_list:
                                    setStyling(token_length, KEYWORD)
                                elif token_name in self.operator_list:
                                    setStyling(token_length, OPERATOR)
                                elif token_name[0].isdigit():
                                    setStyling(token_length, NUMBER)
                                elif token_name in self.builtin_function_list:
                                    setStyling(token_length, BUILTINFUNCTION)
                                else:
                                    setStyling(token_length, self.styles["Default"])
                        break
            elif token_name in self.keyword_list:
                setStyling(token_length, KEYWORD)
            elif token_name in self.type_list:
                setStyling(token_length, KEYWORD)
            elif token_name in self.operator_list:
                setStyling(token_length, OPERATOR)
            elif token_name[0].isdigit():
                setStyling(token_length, NUMBER)
            elif token_name in self.builtin_function_list:
                setStyling(token_length, BUILTINFUNCTION)
            else:
                setStyling(token_length, DEFAULT)
