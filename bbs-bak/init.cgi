#��������������������������������������������������������������������
#�� LIGHT BOARD v7.0
#�� init.cgi - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'LIGHT BOARD v7.0';
#��������������������������������������������������������������������
#��[ ���ӎ��� ]
#�� 1.���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��   �����Ȃ鑹�Q�ɑ΂��č�҂͂��̐ӔC����ؕ����܂���B
#�� 2.�ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B���[����
#��   ��鎿��ɂ͂������ł��܂���B
#��������������������������������������������������������������������

#===========================================================
#  ���ݒ荀��
#===========================================================

# �O���t�@�C���y�T�[�o�p�X�z
$jcode    = 'jcode.pl';
$regkeypl = './lib/registkey.pl';
$registpl = './lib/regist.pl';
$editpl   = './lib/editlog.pl';
$searchpl = './lib/search.pl';
$pastpl   = './lib/pastlog.pl';
$checkpl  = './lib/check.pl';
$pastmkpl = './lib/pastmake.pl';

# �{�̃t�@�C��CGI�yURL�p�X�z
$bbscgi = './light.cgi';

# �Ǘ��t�@�C��CGI�yURL�p�X�z
$admincgi = './admin.cgi';

# ���O�t�@�C���y�T�[�o�p�X�z
$logfile = './data/data.cgi';

# �ݒ�t�@�C���y�T�[�o�p�X�z
$setfile = './data/light.dat';

# �p�X���[�h�t�@�C���y�T�[�o�p�X�z
$pwdfile = './data/pwd.cgi';

# sendmail�p�X�i���[���ʒm����ꍇ�j
# �� �� /usr/lib/sendmail
$sendmail = '/usr/sbin/sendmail';

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 1;

# �P�񓖂�̍ő哊�e�T�C�Y (bytes)
$maxData = 51200;

# ���O���m�F��\��������i0=no 1=yes�j
# �� ���e���ꂽ���O���Ǘ��҂��\���O�Ɋm�F����ꍇ�i�X�p�����C�^�Y���΍�j
$conf_log = 0;

# �ꎞ���O�f�B���N�g���y�T�[�o�p�X�z
$tmpdir = './tmp';

# �ꎞ���ONO�t�@�C���y�T�[�o�p�X�z
$tmpnum = './data/tmpnum.dat';

# �ꎞ���O�p�O���O�t�@�C���y�T�[�o�p�X�z
$tmplog = './data/tmplog.cgi';

## --- <�ȉ��́u���e�L�[�v�@�\�i�X�p���΍�j���g�p����ꍇ�̐ݒ�ł�> --- ##
#
# ���e�L�[�̎g�p�i�X�p���΍�j
# �� 0=no 1=yes
$regist_key = 1;

# ���e�L�[�摜�����t�@�C���yURL�p�X�z
$registkeycgi = './registkey.cgi';

# ���e�L�[�Í��p�p�X���[�h�i�p�����łW�����j
$pcp_passwd = 'pass7777';

# ���e�L�[���e���ԁi���P�ʁj
#   ���e�t�H�[����\�������Ă���A���ۂɑ��M�{�^�����������
#   �܂ł̉\���Ԃ𕪒P�ʂŎw��
$pcp_time = 30;

# ���e�L�[�摜�̑傫���i10�| or 12�|�j
# 10pt �� 10
# 12pt �� 12
$regkey_pt = 10;

# ���e�L�[�摜�̕����F
# �� $text�ƍ��킹��ƈ�a�����Ȃ��B�ڗ�������ꍇ�� #dd0000 �ȂǁB
$moji_col = '#dd0000';

# ���e�L�[�摜�̔w�i�F
# �� $bgcolor�ƍ��킹��ƈ�a�����Ȃ�
$back_col = '#f0f0f0';

#---(�ȉ��́u�ߋ����O�v�@�\���g�p����ꍇ�̐ݒ�ł�)---#
#
# �ߋ����O�@�\ (0=no 1=yes)
$pastkey = 0;

