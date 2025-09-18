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
  my $c_dst = $obj_cgi->param('dst');
  my $c_ded = $obj_cgi->param('ded');
  my $c_page = $obj_cgi->param('page');
  $ret->{'site'} = $c_site;
  $ret->{'target'} = $c_tgt;
  if (defined($c_dst) && defined($c_ded)) {
    $ret->{'analysis'} = 'date';
    $ret->{'dst'} = $c_dst;
    $ret->{'ded'} = $c_ded;
    $sth = $dbh->prepare('SELECT SUM(ana_page.value) AS sum, dirid.val FROM ana_page INNER JOIN dirid ON ana_page.dir = dirid.id AND ana_page.site = ? AND ana_page.target >= ? AND ana_page.target <= ? GROUP BY dirid.val ORDER BY sum DESC');
    $sth->execute($c_sid, $c_dst, $c_ded);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'val'}} = $cur->{'sum'};
    }
  } elsif (defined($c_page)) {
    $ret->{'analysis'} = 'page';
    $ret->{'page'} = $c_page;
    $sth = $dbh->prepare('SELECT SUM(ana_page.value) AS sum, ana_page.target FROM ana_page INNER JOIN dirid ON ana_page.dir = dirid.id AND dirid.val = ? AND ana_page.site = ? GROUP BY ana_page.target ORDER BY ana_page.target DESC');
    $sth->execute($c_page, $c_sid);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'target'}} = $cur->{'sum'};
    }
  } else {
    $obj_cgi->send_error(400, 'parameter error page');
    exit;
  }
} elsif ($c_tgt eq 'ref') {
  my $c_dst = $obj_cgi->param('dst');
  my $c_ded = $obj_cgi->param('ded');
  my $c_page = $obj_cgi->param('page');
  $ret->{'site'} = $c_site;
  $ret->{'target'} = $c_tgt;
  if (defined($c_dst) && defined($c_ded) && defined($c_page)) {
    $ret->{'analysis'} = 'date_page';
    $ret->{'dst'} = $c_dst;
    $ret->{'ded'} = $c_ded;
    $ret->{'page'} = $c_page;
    $sth = $dbh->prepare('SELECT SUM(ana_ref.value) AS sum, referid.val FROM ana_ref INNER JOIN dirid ON ana_ref.dir = dirid.id AND ana_ref.site = ? AND ana_ref.target >= ? AND ana_ref.target <= ? INNER JOIN referid ON ana_ref.refer = referid.id WHERE referid.val != "-" AND dirid.val = ? GROUP BY ana_ref.refer ORDER BY SUM(ana_ref.value) DESC');
    $sth->execute($c_sid, $c_dst, $c_ded, $c_page);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'val'}} = $cur->{'sum'}; 
    }
  } elsif (defined($c_dst) && defined($c_ded)) {
    $ret->{'analysis'} = 'date';
    $ret->{'dst'} = $c_dst;
    $ret->{'ded'} = $c_ded;
    $sth = $dbh->prepare('SELECT SUM(ana_ref.value) AS sum, referid.val FROM ana_ref INNER JOIN dirid ON ana_ref.dir = dirid.id AND ana_ref.site = ? AND ana_ref.target >= ? AND ana_ref.target <= ? INNER JOIN referid ON ana_ref.refer = referid.id WHERE referid.val != "-" GROUP BY ana_ref.refer ORDER BY SUM(ana_ref.value) DESC');
    $sth->execute($c_sid, $c_dst, $c_ded);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'val'}} = $cur->{'sum'}; 
    }
  } elsif (defined($c_page)) {
    $ret->{'analysis'} = 'page';
    $ret->{'page'} = $c_page;
    $sth = $dbh->prepare('SELECT SUM(ana_ref.value) AS sum, referid.val FROM ana_ref INNER JOIN dirid ON ana_ref.dir = dirid.id AND ana_ref.site = ? INNER JOIN referid ON ana_ref.refer = referid.id WHERE referid.val != "-" AND dirid.val = ? GROUP BY ana_ref.refer ORDER BY SUM(ana_ref.value) DESC');
    $sth->execute($c_sid, $c_page);
    $ret->{'count'} = {};
    while (my $cur = $sth->fetchrow_hashref()) {
      $ret->{'count'}->{$cur->{'val'}} = $cur->{'sum'}; 
    }
  } else {
    $obj_cgi->send_error(400, 'parameter error ref');
    exit;
  }
} else {
  $obj_cgi->send_error(400, 'parameter error target');
  exit;
}


print $obj_cgi->header(200);
print to_json(\%$ret);

exit;
