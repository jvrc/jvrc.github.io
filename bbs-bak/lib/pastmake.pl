#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� pastmake.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �ߋ����O����
#-------------------------------------------------
sub past_make {
	# �ߋ����O�t�@�C�������`
	open(NO,"+< $pastno") || &error("Open Error: $pastno");
	eval "flock(NO, 2);";
	my $count = <NO>;
	$count = sprintf("%04d", $count);

	# �ߋ����O���J��
	my $i = 0;
	my ($flg, @data);
	open(LOG,"+< $pastdir/$count.cgi") || &error("Open Error: $count.cgi");
	eval "flock(LOG, 2);";
	while (<LOG>) {
		$i++;
		push(@data,$_);

		# �ő匏���𒴂���ƒ��f
		if ($i >= $pastmax) {
			$flg++;
			last;
		}
	}

	# �ő匏�����I�[�o�[����Ǝ��t�@�C������������
	if ($flg) {

		# �ߋ����O����U����
		close(LOG);

		# �J�E���g�t�@�C�����A�b�v
		$count = sprintf("%04d", $count+1);

		# �J�E���g�t�@�C���X�V
		seek(NO, 0, 0);
		print NO $count;
		truncate(NO, tell(NO));
		close(NO);

		# �V�ߋ����O
		open(LOG,"+> $pastdir/$count.cgi") || &error("Write Error: $count.cgi");
		eval "flock(LOG, 2);";
		print LOG @past;
		close(LOG);

		chmod(0666, "$pastdir/$count.cgi");

	# ���L�ߋ����O�̂܂�
	} else {

		unshift(@data,@past);
		seek(LOG, 0, 0);
		print LOG @data;
		truncate(LOG, tell(LOG));
		close(LOG);
	}
}


1;

