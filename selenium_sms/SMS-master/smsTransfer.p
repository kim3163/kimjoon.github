#!/usr/bin/perl

use IO::Socket;
use POSIX;

MAIN:
{
    if (! @ARGV) {
        print "Usage: $0 FROM[0] TO,TO,TOs 'MSG'\n";
        exit(0);
    }

    my $FROM = $ARGV[0];
warn "FROM: $FROM";
    my @TOs = split(/,/, $ARGV[1]);
warn "TO: @TOs";
    my $MSG = $ARGV[2];
warn "MSG: $MSG";

    my $time = POSIX::strftime("%Y-%m-%d_%H:%M:%S", localtime(time()));

    foreach my $TO (@TOs) {
        my $sock = new IO::Socket::INET(PeerAddr=>"mail.mobigen.com", PeerPort=>"110");
        if (! defined $sock) {
            warn "Socket(mail.mobigen.com:110) failed:$!";
            next;
        }
        my $welcome = <$sock>; # print $welcome;
#        # print "SEND-SMS $FROM $TO $MSG\n";
        print $sock "SEND-SMS $FROM $TO $MSG\r\n";
        close($sock);
    }
}
