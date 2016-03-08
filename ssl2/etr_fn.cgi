#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);

require 'cgi-lib.pl';
require 'jcode.pl';

&ReadParse(*in);

$name = $in{'name'};
$kana = $in{'kana'};
$team = $in{'team'};
$kinmu = $in{'kinmu'};
$yakushoku = $in{'yakushoku'};
$yubin = $in{'yubin'};
$todoufuken = $in{'todoufuken'};
$jusho_1 = $in{'jusho_1'};
$jusho_2 = $in{'jusho_2'};
$tel = $in{'tel'};
$fax = $in{'fax'};
$mail = $in{'mail'};
$date = $in{'date'};
$ip = $in{'ip'};

$owFlag = 0;

$etr_log = "\"$date\",\"$ip\",\"$name\",\"$kana\",\"$team\",\"$kinmu\",\"$yakushoku\",\"$yubin\",\"$todoufuken\",\"$jusho_1\",\"$jusho_2\",\"$tel\",\"$fax\",\"$mail\",,,,\n";

open(FILE,"./jvrc_log/jvrc_etr.csv")||die "Can't open file";
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

	open(FILE, ">./jvrc_log/jvrc_etr.csv")||die "Can't open file";
	flock(FILE,2);
	print FILE @etr_log_body;
	flock(FILE,8);
	close(FILE);

	$printdate = " ����\�\\�����ݓ����� $date \n";
	$printname = " ��   �� �� �O   �� $name \n";
	$printkana = " ��   �t���K�i   �� $kana \n";
	$printteam = " ��   �`�[����   �� $team \n";
	$printkinmu = " ��   �� �� ��   �� $kinmu \n";
	$printyakushoku = " ��    �� �E     �� $yakushoku \n";
	$printyubin = " ��   �X�֔ԍ�   �� $yubin \n";
	$printtodoufuken = " ��   �s���{��   �� $todoufuken \n";
	$printjusho_1 = " ��   �Z �� �P   �� $jusho_1 \n";
	$printjusho_2 = " ���Z���Q�i�A�p�[�g�A�r�����Ȃǁj�� $jusho_2 \n";
	$printtel = " ��   �d�b�ԍ�   �� $tel \n";
	$printfax = " ��    �e�`�w    �� $fax \n";
	$printmail = " �����[���A�h���X�� $mail \n";			

	$topbody = "����������������������������������������������������������������������\n\n�W���p���o�[�`�������{�e�B�N�X�`�������W(JVRC)\n\n����������������������������������������������������������������������\n�ȉ��̓��e���u�W���p���o�[�`�������{�e�B�N�X�`�������W�v�����ǂɑ��M����܂����B\n\n";
	$middlebody = "$printdate$printname$printkana$printteam$printkinmu$printyakushoku$printyubin$printtodoufuken$printjusho_1$printjusho_2$printtel$printfax$printmail\n\n";
	$bottombody = "����������������������������������������������������������������������\n\n���@ ���F2015�N�i����27�N�j10����{ �ڂ����̓z�[���y�[�W�ł��m�点���܂��B\n��@ ��FCEATEC�i\�\\��j\n�Q����F����\n\n�Q���葱���̏ڍׂɂ��Ă͌���A�^�c�����ǂ�育�A���v���܂��B\n\n�W���p���o�[�`�������{�e�B�N�X�`�������W������\�@\������ЃA�h�X���[��\nhttps://jvrc.org/\n�s�d�k 03(5925)2840\�@\�e�`�w 03(5925)2913\n�d���[�� office\@jvrc.org\n\n����������������������������������������������������������������������\n\n�����͂��ꂽ�l���́A�����Q��\�\\�����݈ȊO�ł͎g�p���܂���B\n\�@\���M�͂r�r�k�i�Í����ʐM�j�ŕی삳��Ă��܂��B";
	$send = "\"�u�W���p���o�[�`�������{�e�B�N�X�`�������W�v������\"<office\@jvrc.org>";
	$subject = "�u�W���p���o�[�`�������{�e�B�N�X�`�������W�v�Q��\�\\��";
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
	print MAIL "To: office\@jvrc.org\n";
#	print MAIL "To: e.imabayashi\@adthree.com\n";
	print MAIL "From: $send\n";
	print MAIL "Subject: $subject\n";
	print MAIL "Content-Type: text/plain;\n\n";
	print MAIL "$body\n";
	close(MAIL);


}

