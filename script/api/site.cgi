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

my $ret = {};

$ret->{'log_tz'} = $obj_config->get('log_tz');

$ret->{'sites'} = [];
my $sth = $dbh->prepare('SELECT * FROM siteid');
$sth->execute();
while (my $cs = $sth->fetchrow_hashref) {
  push(@{$ret->{'sites'}}, $cs->{'val'});
}

print $obj_cgi->header(200);
print to_json(\%$ret);

exit;

