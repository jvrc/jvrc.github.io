#!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� admin.cgi - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# �O���t�@�C����荞��
require './init.cgi';
require $jcode;

&decode;
&setfile;
&auth_check;
if ($in{'log_mente'}) { &log_mente; }
elsif ($in{'set_up'}) { &set_up; }
elsif ($in{'aprv_log'}) { &aprv_log; }
elsif ($in{'chg_pwd'}) { &chg_pwd; }
&admin_menu;

#-------------------------------------------------
#  �Ǘ����[�h
#-------------------------------------------------
sub admin_menu {
	&header;
	print <<EOM;
<div align="right">
<form action="$bbscgi">
<input type="submit" value="���f����">
</form>
</div>
<div align="center">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<table border="1" cellpadding="5" cellspacing="0">
<tr>
	<th bgcolor="#b5b5ff">�I��</th>
	<th width="220" bgcolor="#b5b5ff">��������</th>
</tr><tr>
	<th><input type="submit" name="set_up" value="�I��"></th>
	<td>�ݒ���e�̕ύX</td>
</tr><tr>
	<th><input type="submit" name="log_mente" value="�I��"></th>
	<td>�L�������e�i���X</td>
EOM

	if ($conf_log) {

		print qq|</tr><tr>\n|;
		print qq|<th><input type="submit" name="aprv_log" value="�I��"></th>\n|;
		print qq|<td>�����F�L���̏��F�A�b�v</td>|;
	}

	print <<EOM;
</tr><tr>
	<th><input type="submit" name="chg_pwd" value="�I��"></th>
	<td>�p�X���[�h�̕ύX</td>
</tr>
</table>
</form>
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �L���̃����e�i���X
#-------------------------------------------------
sub log_mente {


	# �폜
	if ($in{'job'} eq "dele" && $in{'no'}) {

		# �폜���
		my %del;
		foreach ( split(/\0/, $in{'no'}) ) {
			$del{$_} = 1;
		}

		# �폜�L���������
		my @data;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no) = split(/<>/);

			if (!defined($del{$no})) {
				push(@data,$_);
			}
		}

		# �X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

	# �C���t�H�[��
	} elsif ($in{'job'} eq "edit" && $in{'no'}) {

		# �L���͂P�̂�
		if ($in{'no'} =~ /\0/) { &error("�C���L���̑I���͂P�݂̂ł�"); }

		local($no,$dat,$nam,$eml,$sub,$com,$url);
		open(IN,"$logfile") || &error("Open Error: $logfile");
		while (<IN>) {
			($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);

			last if ($in{'no'} == $no);
		}
		close(IN);

		&edit_form($no,$dat,$nam,$eml,$sub,$com,$url);

	# �C�����s
	} elsif ($in{'job'} eq "edit2") {

		# ���̓`�F�b�N
		if ($in{'url'} eq "http://") { $in{'url'} = ""; }

		# �f�[�^�I�[�v��
		my @data;
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);

			if ($in{'no'} == $no) {
				$_ = "$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@data,$_);
		}

		# �X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);
	}

	# �Ǘ����
	&header;
	&back_btn;
	print <<EOM;
<p>������I�����đ��M�{�^���������Ă��������B</p>
<form action="$admincgi" method="post">
<input type="hidden" name="log_mente" value="1">
<input type="hidden" name="pass" value="$in{'pass'}">
�����F
<select name="job">
<option value="edit">�C��
<option value="dele">�폜</select>
<input type="submit" value="���M����">
<dl>
EOM

	# �L���W�J
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70) . "...";
		}

		print qq|<dt><hr><input type="checkbox" name="no" value="$no">|;
		print qq|[<b>$no</b>] <b style="color:$subcol">$sub</b> - <b>$nam</b> - $dat|;
		print qq|<dd>$com <font color="$subcol" size="-1">&lt;$hos&gt;</font>\n|;
	}
	close(IN);

	print <<EOM;
