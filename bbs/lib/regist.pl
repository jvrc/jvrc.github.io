#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� regist.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  ���e��t
#-------------------------------------------------
sub regist {
	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
	if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
	if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
		&error("e-mail�̓��͓��e������������܂���");
	}
	if ($in{'url'} eq "http://") { $in{'url'} = ""; }
	if ($in{'sub'} eq "") { $in{'sub'} = "����"; }
	if ($no_wd) { &no_wd; }
	if ($jp_wd) { &jp_wd; }
	if ($urlnum > 0) { &urlnum; }

	# ���e�L�[�`�F�b�N
	if ($regist_key) {
		require $regkeypl;

		if ($in{'regikey'} !~ /^\d{4}$/) {
			&error("���e�L�[�����͕s���ł��B<br>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}

		# ���e�L�[�`�F�b�N
		# -1 : �L�[�s��v
		#  0 : �������ԃI�[�o�[
		#  1 : �L�[��v
		my $chk = &registkey_chk($in{'regikey'}, $in{'str_crypt'});
		if ($chk == 0) {
			&error("���e�L�[���������Ԃ𒴉߂��܂����B<br>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐������ē��͂��Ă�������");
		} elsif ($chk == -1) {
			&error("���e�L�[���s���ł��B<br>���e�t�H�[���ɖ߂��čēǍ��݌�A�w��̐�������͂��Ă�������");
		}
	}

	# �폜�L�[�Í���
	local($pwd, $time, $date);
	if ($in{'pwd'} ne "") { $pwd = &encrypt($in{'pwd'}); }

	# ���Ԏ擾
	$time = time;
	my ($min,$hour,$mday,$mon,$year,$wday) = (localtime($time))[1..6];
	my @wk = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
				$year+1900,$mon+1,$mday,$wk[$wday],$hour,$min);

	# �ꎞ�t�@�C�����e�̂Ƃ�
	if ($conf_log == 1) {
		&conf_log;

	# �����f�̂Ƃ�
	} else {
		&add_log;
	}

	# �N�b�L�[�𔭍s
	&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'});

	# ���[������
	if ($sendmail && $mail && $in{'email'} ne $mail) { &mailto; }

	# �������b�Z�[�W
	&message("���e�͐���ɏ�������܂���");
}

#-------------------------------------------------
#  �L���ǉ�
#-------------------------------------------------
sub add_log {
	# ���O���J��
	local($i, @data, @past);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	my $top = <DAT>;

	# ��d���e�֎~
	my ($no,$dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $top);
	if ($host eq $ho && $wait > $time - $tim) {
		close(DAT);
		&error("�A�����e�͂������΂炭���Ԃ�u���Ă�������");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		close(DAT);
		&error("��d���e�͋֎~�ł�");
	}

	# �L��������
	$data[0] = $top;
	while (<DAT>) {
		$i++;

		# ���s���O
		if ($i < $max-1) {
			push(@data,$_);

		# �ߋ����O
		} elsif ($pastkey) {
			push(@past,$_);
		}
	}

	# �L��No
	$no++;

	# �X�V
	seek(DAT, 0, 0);
	print DAT "$no<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>\n";
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	# �ߋ����O�X�V
	if (@past > 0) {
		require $pastmkpl;
		&past_make;
	}
}

