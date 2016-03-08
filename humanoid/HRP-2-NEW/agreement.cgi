#!/usr/bin/perl

use CGI::Carp qw(fatalsToBrowser);

require 'cgi-lib.pl';

&ReadParse(*in);


if (&MethPost()) {
    foreach $x (%in) {
        $value = $in{$x};
        $value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
		$value =~ s/&/&amp;/g;
		$value =~ s/"/&quot;/g;
		$value =~ s/</&lt;/g;
		$value =~ s/>/&gt;/g;
		$value =~ s/,/�A/g;
        $in{$x} = $value;
    }
}



$name = $in{'name'};
$shozoku = $in{'shozoku'};
$mail = $in{'mail'};



($sec, $min, $hour, $mday, $mon, $year, $wday, $yday, $isdst) = localtime(time);
$month = $mon+1;
$year+=1900;
$date = "$year�N$month��$mday��$hour��$min��$sec�b";
$ip = $ENV{"REMOTE_ADDR"};


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

<link rel="shortcut icon" href="../../images/favicon.ico" />

<link href="../../css/import.css" rel="stylesheet" type="text/css" media="all" />
<link href="style_agreement.css" rel="stylesheet" type="text/css" media="all" />
<script type="text/javascript" src="../../js/jquery-1.7.1.min.js"></script>
<script type="text/javascript" src="../../js/base.js"></script>

</head>
<body>

<div id="page">

<div id="header">
<div class="imgArea">
<a href="http://jvrc.org/index.html">
<img src="../../images/img-main.png" alt="���C���C���[�W" width="1115" height="313" /></a>


<div class="english"><a href="https://jvrc.org/en/download.html"><img src="../../images/en_flag.png" alt="english" width="21" height="14" />English</a>
</div><!--/ english-->

</div><!-- / #imgArea -->
</div><!-- / #header -->


<div id="navi">
<ul id="dropmenu">
<li><a href="http://jvrc.org/index.html">TOP&nbsp;<img src="../../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/about.html">�i�u�q�b�ɂ���</a></li>
  </ul>
</li>
<li><a href="http://jvrc.org/rule.html">���Z���[��&nbsp;<img src="../../images/sankaku.png" alt="" width="8" height="6"/></a>
  <ul class="mainNav">
  <li><a href="http://jvrc.org/tech-guide.html">JVRC�e�N�j�J���K�C�h</a></li>
  </ul>
</li>
<li><a href="http://jvrc.github.com/tutorials/html-ja/index.html" target="_blank">�`���[�g���A��</a></li>
<li><a href="http://jvrc.org/team.html">�`�[���Љ�</a></li>
<li class="current-page"><a href="http://jvrc.org/download.html">�_�E�����[�h</a></li>
<li><a href="http://jvrc.org/result.html">�i�s�󋵁E����</a></li>
<li><a href="http://jvrc.org/faq.html">�悭���邲����(FAQ)</a></li>
<li><a href="https://jvrc.org/ssl/contact.html"><img src="../../images/inquiry-icon.png" alt="" width="22" height="16" />&nbsp;���₢���킹&nbsp;<img src="../../images/sankaku.png" alt="" width="8" height="6" /></a>
  <ul>
  <li><a href="https://jvrc.org/ssl/etr.html"><img src="../../images/sanka-icon.png" alt="" width="26" height="21" />&nbsp;�Q���\����</a></li>
  </ul>
</li>
</ul>
<!-- / #navi --></div>

<div id="contents" class="clearfix">
<div id="main2">

<h2>�_�E�����[�h\�\\�����݊m�F</h2>
<br />
<div class="need2">
<span class="red">�ȉ��̓��e�ɂ��ԈႢ���Ȃ���΁y��\�\\�����݂���������z�{�^���������Ă��������B</span>
</div>

<table class="form" summary="�_�E�����[�h\�\\������">
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
</table>

<br />

<div class="t-center">
<form method="post" action="https://jvrc.org/humanoid/HRP-2-NEW/agreement_fn.cgi" name="thisform" onsubmit='return checkForm()'>
<input type=button value=" �� �� " onClick="javascript:history.back()">�@<input type=submit value="��\�\\�����݂���������">
<input type=hidden name="name" value="$name">
<input type=hidden name="shozoku" value="$shozoku">
<input type=hidden name="mail" value="$mail">								
<input type=hidden name="date" value="$date">
<input type=hidden name="ip" value="$ip">
</form>
</div>
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
<a href="#"><img src="../../images/go-top.png" alt="�g�b�v��" width="88" height="38" /></a></div>

<div id="footer">
<div class="sponsor alpha">��ÁF<a href="http://www.nedo.go.jp/" target="_blank"><img src="../../images/nedo-logo.png" alt="���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@�\" width="60" height="31"/></a>�@���������J���@�l�@�V�G�l���M�[�E�Y�ƋZ�p�����J���@\�\\ �@�@�@�@���ÁF<a href="http://www.meti.go.jp/" target="_blank"><img src="../../images/keizai-logo.png" alt="�o�ώY�Ə�" width="111" height="33" /></a>
</div>
<div class="copyright">Copyright &copy; 2015 Japan Virtual Robotics Challenge. All Rights Reserved.</div>
<!-- / #footer --></div>

<!-- / #page --></div>


</body>
</html>

EOM
exit;