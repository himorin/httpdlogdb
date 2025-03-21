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

my $ret;

if ($c_tgt eq 'page') {
  my $c_date = $obj_cgi->param('date');
  my $c_page = $obj_cgi->param('page');
  $ret->{'site'} = $c_site;
  $ret->{'target'} = $c_tgt;
  if (defined($c_date)) {
    $ret->{'analysis'} = 'date';
    $ret->{'date'} = $c_date;
    $sth = $dbh->prepare('SELECT * FROM ana_page INNER JOIN dirid ON ana_page.dir = dirid.id AND ana_page.site = ? AND ana_page.target = ? ORDER BY value DESC');
    $sth->execute($c_sid, $c_date);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'val'}} = $cur->{'value'};
    }
  } elsif (defined($c_page)) {
    $ret->{'analysis'} = 'page';
    $ret->{'page'} = $c_page;
    $sth = $dbh->prepare('SELECT * FROM ana_page INNER JOIN dirid ON ana_page.dir = dirid.id AND dirid.val = ? AND ana_page.site = ? ORDER BY ana_page.target DESC');
    $sth->execute($c_page, $c_sid);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'target'}} = $cur->{'value'};
    }
  } else {
    $obj_cgi->send_error(400, 'parameter error');
    exit;
  }
} else {
  $obj_cgi->send_error(400, 'parameter error');
  exit;
}


print $obj_cgi->header(200);
print to_json(\%$ret);

exit;

