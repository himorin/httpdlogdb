#! /usr/bin/perl

use strict;
use lib '../';

use JSON;
use PNAPI::Constants;
use PNAPI::Config;
use PNAPI::CGI;
use PNAPI::DB;

my $obj_cgi = new PNAPI::CGI;
my $obj_config = new PNAPI::Config;
my $obj_db = new PNAPI::DB;
my $dbh = $obj_db->dbh();
my $sth;

my $c_site = $obj_cgi->param('site');
my $c_tgt = $obj_cgi->param('target');

$sth = $dbh->prepare('SELECT * FROM siteid WHERE val = ?');
$sth->execute($c_site);
if ($sth->rows != 1) {
  $obj_cgi->send_error(404, 'site not found');
  exit;
}
my $tmp = $sth->fetchrow_hashref();
my $c_sid = $tmp->{'id'};

my $c_dst = $obj_cgi->param('dst');
my $c_ded = $obj_cgi->param('ded');
my $c_page = $obj_cgi->param('page');

my $ret;

if ($c_tgt eq 'sns_fb') {
  $ret->{'site'} = $c_site;
  $ret->{'target'} = $c_tgt;
  my @params = ($c_sid);
  my $query = 'SELECT COUNT(atime) AS sum, query, dirid.val FROM rawlog INNER JOIN dirid ON rawlog.dir = dirid.id WHERE site = ? AND ';
  if (defined($c_dst) && defined($c_ded)) {
    $query .= ' atime >= ? AND atime <= ? AND ';
    push(@params, ($c_dst, $c_ded));
    $ret->{'dst'} = $c_dst;
    $ret->{'ded'} = $c_ded;
  }
  if (defined($c_page)) {
    $query .= ' dirid.val = ? AND ';
    push(@params, $c_page);
    $ret->{'page'} = $c_page;
  }
  $query .= ' INSTR(query, "fbclid=") > 0 GROUP BY query, dir';
  $sth = $dbh->prepare($query);
  $sth->execute(@params);
  $ret->{'count'} = {};
  while (my $cur = $sth->fetchrow_hashref()) {
    my $dat = { "sum" => $cur->{'sum'}, "page" => $cur->{'val'} };
    $ret->{'count'}->{$cur->{'query'}} = $dat;
  }
} elsif ($c_tgt eq 'sns_x') {
  $ret->{'site'} = $c_site;
  $ret->{'target'} = $c_tgt;
  my @params = ($c_sid);
  my $query = 'SELECT referid.val AS refer, dirid.val AS dir, COUNT(*) AS sum FROM referid INNER JOIN rawlog ON INSTR(referid.val, "https://t.co") > 0 AND referid.id = rawlog.dir INNER JOIN dirid ON rawlog.dir = dirid.id ';
  if (defined($c_dst) && defined($c_ded)) {
    $query .= ' rawlog.atime >= ? AND rawlog.atime <= ? AND ';
    push(@params, ($c_dst, $c_ded));
    $ret->{'dst'} = $c_dst;
    $ret->{'ded'} = $c_ded;
  }
  if (defined($c_page)) {
    $query .= ' dirid.val = ? AND ';
    push(@params, $c_page);
    $ret->{'page'} = $c_page;
  }
  $query .= ' GROUP BY referid.id, rawlog.dir;';
  $sth = $dbh->prepare($query);
  $sth->execute(@params);
  $ret->{'count'} = {};
  while (my $cur = $sth->fetchrow_hashref()) {
    my $dat = { "sum" => $cur->{'sum'}, "page" => $cur->{'dir'} };
    $ret->{'count'}->{$cur->{'refer'}} = $dat;
  }
} else {
  $obj_cgi->send_error(400, 'parameter error target');
  exit;
}


print $obj_cgi->header(200);
print to_json(\%$ret);

exit;
