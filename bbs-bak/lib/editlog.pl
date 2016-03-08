#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� edit.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �L���C��
#-------------------------------------------------
sub editlog {
	# ���̓`�F�b�N
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# �C�����s
	if ($in{'submit'}) {

		# �`�F�b�N
		if ($no_wd) { &no_wd; }
		if ($jp_wd) { &jp_wd; }
		if ($urlnum > 0) { &urlnum; }

		# �����̓`�F�b�N
		if ($in{'name'} eq "") { &error("���O�����͂���Ă��܂���"); }
		if ($in{'comment'} eq "") { &error("�R�����g�����͂���Ă��܂���"); }
		if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,5}$/) {
			&error("�d���[���̓��͓��e������������܂���");
		}
		if ($in{'url'} eq "http://") { $in{'url'} = ""; }
		if ($in{'sub'} eq "") { $in{'sub'} = "����"; }

		# �����ւ�
		my ($flg, @data);
		open(DAT,"+< $logfile") || &error("Open Error: $logfile");
		eval "flock(DAT, 2);";
		while (<DAT>) {
			my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd,$tim) = split(/<>/);

			if ($in{'no'} == $no) {

				# �F�؃`�F�b�N
				if ($pwd eq "" || &decrypt($in{'pwd'}, $pwd) != 1) {
					$flg = -1;
					last;
				}

				$flg = 1;
				$_ = "$no<>$dat<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$hos<>$pwd<>$tim<>\n";
			}
			push(@data,$_);
		}

		if ($flg != 1) {
			close(DAT);
			&error("�s���ȏ����ł�");
		}

		# �X�V
		seek(DAT, 0, 0);
		print DAT @data;
		truncate(DAT, tell(DAT));
		close(DAT);

		# �������b�Z�[�W
		&message("�L���̏C�����������܂���");
	}

	# �L�����o
	my ($flg, @edit);
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		if ($in{'no'} == $no) {

			# �p�X���[�h�Ȃ�
			if ($pwd eq "") {
				$flg = 2;
			}

			# �p�X���[�h��v
			if (&decrypt($in{'pwd'}, $pwd) == 1) {
				$flg = 1;
				@edit = ($no,$dat,$nam,$eml,$sub,$com,$url);

			# �p�X���[�h�s��v
			} else {
				$flg = 3;
			}
			last;
		}
	}
	close(IN);

	if (!$flg) {
		close(DAT);
		&error("�Y���L������������܂���");
	} elsif ($flg == 2) {
		close(DAT);
		&error("���̋L���ɂ̓p�X���[�h���ݒ肳��Ă��܂���");
	} elsif ($flg == 3) {
		close(DAT);
		&error("�p�X���[�h���Ⴂ�܂�");
	}

	# �C���t�H�[��
	&edit_form(@edit);
}

#-------------------------------------------------
#  �L���폜
#-------------------------------------------------
sub delelog {
	# ���̓`�F�b�N
	if (!$post_flag) { &error("�s���ȃA�N�Z�X�ł�"); }
	if ($in{'no'} eq "" || $in{'pwd'} eq "") {
		&error("�L��No���̓p�X���[�h�����͂���Ă��܂���");
	}

	# ���O��ǂݍ���
	my ($flg, @data);
	open(DAT,"+< $logfile") || &error("Open Error: $logfile");
	eval "flock(DAT, 2);";
	while (<DAT>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url,$hos,$pwd) = split(/<>/);

		if ($in{'no'} == $no) {

			# �p�X���[�h�Ȃ�
			if ($pwd eq "") {
				$flg = 2;
				last;
			}

			# �p�X���[�h��v
			if (&decrypt($in{'pwd'}, $pwd) == 1) {
				$flg = 1;
				next;

			# �p�X���[�h�s��v
			} else {
				$flg = 3;
				last;
			}
		}
		push(@data,$_);
	}

	if (!$flg) {
		close(DAT);
		&error("�Y���L������������܂���");
	} elsif ($flg == 2) {
		close(DAT);
		&error("���̋L���ɂ̓p�X���[�h���ݒ肳��Ă��܂���");
	} elsif ($flg == 3) {
		close(DAT);
		&error("�p�X���[�h���Ⴂ�܂�");
	}

	# ���O�X�V
	seek(DAT, 0, 0);
	print DAT @data;
	truncate(DAT, tell(DAT));
	close(DAT);

	# �������b�Z�[�W
	&message("�L���͐���ɍ폜����܂���");
}

#-------------------------------------------------
#  �ҏW�t�H�[��
#-------------------------------------------------
sub edit_form {
	my ($no,$dat,$nam,$eml,$sub,$com,$url) = @_;
	if (!$url) { $url = "http://"; }
	$com =~ s/<br>/\n/g;

	# �ҏW���
	&header;
	print <<EOM;
[<a href="javascript:history.back()">�O��ʂɖ߂�</a>]
<h3>�ҏW�t�H�[��</h3>
<ul>
<li>�C�����镔���̂ݕύX���Ă��������B
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="$mode">
<input type="hidden" name="no" value="$in{'no'}">
<input type="hidden" name="pwd" value="$in{'pwd'}">
���e�Җ�<br><input type="text" name="name" size="28" value="$nam"><br>
�d���[��<br><input type="text" name="email" size="28" value="$eml"><br>
�^�C�g��<br><input type="text" name="sub" size="36" value="$sub"><br>
�Q�Ɛ�<br><input type="text" name="url" size="45" value="$url"><br>
�R�����g<br><textarea name="comment" cols="58" rows="7">$com</textarea><br>
<input type="submit" name="submit" value="���M����">
</form>
</ul>
</body>
</html>
EOM
	exit;
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


1;

