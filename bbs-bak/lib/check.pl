#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� check.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	&header;
	print <<EOM;
<h2>Check Mode</h2>
<ul>
EOM

	# ���O�`�F�b�N
	foreach ( $logfile, $setfile, $pwdfile, $tmpnum, $tmplog ) {
		if (-f $_) {
			print "<li>�p�X�F$_ �� OK\n";

			if (-r $_ && -w $_) {
				print "<li>�p�[�~�b�V�����F$_ �� OK\n";
			} else {
				print "<li>�p�[�~�b�V�����F$_ �� NG\n";
			}
		} else {
			print "<li>�p�X�F$_ �� NG\n";
		}
	}

	# �f�B���N�g��
	if (-d $tmpdir) {
		print "<li>�f�B���N�g���p�X�F$tmpdir �� OK\n";
		if (-r $tmpdir && -w $tmpdir && -x $tmpdir) {
			print "<li>�f�B���N�g���p�[�~�b�V�����F$_ �� OK\n";
		} else {
			print "<li>�f�B���N�g���p�[�~�b�V�����F$_ �� NG\n";
		}
	} else {
		print "<li>�f�B���N�g���p�X�F$_ �� NG\n";
	}

	# �ߋ����O
	@yn = ('�Ȃ�', '����');
	print "<li>�ߋ����O�F$yn[$pastkey]\n";
	if ($pastkey) {
		if (-f $pastno) {
			print "<li>�p�X�F$pastno �� OK\n";
			if (-r $pastno && -w $pastno) {
				print "<li>�p�[�~�b�V�����F$pastno �� OK\n";
			} else {
				print "<li>�p�[�~�b�V�����F$pastno �� NG\n";
			}
		} else {
			print "<li>�p�X�F$pastno �� NG\n";
		}
		if (-d $pastdir) {
			print "<li>�p�X�F$pastdir �� OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<li>�p�[�~�b�V�����F$pastdir �� OK\n";
			} else {
				print "<li>�p�[�~�b�V�����F$pastdir �� NG\n";
			}
		} else {
			print "<li>�p�X�F$pastdir �� NG\n";
		}
	}
	print "</ul>\n</body></html>\n";
	exit;
}



1;