<dt><hr>
</dl>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �ݒ菈��
#-------------------------------------------------
sub set_up {

	# �ҏW���s
	if ($in{'submit'}) {

		# �`�F�b�N
		if (!$in{'home'}) { &error('�߂��̓��͂�����܂���'); }
		if (!$in{'max'}) { &error('�ő�L�����̓��͂�����܂���'); }
		if (!$in{'plog'}) { &error('�\�������̓��͂�����܂���'); }
		if (!$in{'b_size'}) { &error('�{�������T�C�Y�̓��͂�����܂���'); }
		if ($in{'t_img'} eq "http://") { $in{'t_img'} = ""; }
		if ($in{'bg'} eq "http://") { $in{'bg'} = ""; }
		$in{'no_wd'} =~ s/�@/ /g;

		# �X�V
		open(OUT,"+> $setfile") || &error("Write Error : $setfile");
		print OUT "$in{'title'}<>$in{'t_col'}<>$in{'t_size'}<>$in{'t_face'}<>$in{'t_img'}<>$in{'bg'}<>$in{'bc'}<>$in{'tx'}<>$in{'li'}<>$in{'vl'}<>$in{'al'}<>$in{'home'}<>$in{'max'}<>$in{'subcol'}<>$in{'refcol'}<>$in{'plog'}<>$in{'b_size'}<>$in{'mail'}<>$in{'deny'}<>$in{'link'}<>$in{'wait'}<>$in{'no_wd'}<>$in{'jp_wd'}<>$in{'urlnum'}<>";
		close(OUT);

		# �������b�Z�[�W
		&header;
		print qq|<div align="center"><h3>�ݒ肪�������܂���</h3>\n|;
		print qq|<form action="$admincgi" method="post">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass'}">\n|;
		print qq|<input type="submit" value="�Ǘ�TOP�ɖ߂�"></form>\n|;
		print qq|</div>\n</body></html>\n|;
		exit;
	}

	$t_img ||= "http://";
	$bg    ||= "http://";
	$home  ||= "http://";
	$b_size =~ s/\D//g;

	&header;
	&back_btn;
	print <<EOM;
<ul>
<li>�C�����镔���̂ݕύX���Ă��������B
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="set_up" value="1">
<table border="0">
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>�^�C�g����</td>
  <td><input type="text" name="title" size="30" value="$title"></td>
</tr><tr>
  <td>�^�C�g���F</td>
  <td>
	<input type="text" name="t_col" size="12" value="$t_col" style="ime-mode:inactive">
	<font color="$t_col">��</font>
  </td>
</tr><tr>
  <td>�^�C�g���T�C�Y</td>
  <td>
	<input type="text" name="t_size" size="5" value="$t_size" style="ime-mode:inactive">
	�s�N�Z��
  </td>
</tr><tr>
  <td>�^�C�g���t�H���g</td>
  <td><input type="text" name="t_face" size="30" value="$t_face" style="ime-mode:inactive"></td>
</tr><tr>
  <td>�^�C�g���摜</td>
  <td>
	<input type="text" name="t_img" size="40" value="$t_img" style="ime-mode:inactive">
	�i�C�Ӂj
  </td>
</tr><tr><td colspan="2"><hr></td></tr>
<tr>
  <td>�ǎ�</td>
  <td>
	<input type="text" name="bg" size="40" value="$bg" style="ime-mode:inactive">
	�i�C�Ӂj
  </td>
</tr><tr>
  <td>�w�i�F</td>
  <td><input type="text" name="bc" size="12" value="$bc" style="ime-mode:inactive">
	<font color="$bc">��</font></td>
</tr>
<tr>
  <td>�����F</td>
  <td><input type="text" name="tx" size="12" value="$tx" style="ime-mode:inactive">
	<font color="$tx">��</font></td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type="text" name="li" size="12" value="$li" style="ime-mode:inactive">
	<font color="$li">��</font> �i���K��j</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type="text" name="vl" size="12" value="$vl" style="ime-mode:inactive">
	<font color="$vl">��</font> �i�K��ρj</td>
</tr>
<tr>
  <td>�����N�F</td>
  <td><input type="text" name="al" size="12" value="$al" style="ime-mode:inactive">
	<font color="$al">��</font> �i�K�⒆�j</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>�L���薼�F</td>
  <td><input type="text" name="subcol" size="12" value="$subcol" style="ime-mode:inactive">
	<font color="$subcol">��</font></td>
</tr>
<tr>
  <td>���p���F</td>
  <td><input type="text" name="refcol" size="12" value="$refcol" style="ime-mode:inactive">
	<font color="$refcol">��</font></td>
</tr>
<tr>
  <td>�߂��</td>
  <td><input type="text" name="home" size="40" value="$home" style="ime-mode:inactive"></td>
</tr>
<tr>
  <td>�ő�L����</td>
  <td><input type="text" name="max" size="5" value="$max" style="ime-mode:inactive"></td>
</tr>
<tr>
  <td>�\\������</td>
  <td><input type="text" name="plog" size="5" value="$plog" style="ime-mode:inactive">
	�i1�y�[�W����̋L���\\�����j</td>
</tr>
<tr>
  <td>�{������</td>
  <td><input type="text" name="b_size" size="5" value="$b_size" style="ime-mode:inactive">
	�s�N�Z��</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>URL�����N</td>
  <td>
EOM

	my @ox = ("���Ȃ�","����");
	foreach (0,1) {
		if ($link == $_) {
			print "<input type=\"radio\" name=\"link\" value=\"$_\" checked>$ox[$_]\n";
		} else {
			print "<input type=\"radio\" name=\"link\" value=\"$_\">$ox[$_]\n";
		}
	}

	print <<EOM;
	&nbsp;�i�L������URL�����������N�j
  </td>
</tr>
<tr>
  <td>URL����</td>
  <td><input type="text" name="urlnum" size="5" value="$urlnum" style="ime-mode:inactive">
	�i���e���A�{���Ɋ܂܂��URL�̌������B0�ɂ���Ƌ@�\\�I�t�j</td>
</tr>
<tr>
  <td>���e�Ԋu</td>
  <td><input type="text" name="wait" size="5" value="$wait" style="ime-mode:inactive"> �b
	�i����z�X�g�̘A�����e����j</td>
</tr>
<tr>
  <td>�p������</td>
  <td>
EOM

	foreach (0,1) {
		if ($jp_wd == $_) {
			print "<input type=\"radio\" name=\"jp_wd\" value=\"$_\" checked>$ox[$_]\n";
		} else {
			print "<input type=\"radio\" name=\"jp_wd\" value=\"$_\">$ox[$_]\n";
		}
	}

	print <<EOM;
	&nbsp;�i�薼�E�{���ɓ��{�ꂪ�܂܂�Ȃ��ꍇ���e���ہj
</tr>
EOM

	if ($sendmail) {
		print "<tr><td colspan=\"2\"><hr></td></tr>\n";
		print "<tr><td>�d���[��</td>";
		print "<td><input type=\"text\" name=\"mail\" size=\"30\" value=\"$mail\"><br>\n";
		print "�i���[���ʒm����ꍇ�j</td></tr>\n";
	}

	print <<"EOM";
<tr><td colspan="2"><hr></td></tr>
<tr>
  <td>���ۃz�X�g</td>
  <td><input type="text" name="deny" size="50" value="$deny">
	�i�X�y�[�X�ŋ�؂�j</td>
</tr>
<tr>
  <td>�֎~���[�h</td>
  <td><input type="text" name="no_wd" size="50" value="$no_wd">
	�i�X�y�[�X�ŋ�؂�j</td>
</tr>
<tr><td colspan="2"><hr></td></tr>
</table>
<input type="submit" name="submit" value="�ݒ���C������"></form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �����F�L���̏��F
#-------------------------------------------------
sub aprv_log {
	# ���F
	if ($in{'job'} eq "aprv" && $in{'no'}) {

		# �Y�����O
		my @log;
		foreach ( split(/\0/, $in{'no'}) ) {
			open(DB,"$tmpdir/$_.cgi");
			my $log = <DB>;
			close(DB);

			unshift(@log,$log);
		}

		# �{�ԃ��O
		local($i, $top, @data, @past);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			$i++;
			if ($i == 1) { $top = $_; }

			# ���s���O
			if ($i < $max - @log) {
				push(@data,$_);

			# �ߋ����O
			} elsif ($pastkey) {
				push(@past,$_);
			}
		}

		# �̔�
		my $num = (split(/<>/, $top))[0];

		# �{�ԃf�[�^�X�V
		foreach (@log) {
			$num++;
			unshift(@data,"$num<>$_\n");
		}

		# �{�ԃf�[�^�X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �ߋ����O�X�V
		if (@past > 0) {
			require $pastmkpl;
			&past_make;
		}

		# �ꎞ���O�폜
		foreach ( split(/\0/, $in{'no'}) ) {
			unlink("$tmpdir/$_.cgi");
		}

	# �폜
	} elsif ($in{'job'} eq "dele" && $in{'no'}) {

		# ���O�폜
		foreach ( split(/\0/, $in{'no'}) ) {
			unlink("$tmpdir/$_.cgi");
		}
	}

	opendir(DIR,"$tmpdir");
	my @dir = readdir(DIR);
	closedir(DIR);

	my @log;
	foreach (@dir) {
		if (/^(\d+)\.cgi$/) {
			push(@log,$1);
		}
	}
	@log = sort{ $b <=> $a }@log;

	# �Ǘ����
	&header;
	&back_btn;
	print <<EOM;
<p>������I�����đ��M�{�^���������Ă��������B</p>
<form action="$admincgi" method="post">
<input type="hidden" name="aprv_log" value="1">
<input type="hidden" name="pass" value="$in{'pass'}">
�����F
<select name="job">
<option value="aprv">���F
<option value="dele">�폜
</select>
<input type="submit" value="���M����">
<dl>
EOM

	foreach (@log) {

		open(DB,"$tmpdir/$_.cgi");
		my $log = <DB>;
		close(DB);

		my ($dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/, $log);
		$nam = "<a href=\"mailto:$eml\">$nam</a>" if ($eml);
		$com =~ s/<([^>]|\n)*>//g;
		if (length($com) > 70) {
			$com = substr($com,0,70) . "...";
		}

		print qq|<dt><hr><input type="checkbox" name="no" value="$_">|;
		print qq|<b style="color:$subcol">$sub</b> - <b>$nam</b> - $dat|;
		print qq|<dd>$com <font color="$subcol" size="-1">&lt;$hos&gt;</font>\n|;
	}

	print <<EOM;
<dt><hr>
</dl>
</form>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub enter_disp {
	&header;
	print <<EOM;
<div align="center">
<h4>�p�X���[�h����͂��Ă�������</h4>
<form action="$admincgi" method="post">
<input type="radio" name="mode" value="admin" checked>�L��
<input type="radio" name="mode" value="setup">�ݒ�<br><br>
<input type="password" name="pass" size="10">
<input type="submit" value=" �F�� ">
</form>
</div>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �������
#-------------------------------------------------
sub back_btn {
	print <<EOM;
<div align="right">
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="submit" value="&lt; ���j���[">
</form>
</div>
EOM
}

#-------------------------------------------------
#  �ҏW�t�H�[��
#-------------------------------------------------
sub edit_form {
	local($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	$url ||= "http://";
	$com =~ s/<br>/\n/g;

	&header;
	print <<EOM;
[<a href="javascript:history.back()">�O��ʂɖ߂�</a>]
<h3>�ҏW�t�H�[��</h3>
<ul>
<li>�C�����镔���̂ݕύX���Ă��������B
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="log_mente" value="1">
<input type="hidden" name="job" value="edit2">
���e�Җ�<br><input type="text" name="name" size="28" value="$nam"><br>
�d���[��<br><input type="text" name="email" size="28" value="$eml"><br>
�^�C�g��<br><input type="text" name="sub" size="36" value="$sub"><br>
�Q�Ɛ�<br><input type="text" name="url" size="45" value="$url"><br>
�R�����g<br><textarea name="comment" cols="58" rows="7">$com</textarea><br>
<input type="submit" value=" �C�����s�� "></form>
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �p�X���[�h�F��
#-------------------------------------------------
sub auth_check {
	# �p�X���[�h�t�@�C������̏ꍇ�͐ݒ��ʂ�
	if (-z $pwdfile) {
		&chg_pwd;
	}

	# �p�X���[�h�����͂̏ꍇ�͓��͉�ʂ�
	if ($in{'pass'} eq "") {
		&pwd_form;
	}

	# �p�X���[�h�ǂݍ���
	open(IN,"$pwdfile");
	my $data = <IN>;
	close(IN);

	# �F��
	if (&decrypt($in{'pass'}, $data) != 1) {
		&error("�F�؂ł��܂���");
	}
}

#-------------------------------------------------
#  �p�X���[�h���͉��
#-------------------------------------------------
sub pwd_form {
	&header;
	print <<EOM;
<div align="center">
<p>�Ǘ��p�X���[�h����͂��Ă�������</p>
<form action="$admincgi" method="post">
<input type="password" name="pass" size="20">
<input type="submit" value="�F��">
</form>
</div>
<script language="javascript">
<!--
self.document.forms[0].pass.focus();
//-->
</script>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �p�X���[�h�ύX
#-------------------------------------------------
sub chg_pwd {
	# �ύX
	if ($in{'submit'}) {

		my $err;
		if ($in{'pass1'} eq "" || $in{'pass2'} eq "") {
			$ere .= "�V�p�X���[�h�������͂ł�<br>";
		}
		if ($in{'pass1'} ne $in{'pass2'}) {
			$err .= "�ēx���͂����p�X���[�h���Ⴂ�܂�<br>";
		}
		if ($err) { &error($err); }

		open(DAT,"+> $pwdfile") || &error("Write Error: $pwdfile");
		print DAT &encrypt($in{'pass1'});
		close(DAT);

		# �������b�Z�[�W
		&header;
		print qq|<div align="center"><h3>�ύX���������܂���</h3>\n|;
		print qq|<form action="$admincgi" method="post">\n|;
		print qq|<input type="hidden" name="pass" value="$in{'pass1'}">\n|;
		print qq|<input type="submit" value="�Ǘ�TOP�ɖ߂�"></form>\n|;
		print qq|</div>\n</body></html>\n|;
		exit;
	}

	&header;
	&back_btn;
	print <<EOM;
<blockquote>
�V�p�X���[�h����͂��Ă�������
<form action="$admincgi" method="post">
<input type="hidden" name="pass" value="$in{'pass'}">
<input type="hidden" name="chg_pwd" value="1">
<table>
<p>���V�p�X���[�h�i�p������8�����ȓ��j<br>
<input type="password" name="pass1" size="20">
</p>
<p>���ēx����<br>
<input type="password" name="pass2" size="20">
</p>
<input type="submit" name="submit" value="���M����">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}


