#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� search.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  ��������
#-------------------------------------------------
sub search {
	my ($target) = @_;

	# �y�[�W��
	my $page = 0;
	foreach ( keys(%in) ) {
		if (/^page(\d+)$/) {
			$page = $1;
			last;
		}
	}

	print "<td><form action=\"$bbscgi\" method=\"post\">\n";
	print "<input type=\"hidden\" name=\"mode\" value=\"$mode\">\n";

	my $param;
	if ($in{'pastlog'}) {
		print "<input type=\"hidden\" name=\"pastlog\" value=\"$in{'pastlog'}\">\n";
		$param = "&pastlog=$in{'pastlog'}";
	}

	print "�L�[���[�h <input type=\"text\" name=\"word\" size=\"40\" value=\"$in{'word'}\"> ";
	print "���� <select name=\"cond\"> &nbsp; ";

	if ($in{'cond'} eq "") { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq $_) {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}

	print "</select> �\\�� <select name=\"view\">\n";

	if ($in{'view'} eq "") { $in{'view'} = 10; }
	foreach (10,15,20,25,30) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_��\n";
		} else {
			print "<option value=\"$_\">$_��\n";
		}
	}

	print "</select> <input type=\"submit\" value=\" ���� \">";
	print "</td></form></tr></table>\n";

	## --- �������s
	if ($in{'word'} ne "") {

		# ���͓��e����
		$in{'word'} =~ s/�@/ /g;
		my @wd = split(/\s+/, $in{'word'});

		print "<dl>\n";

		# �t�@�C����ǂݍ���
		my $i = 0;
		open(IN,"$target") || &error("Open Error: $target");
		while (<IN>) {
			my ($no,$ymd,$nam,$eml,$sub,$com,$url) = split(/<>/);

			my $flg;
			foreach $wd (@wd) {
				if (index("$nam $eml $sub $com $url", $wd) >= 0) {
					$flg = 1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') {
						$flg = 0;
						last;
					}
				}
			}
			if ($flg) {
				$i++;
				if ($i < $page + 1) { next; }
				if ($i > $page + $in{'view'}) { next; }

				if ($eml) { $nam = "<a href=\"mailto:$eml\">$nam</a>"; }
				if ($url) { $com .= "<p><a href=\"$url\" target=\"_blank\">$url</a>"; }

				print "<dt><hr>[<b>$no</b>] <b style=\"color:$subcol\">$sub</b> ";
				print "���e�ҁF<b>$nam</b> ���e���F$ymd<br><br>\n";
				print "<dd>$com<br><br>\n";
			}
		}
		close(IN);

		print "<dt><hr>�������ʁF<b>$i</b>��</dl>\n";

		my $next = $page + $in{'view'};
		my $back = $page - $in{'view'};
		my $enwd = &url_enc($in{'word'});
		if ($back >= 0) {
			print "[<a href=\"$bbscgi?mode=$mode&page$back=1&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$param\">�O��$in{'view'}��</a>]\n";
		}
		if ($next < $i) {
			print "[<a href=\"$bbscgi?mode=$mode&page$next=1&word=$enwd&view=$in{'view'}&cond=$in{'cond'}$param\">����$in{'view'}��</a>]\n";
		}
		print "</body></html>\n";
		exit;
	}
	## --- ���������܂�
}

#-------------------------------------------------
#  URL�G���R�[�h
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}


1;

