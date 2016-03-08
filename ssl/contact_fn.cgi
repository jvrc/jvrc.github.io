#!/usr/bin/perl

require 'cgi-lib.pl';
require 'jcode.pl';

&ReadParse(*in);

$name = $in{'name'};
$shozoku = $in{'shozoku'};
$mail = $in{'mail'};
$naiyo = $in{'naiyo'};

$date = $in{'date'};
$ip = $in{'ip'};

$owFlag = 0;

$etr_log = "\"$date\",\"$ip\",\"$name\",\"$shozoku\",\"$mail\",\"$naiyo\",,,,\n";

open(FILE,"./jvrc_log/jvrc_con.csv")||die "Can't open file";
flock(FILE,2);
@etr_log_body=<FILE>;
flock(FILE,8);
close(FILE);

foreach $line(@etr_log_body){
	if($line eq $etr_log){
		$owFlag = 1;
	}
}


if($owFlag == 0){

	$num = unshift (@etr_log_body, $etr_log);

	open(FILE, ">./jvrc_log/jvrc_con.csv")||die "Can't open file";
	flock(FILE,2);
	print FILE @etr_log_body;
	flock(FILE,8);
	close(FILE);

	$printdate = " ��  ���⍇������  �� $date \n";
	$printname = " ��     ��  ��     �� $name \n";
	$printshozoku = " ���������i�Ζ���j�� $shozoku \n";
	$printmail = " �� ���[���A�h���X �� $mail \n";
	$printnaiyo = " ��  ���⍇�����e  �� $naiyo \n";

	$topbody = "����������������������������������������������������������������������\n\n�W���p���o�[�`�������{�e�B�N�X�`�������W(JVRC)\n\n����������������������������������������������������������������������\n���⍇���A���肪�Ƃ��������܂����B\n\n�ȉ��̓��e���u�W���p���o�[�`�������{�e�B�N�X�`�������W�v�����ǂɑ��M����܂����B\n\n";$middlebody = "$printdate$printname$printshozoku$printmail$printnaiyo\n\n";
	
	$bottombody = "����������������������������������������������������������������������\n\n���@���F2015�N�i����27�N�j10��7���`10��10��\n��@��FCEATEC JAPAN 2015\n�Q����F����\n\n�W���p���o�[�`�������{�e�B�N�X�`�������W������\nhttp://www.jvrc.org/\ninquiry\@jvrc.org\n\n����������������������������������������������������������������������\n\n�����͂��ꂽ�l���́A�����̂��₢�����ȊO�ł͎g�p�v���܂���B\n\�@\���M�͂r�r�k�i�Í����ʐM�j�ŕی삳��Ă��܂��B";
	$send = "\"�uJapan Virtual Robotics Challenge(JVRC)�v������\"<inquiry\@jvrc.org>";
	$subject = "�u�W���p���o�[�`�������{�e�B�N�X�`�������W�v���⍇��";
	$body = "$topbody$middlebody$bottombody";

	jcode::convert(\$subject,'jis');
	jcode::convert(\$body,'jis');
	jcode::convert(\$send,'jis');

	open(MAIL,"| /usr/sbin/sendmail -t");
	print MAIL "To: $mail\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);
#��͓��͎҈��A���͎����ǈ���������������������������������
    open(MAIL,"| /usr/sbin/sendmail -t");
	print MAIL "To: inquiry\@jvrc.org\n";
#	print MAIL "To: e.imabayashi\@adthree.com\n";
#	print MAIL "To: mmm\@s-vivid.com\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);

}