# �ߋ����O�f�B���N�g���y�T�[�o�p�X�z
$pastdir = './past';

# �ߋ����O�J�E���g�t�@�C���y�T�[�o�p�X�z
$pastno = './data/pastno.dat';

# �ߋ����O�P�t�@�C������̍ő匏��
$pastmax = 400;

#===========================================================
#  ���ݒ芮��
#===========================================================

#-------------------------------------------------
#  �t�H�[���f�R�[�h
#-------------------------------------------------
sub decode {
	my $buf;
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$post_flag = 1;
		if ($ENV{'CONTENT_LENGTH'} > $maxData) {
			&error("���e�ʂ��傫�����܂�");
		}
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$post_flag = 0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in);
	foreach ( split(/&/, $buf) ) {
		my ($key, $val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# S-JIS�R�[�h�ϊ�
		&jcode::convert(\$val, "sjis", "", "z");

		# �G�X�P�[�v
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/\0//g;
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	$mode = $in{'mode'};
	$headflag = 0;
	$ENV{'TZ'} = "JST-9";
}

#-------------------------------------------------
#  �ݒ�t�@�C���F��
#-------------------------------------------------
sub setfile {
	# �ݒ�t�@�C���ǂݍ���
	open(IN,"$setfile") || &error("Open Error: $setfile");
	my $file = <IN>;
	close(IN);

	# �ݒ���e�F��
	($title,$t_col,$t_size,$t_face,$t_img,$bg,$bc,$tx,$li,$vl,$al,$home,$max,$subcol,$refcol,$plog,$b_size,$mail,$deny,$link,$wait,$no_wd,$jp_wd,$urlnum) = split(/<>/, $file);

	# IP&�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }

	# �A�N�Z�X����
	if ($deny) {
		local($flag);
		foreach ( split(/\s+/, $deny) ) {
			s/\./\\\./g;
			s/\*/\.*/g;
			if ($host =~ /$_/i) { $flag = 1; last; }
		}
		if ($flag) { &error("�����������p�ł��܂���"); }
	}
	$b_size .= "px";
}

#-------------------------------------------------
#  HTML�w�b�_
#-------------------------------------------------
sub header {
	if ($headflag) { return; }

	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<meta http-equiv="content-style-type" content="text/css">
<style type="text/css">
<!--
body,td,th {
	font-size: $b_size;
	font-family: "MS UI Gothic","�l�r �o�S�V�b�N",Osaka;
}
.num { font-family:Verdana,Helvetica,Arial; }
.l { background-color: #666666; color: #ffffff; }
.r { background-color: #ffffff; color: #000000; }
-->
</style>
<title>$title</title></head>
EOM

	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$li\" vlink=\"$vl\" alink=\"$al\">\n";
	}
	$headflag = 1;
}

#-------------------------------------------------
#  �G���[����
#-------------------------------------------------
sub error {
	&header;
	print <<"EOM";
<div align="center">
<hr width="400">
<h3>ERROR !</h3>
<font color="#dd0000">$_[0]</font>
<p>
<form>
<input type="button" value="�O��ʂɖ߂�" onclick="history.back()">
</form>
<p>
<hr width="400">
</div>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �p�X���[�h�Í�
#-------------------------------------------------
sub encrypt {
	my $inp = shift;

	# ��╶������`
	my @char = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');

	# �����Ŏ�𒊏o
	srand;
	my $salt = $char[int(rand(@char))] . $char[int(rand(@char))];

	# �Í���
	crypt($inp, $salt) || crypt ($inp, '$1$' . $salt);
}

#-------------------------------------------------
#  �p�X���[�h�ƍ�
#-------------------------------------------------
sub decrypt {
	my ($inp, $log) = @_;

	# �풊�o
	my $salt = $log =~ /^\$1\$(.*)\$/ && $1 || substr($log, 0, 2);

	# �ƍ�
	if (crypt($inp, $salt) eq $log || crypt($inp, '$1$' . $salt) eq $log) {
		return 1;
	} else {
		return 0;
	}
}


1;