print "Content-type: text/html\n\n";

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
<a href="../index.html">
<img src="../images/img-main.png" alt="���C���C���[�W" width="1115" height="313" /></a>

<div class="english"><a href="https://jvrc.org/en/ssl/etr.html"><img src="../images/en_flag.png" alt="english" width="21" height="14" />English</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<div id="naviArea">
<ul id="gNav">
<li><a href="../index.html">TOP</a></li>
<li><a href="../rule.html">���Z���[��</a></li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">�`���[�g���A��</a></li>
<li><a href="../team.html">�`�[���Љ�</a></li>
<li><a href="../download.html">�_�E�����[�h</a></li>
<li><a href="../result.html">�i�s�󋵁E����</a></li>
<li class="current-page"><a href="etr.html"><img src="../images/sanka-icon.png" alt="" width="26" height="25" /> �Q��\�\\����</a></li>
<li><a href="contact.html"><img src="../images/inquiry-icon.png" alt="" width="22" height="16" /> ���₢���킹</a></li>
</ul>
<!-- / #naviArea --></div>
<!-- / #navi --></div>


<div id="contents" class="clearfix">
<div id="main2">

<h2>�Q��\�\\���݊���</h2>
<br />

<div class="need2">
<span class="red">�ȉ��̓��e�𑗐M���܂����B�T���̃��[�������m�F���������B</span><br />
<br /> 
</div>
                 
<table class="form" summary="��\�\\����">
<tr>
<th nowrap="nowrap" class="t_top">�����O</th>
<td width="6%" class="aqua"><div class="need">�K�{</div></td>
<td class="t_top">$name</td>
</tr>
<tr>
<th nowrap="nowrap">�t���K�i</th>
<td><div class="need">�K�{</div></td>
<td>$kana</td>
</tr>
<tr>
<th nowrap="nowrap">�`�[����</th>
<td>&nbsp;</td>
<td>$team</td>
</tr>
<tr>
<th nowrap="nowrap">������</th>
<td>&nbsp;</td>
<td>$kinmu</td>
</tr>
<tr>
<th nowrap="nowrap">��E</th>
<td>&nbsp;</td>
<td>$yakushoku</td>
</tr>
<tr>
<th nowrap="nowrap">�X�֔ԍ�</th>
<td>&nbsp;</td>
<td>$yubin</td>
</tr>
<tr>
<th nowrap="nowrap">�s���{��</th>
<td>&nbsp;</td>
<td>$todoufuken</td>
</tr>
<tr>
<th nowrap="nowrap">�Z���P</th>
<td>&nbsp;</td>
<td>$jusho_1</td>
</tr>
<tr>
<th nowrap="nowrap">�Z���Q<br />�i�r�����Ȃǁj</th>
<td>&nbsp;</td>
<td>$jusho_2</td>
</tr>
<tr>
<th nowrap="nowrap">�d�b�ԍ�</th>
<td>&nbsp;</td>
<td>$tel</td>
</tr>
<tr>
<th nowrap="nowrap">�e�`�w</th>
<td>&nbsp;</td>
<td>$fax</td>
</tr>
<tr>
<th nowrap="nowrap">���[���A�h���X</th>
<td><div class="need">�K�{</div></td>
<td>$mail</td>
</tr>
</table>
<br />

<div class="line">�@</div>

<div>
<dl class="sign" id="ssl">
<dt style="height:50px;"><span id="ss_img_wrapper_100-50_flash_ja">
<script language="JavaScript" TYPE="text/javascript" src="https://trusted-web-seal.cybertrust.ne.jp/seal/getScript?host_name=jvrc.org&type=48&svc=4&cmid=2012706"></script><br />
</span></dt>

<dd style="height:50px;">�����L���������l���́A���АӔC�̉��ŊǗ����A�{���ȊO�̖ړI�ł͎g�p�v���܂���B
</dd>
</dl>
</div>


</div><!--main2-->
</div><!-- / #contents -->


<div class="pageTop alpha">
<a href="#"><img src="../images/go-top.png" alt="�g�b�v��" width="88" height="38" /></a></div>

<div id="footer">
<div class="sponsor alpha">��ÁF<a href="http://www.nedo.go.jp/" target="_blank"><img src="../images/nedo-logo.png" alt="���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\" width="60" height="31"/></a>�@���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\ �@�@�@�@���ÁF<a href="http://www.meti.go.jp/" target="_blank"><img src="../images/keizai-logo.png" alt="�o�ώY�Ə�" width="111" height="33" /></a>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>

</body>
</html>

EOM
exit;