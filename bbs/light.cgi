#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� light.cgi - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './init.cgi';
require $jcode;

&decode;
&setfile;
if ($in{'regist'}) {
	require $registpl;
	&regist;
} elsif ($mode eq "editlog") {
	require $editpl;
	&editlog;
} elsif ($mode eq "delelog") {
	require $editpl;
	&delelog;
} elsif ($mode eq "past" && $pastkey) {
	require $pastpl;
	require $searchpl;
	&pastlog;
} elsif ($mode eq "check") {
	require $checkpl;
	&check;
} elsif ($mode eq "howto") {
	&howto;
} elsif ($mode eq "find") {
	&find;
}
&viewlog;

#-------------------------------------------------
#  �L���\��
#-------------------------------------------------
sub viewlog {
	# ���X�����y�[�W����F��
	my ($res, $page);
	foreach ( keys(%in) ) {
		if (/^res(\d+)$/) {
			$res = $1;
			last;
		} elsif (/^page(\d+)$/) {
			$page = $1;
			last;
		}
	}

	# �N�b�L�[�擾
	my ($cnam, $ceml, $curl, $cpwd) = &get_cookie;
	if (!$curl) { $curl = "http://"; }

	# �^�C�g���\��
	&header;
	print "<div align=\"center\">\n";
	if ($t_img) {
		print "<img src=\"$t_img\" alt=\"$title\" alt=\"$title\">\n";
	} else {
		print "<b style=\"color:$t_col; font-size:$t_size";
		print "px; font-family:'$t_face'\">$title</b>\n";
	}

	# �\���J�n
	print <<"EOM";
<hr width="90%">
[<a href="$home" target="_top">�g�b�v�ɖ߂�</a>]
[<a href="$bbscgi?mode=howto">���ӎ���</a>]
[<a href="$bbscgi?mode=find">���[�h����</a>]
EOM

	# �ߋ����O�����N
	print "[<a href=\"$bbscgi?mode=past\">�ߋ����O</a>]\n" if ($pastkey);

	# ���O�ҏW�@�\�̃����N
	print "[<a href=\"$admincgi\">�Ǘ��p</a>]\n";

	# �ԐM���[�h
	my ($resub, $recom);
	if ($res) {

		# ���p�L�����o
		open(IN,"$logfile");
		while (<IN>) {
			my ($no,$dat,$nam,$eml,$sub,$com) = split(/<>/);

			if ($res == $no) {

				# �R�����g�Ɉ��p���t��
				$recom = "&gt; $com";
				$recom =~ s/<br>/\n&gt; /g;

				# �薼�Ɉ��p���ڕt��
				$sub =~ s/^Re://;
				$resub = "Re:[$res] $sub";

				last;
			}
		}
		close(IN);
	}

	# ���e�t�H�[��
	print <<EOM;
<hr width="90%"></div>
<form method="post" action="$bbscgi">
<blockquote>
<table cellpadding="1" cellspacing="1">
<tr>
  <td><b>���Ȃ܂�</b></td>
  <td><input type="text" name="name" size="28" value="$cnam"></td>
</tr>
<tr>
  <td><b>�d���[��</b></td>
  <td><input type="text" name="email" size="28" value="$ceml"></td>
</tr>
<tr>
  <td><b>�^�C�g��</b></td>
  <td><input type="text" name="sub" size="36" value="$resub">
	<input type="submit" name="regist" value="���e����"><input type="reset" value="���Z�b�g"></td>
</tr>
<tr>
  <td colspan="2"><b>�R�����g</b><br>
  <textarea cols="56" rows="7" name="comment">$recom</textarea></td>
</tr>
<tr>
  <td><b>�Q�Ɛ�</b></td>
  <td><input type="text" size="50" name="url" value="$curl"></td>
</tr>
EOM

	# ���e�L�[
	if ($regist_key) {
		require $regkeypl;
		my ($str_plain,$str_crypt) = &pcp_makekey;

		print qq|<tr><td><b>���e�L�[</b></td>|;
		print qq|<td><input type="text" name="regikey" size="6" style="ime-mode:inactive" value="">\n|;
		print qq|�i���e�� <img src="$registkeycgi?$str_crypt" align="absmiddle" alt="���e�L�["> ����͂��Ă��������j</td></tr>\n|;
		print qq|<input type="hidden" name="str_crypt" value="$str_crypt">\n|;
	}

	print <<EOM;
<tr>
  <td><b>�p�X���[�h</b></td>
  <td><input type="password" name="pwd" size="8" maxlength="8" value="$cpwd">
  �i�L�������e�p�j</td>
</tr>
</table>
</blockquote>
<dl>
EOM

	# �L���W�J
	my $i = 0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { next; }

		my ($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);

		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color="$refcol">$2<\/font>/g;
		$com .= "<p><a href=\"$url\" target=\"_blank\">$url</a>" if ($url);

		# �L���ҏW
		print "<dt><hr>[<b>$no</b>] <b style=\"color:$subcol\">$sub</b> ";
		print "���e�ҁF<b>$nam</b> ���e���F$dat &nbsp;";
		print "<input type=\"submit\" name=\"res$no\" value=\"�ԐM\"><br><br>\n";
		print "<dd>$com<br><br>\n";
	}
	close(IN);

	print "<dt><hr></dl>\n";

	# �J��z���y�[�W��`
	my $next = $page + $plog;
	my $back = $page - $plog;

	my $flg;
	if ($back >= 0) {
		$flg = 1;
		print qq|<input type="submit" name="page$back" value="�O�y�[�W">\n|;
	}
	if ($next < $i) {
		$flg = 1;
		print qq|<input type="submit" name="page$next" value="���y�[�W">\n|;
	}

	# �y�[�W�ړ��{�^���\��
	if ($flg) {
		my ($x, $y) = (1, 0);
		while ( $i > 0 ) {
			if ($page == $y) {
				print "<b>[$x]</b>\n";
			} else {
				print "[<a href=\"$bbscgi?page$y=val\">$x</a>]\n";
			}
			$x++;
			$y += $plog;
			$i -= $plog;
		}
	}
	print <<"EOM";
</form>
<div align="center">
<form action="$bbscgi" method="post">
���� <select name="mode">
<option value="editlog">�C��
<option value="delelog">�폜</select>
�L��No<input type="text" name="no" size="3" style="ime-mode:inactive">
�Ï؃L�[<input type="password" name="pwd" size="6" maxlength="8">
<input type="submit" value="���M"></form>
<!-- ���쌠�\\�L:�폜�֎~($ver) -->
<span style="font-size:10px;font-family:Verdana,Helvetica">
- <a href="http://www.kent-web.com/" target="_top">LightBoard</a> -
</span></div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  ���ӎ���
#-------------------------------------------------
sub howto {
	&header;
	print <<EOM;
<div align="center">
<table border="1" width="85%" cellpadding="15">
<tr><td class="r">
<h3>�f�����p��̒���</h3>
<ol>
<li>���̌f����<b>�N�b�L�[�Ή�</b>�ł��B1�x�L���𓊍e���������ƁA���Ȃ܂��A�d���[���A�t�q�k�A�Ï؃L�[�̏���2��ڈȍ~�͎������͂���܂��B�i���������p�҂̃u���E�U���N�b�L�[�Ή��̏ꍇ�j
<li>���e���e�ɂ́A<b>�^�O�͈�؎g�p�ł��܂���B</b>
<li>�L���𓊍e�����ł̕K�{���͍��ڂ�<b>�u���Ȃ܂��v</b>��<b>�u���b�Z�[�W�v</b>�ł��B�d���[���A�t�q�k�A�薼�A�Ï؃L�[�͔C�ӂł��B
<li>�L���ɂ́A<b>���p�J�i�͈�؎g�p���Ȃ��ŉ������B</b>���������̌����ƂȂ�܂��B
<li>�L���̓��e����<b>�Ï؃L�[</b>�i�p������8�����ȓ��j�����Ă����ƁA���̋L���͎���Ï؃L�[�ɂ���č폜���邱�Ƃ��ł��܂��B
<li>�L���̕ێ������͍ő�<b>$max��</b>�ł��B����𒴂���ƌÂ����Ɏ����폜����܂��B
<li>�����̋L���ɊȒP��<b>�u�ԐM�v</b>���邱�Ƃ��ł��܂��B�e�L���ɂ���<b>�u�ԐM�v�{�^��</b>�������Ɠ��e�t�H�[�����ԐM�p�ƂȂ�܂��B
<li>�ߋ��̓��e�L������<b>�u�L�[���[�h�v�ɂ���ĊȈՌ������ł��܂��B</b>�g�b�v���j���[��<a href="$bbscgi?mode=find">�u���[�h�����v</a>�̃����N���N���b�N����ƌ������[�h�ƂȂ�܂��B
<li>�Ǘ��҂��������s���v�Ɣ��f����L���⑼�l���排�������L���͗\\���Ȃ��폜���邱�Ƃ�����܂��B
</ol>
</td></tr>
</table>
<form>
<input type="button" value="�f���ɖ߂�" onclick="history.back()">
</form>
</div>
</body>
</html>
EOM

	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub find {
	&header;
	print <<EOM;
<form action="$bbscgi">
<input type="submit" value="�f���ɖ߂�">
</form>
<ul>
<li>����������<b>�L�[���[�h</b>����͂��A�u�����v�u�\\���v��I�����āu�����v�{�^���������ĉ������B
<li>�L�[���[�h�͔��p�X�y�[�X�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B
</ul>
<table>
<tr>
EOM

	require $searchpl;
	&search($logfile);
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  �N�b�L�[�擾
#-------------------------------------------------
sub get_cookie {
	# �N�b�L�[���擾
	my $cook = $ENV{'HTTP_COOKIE'};

	# �Y��ID�����o��
	my %cook;
	foreach ( split(/;/, $cook) ) {
		my ($key, $val) = split(/=/);

		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# �f�[�^��URL�f�R�[�h���ĕ���
	my @cook;
	foreach ( split(/<>/, $cook{'LIGHT_BOARD'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		push(@cook,$_);
	}
	return @cook;
}

#-------------------------------------------------
#  ���������N
#-------------------------------------------------
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(https?\:[\w\.\~\-\/\?\&\=\@\;\#\:\%]+)/$1<a href=\"$2\" target=\"_top\">$2<\/a>/g;
}