print "Content-type: text/html\n\n";
#print "Content-type: text/html; charset=Shift_JIS\n\n";

	print <<EOM;


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja" dir="ltr">
<head>
<meta http-equiv="content-type" content="text/html; charset=Shift_JIS" />
<title>�W���p���o�[�`�������{�e�B�N�X�`�������W</title>
<meta http-equiv="content-style-type" content="text/css" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="keywords" content="�W���p���o�[�`�������{�e�B�N�X�`�������W,Japan Virtual Robotics Challenge,JVRC,���������J���@�l�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\,NEDO," />
<meta name="description" content="�u�W���p���o�[�`�������{�e�B�N�X�`�������W�iJapan Virtual Robotics Challenge�j�v�i����JVRC�j�͍��������J���@�l�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\ (NEDO) �����{���́u���E��Õ���̍��ی����J���E���؃v���W�F�N�g�^���{�b�g����̍��ی����J���E���؎��Ɓ^�ЊQ�Ή����{�b�g�����J���i�A�����J�j�v�v���W�F�N�g�̈�Ƃ��Ď��{����ЊQ�Ή����{�b�g�̃R���s���[�^�V�~�����[�V�����ɂ�鋣�Z��ł��B" />

<link rel="shortcut icon" href="../images/favicon.ico" />

<link href="../css/import.css" rel="stylesheet" type="text/css" media="all" />
<link href="style_info.css" rel="stylesheet" type="text/css" media="all" />
<script type="text/javascript" src="../js/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="../js/base.js"></script>

</head>


<body>

<div id="page">

<div id="header">
<div class="imgArea">
<a href="http://jvrc.org/index.html">
<img src="../images/img-main.png" alt="���C���C���[�W" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/en/ssl/contact.html"><img src="../images/en_flag.png" alt="english" width="21" height="14" />English</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<ul id="dropmenu">
<li><a href="http://jvrc.org/index.html">TOP&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/about.html">�i�u�q�b�ɂ���</a></li>
  </ul>
</li>
<li><a href="http://jvrc.org/rule.html">���Z���[��&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/tech-guide.html">JVRC�e�N�j�J���K�C�h</a></li>
  </ul>
</li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">�`���[�g���A��</a></li>
<li><a href="http://jvrc.org/team.html">�`�[���Љ�</a></li>
<li><a href="http://jvrc.org/download.html">�_�E�����[�h</a></li>
<li><a href="http://jvrc.org/result.html">�i�s�󋵁E����</a></li>
<li><a href="http://jvrc.org/faq.html">�悭���邲����(FAQ)</a></li>
<li class="current-page"><a href="https://jvrc.org/ssl/contact.html"><img src="../images/inquiry-icon.png" alt="" width="22" height="16" />&nbsp;���₢���킹&nbsp;<img src="../images/sankaku.png" alt="" width="8" height="6" /></a>
  <ul>
  <li><a href="https://jvrc.org/ssl/etr.html"><img src="../images/sanka-icon.png" alt="" width="26" height="21" />&nbsp;�Q���\����</a></li>
  </ul>
</li>
</ul>
<!-- / #navi --></div>

<div id="contents" class="clearfix">
<div id="main2">


<h2>���₢��������</h2>
<br />
<div class="need2">
<span class="red">�ȉ��̓��e�𑗐M���܂����B</span></div>
  
                    
<table class="form" summary="���₢���킹">
<tr>
<th width="17%" nowrap="nowrap" class="t_top">�����O</th>
<td width="6%" class="aqua"><div class="need">�K�{</div></td>
<td width="77%" class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">��������i�Ζ���j</th>
<td><div class="need">�K�{</div></td>
<td>$shozoku</td>
</tr>
<tr>
<th nowrap="nowrap">���[���A�h���X</th>
<td><div class="need">�K�{</div></td>
<td>$mail</td>
</tr>
<tr>
<th nowrap="nowrap">���₢���킹���e</th>
<td><div class="need">�K�{</div></td>
<td>$naiyo</td>
</tr>
</table>

<br />


<div class="line">�@</div>

<div>
<dl class="sign" id="ssl">
<!--
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja"><a href="http://jp.globalsign.com/" target="_blank"><img alt="SSL�@�O���[�o���T�C���̃T�C�g�V�[��" border="0" id="ss_img" src="//seal.globalsign.com/SiteSeal/images/gs_noscript_100-50_ja.gif"></a></span><script type="text/javascript" src="//seal.globalsign.com/SiteSeal/gs_flash_100-50_ja.js"></script></dt>
-->
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>
<dd style="height:50px;">�����L���������l���́A���АӔC�̉��ŊǗ����A�{���ȊO�̖ړI�ł͎g�p�v���܂���B</dd>
</dl>
</div>

</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../images/go-top.png" alt="�g�b�v��" width="88" height="38" /></a></div>

<div id="footer">
<div class="sponsor alpha">��ÁF<a href="http://www.nedo.go.jp/" target="_blank"><img src="../images/nedo-logo.png" alt="���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\" width="60" height="31"/></a>�@���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@\�\\ �@�@�@�@���ÁF<a href="http://www.meti.go.jp/" target="_blank"><img src="../images/keizai-logo.png" alt="�o�ώY�Ə�" width="111" height="33" /></a>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>

</body>
</html>

EOM
exit;