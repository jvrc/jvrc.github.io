#��������������������������������������������������������������������
#�� LIGHT BOARD
#�� pastlog.pl - 2009/01/17
#�� Copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

#-------------------------------------------------
#  �ߋ����O���
#-------------------------------------------------
sub pastlog {
	# �y�[�W��
	local($page) = 0;
	foreach ( keys(%in) ) {
		if (/^page(\d+)$/) {
			$page = $1;
			last;
		}
	}

	# �ߋ����ONo
	open(IN,"$pastno") || &error("Open Error: $pastno");
	my $no = <IN>;
	close(IN);

	$in{'pastlog'} =~ s/\D//g;
	if (!$in{'pastlog'}) {
		$in{'pastlog'} = $no;
	}
	$in{'pastlog'} = sprintf("%04d", $in{'pastlog'});

	&header;
	print <<EOM;
[<a href="$bbscgi?">�f���ɖ߂�</a>]
<hr>
<form action="$bbscgi" method="post">
<input type="hidden" name="mode" value="$mode">
<table>
<tr>
	<td><b>�ߋ����O�F</b> <select name="pastlog">
EOM

	# �ߋ����O�I��
	for ( my $i = $no; $i > 0; --$i ) {
		$i = sprintf("%04d", $i);
		next unless (-e "$pastdir/$i.cgi");
		if ($in{'pastlog'} == $i) {
			print "<option value=\"$i\" selected>$i\n";
		} else {
			print "<option value=\"$i\">$i\n";
		}
	}
	print "</select> <input type=\"submit\" value=\"�ړ�\">";
	print "</td></form><td width=\"20\"></td>\n";

	&search("$pastdir/$in{'pastlog'}.cgi");

	print "<dl>\n";

	my $i = 0;
	open(IN,"$pastdir/$in{'pastlog'}.cgi") || &error("Open Error: $in{'pastlog'}.cgi");
	while (<IN>) {
		my ($no,$dat,$nam,$eml,$sub,$com,$url) = split(/<>/);

		$i++;
		if ($i < $page + 1) { next; }
		if ($i > $page + $plog) { last; }

		&auto_link($com) if ($link);
		$com =~ s/([>]|^)(&gt;[^<]*)/$1<font color="$refcol">$2<\/font>/g;

		if ($eml) { $nam = "<a href=\"mailto:$eml\">$nam</a>"; }
		if ($url) { $url = "&lt;<a href=\"$url\" target=\"_blank\">URL</a>&gt;"; }

		print "<dt><hr>[<b>$no</b>] <b style=\"color:$subcol\">$sub</b> ";
		print "���e�ҁF<b>$nam</b> ���e���F$dat &nbsp; $url <br><br>";
		print "<dd>$com<br><br>\n";

	}
	close(IN);

	print "<dt><hr></dl>\n";

	# �y�[�W�J�z
	my $next = $page + $plog;
	my $back = $page - $plog;

	if ($back >= 0 || $next < $i) {
		print "<form action=\"$bbscgi\" method=\"post\">\n";
		print "<input type=\"hidden\" name=\"mode\" value=\"past\">\n";
		print "<input type=\"hidden\" name=\"pastlog\" value=\"$in{'pastlog'}\">\n";

		if ($back >= 0) {
			print "<input type=\"submit\" name=\"page$back\" value=\"�O��$plog��\">\n";
		}
		if ($next < $i) {
			print "<input type=\"submit\" name=\"page$next\" value=\"����$plog��\">\n";
		}

		print "</form>\n";
	}
	print "</body></html>\n";
	exit;
}


1;