#-------------------------------------------------
#  �N�b�L�[���s
#-------------------------------------------------
sub set_cookie {
	my @cook = @_;

	my @t = gmtime(time + 60*24*60*60);
	my @m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	my @w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# ���ەW�������`
	my $gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# �ۑ��f�[�^��URL�G���R�[�h
	my $cook;
	foreach (@cook) {
		# �^�O�r��
		s/&gt;//g;
		s/&lt;//g;
		s/&quot;//g;
		s/&amp;//g;

		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# �i�[
	print "Set-Cookie: LIGHT_BOARD=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  ���[�����M
#-------------------------------------------------
sub mailto {
	# �L���̉��s�E�^�O�𕜌�
	my $com  = $in{'comment'};
	$com =~ s/<br>/\n/g;
	$com =~ s/&lt;/��/g;
	$com =~ s/&gt;/��/g;
	$com =~ s/&quot;/�h/g;
	$com =~ s/&amp;/��/g;

	# ���[���{�����`
	my $mbody = <<"EOM";
���e�����F$date
�z�X�g���F$host
�u���E�U�F$ENV{'HTTP_USER_AGENT'}

���e�Җ��F$in{'name'}
�d���[���F$in{'email'}
�t�q�k  �F$in{'url'}
�^�C�g���F$in{'sub'}

$com
EOM

	# �薼��BASE64��
	my $msub = &base64("[$title : $no] $in{'sub'}");

	# ���[���A�h���X���Ȃ��ꍇ
	my $email;
	if ($in{'email'} eq "") { $email = $mail; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t -i") || &error("���[�����M���s");
	print MAIL "To: $mail\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";

	foreach ( split(/\n/, $mbody) ) {
		&jcode::convert(\$_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}

	close(MAIL);
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#	�Ƃقق�WWW����Ō��J����Ă��郋�[�`�����Q�l�ɂ��܂����B
#	http://www.tohoho-web.com/
sub base64 {
	my ($sub) = @_;
	&jcode::convert(\$sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	my $ch = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	my ($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i = 0; $y = substr($x,$i,6); $i += 6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  �������b�Z�[�W
#-------------------------------------------------
sub message {
	local($msg) = @_;

	&header;
	print <<EOM;
<blockquote>
<h3>$msg</h3>
<form action="$bbscgi">
<input type="submit" value="�f���֖߂�">
</form>
</blockquote>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  �֎~���[�h�`�F�b�N
#-------------------------------------------------
sub no_wd {
	my $flg;
	foreach ( split(/\s+/, $no_wd) ) {
		if (index("$in{'name'} $in{'sub'} $in{'comment'}", $_) >= 0) {
			$flg = 1;
			last;
		}
	}
	if ($flg) { &error("�֎~���[�h���܂܂�Ă��܂�"); }
}

#-------------------------------------------------
#  ���{��`�F�b�N
#-------------------------------------------------
sub jp_wd {
	if ($in{'comment'} !~ /[\x81-\x9F\xE0-\xFC][\x40-\x7E\x80-\xFC]/) {
		&error("�R�����g�ɓ��{�ꂪ�܂܂�Ă��܂���");
	}
}

#-------------------------------------------------
#  URL���`�F�b�N
#-------------------------------------------------
sub urlnum {
	my $com = $in{'comment'};
	my $num = ($com =~ s|(https?://)|$1|ig);
	if ($num > $urlnum) {
		&error("�R�����g����URL�A�h���X�͍ő�$urlnum�܂łł�");
	}
}

#-------------------------------------------------
#  �ꎞ�t�@�C���ۑ�
#-------------------------------------------------
sub conf_log {
	# �O���O
	open(TMP,"+< $tmplog") || &error("Open Error: $tmplog");
	eval "flock(TMP, 2);";
	my $data = <TMP>;

	# ��d���e�֎~
	my ($dat,$nam,$eml,$sub,$com,$url,$ho,$pw,$tim) = split(/<>/, $data);
	if ($host eq $ho && $wait > $time - $tim) {
		close(TMP);
		&error("�A�����e�͂������΂炭���Ԃ�u���Ă�������");
	}
	if ($in{'name'} eq $nam && $in{'comment'} eq $com) {
		close(TMP);
		&error("��d���e�͋֎~�ł�");
	}

	# ��������
	seek(TMP, 0, 0);
	print TMP "$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>";
	truncate(TMP, tell(TMP));
	close(TMP);

	# �̔�
	open(NO,"+< $tmpnum") || &error("Open Error: $tmpnum");
	eval "flock(NO, 2);";
	my $num = <NO> + 1;
	seek(NO, 0, 0);
	print NO $num;
	truncate(NO, tell(NO));
	close(NO);

	# �t�@�C������
	open(TMP,"+> $tmpdir/$num.cgi");
	eval "flock(TMP, 2);";
	print TMP "$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pwd<>$time<>";
	close(TMP);
}


1;

